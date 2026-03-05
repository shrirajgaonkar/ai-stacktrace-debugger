from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Session, Pattern
from app.parsing.pipeline import process_log
from app.patterns.matcher import find_best_match
from app.llm.router import LLMRouter
from app.llm.prompts import (
    EXPLAIN_SYSTEM_V1,
    ROOT_CAUSE_SYSTEM_V1,
    FIX_STEPS_SYSTEM_V1,
    build_user_prompt,
)
from app.services.pattern_service import get_all_patterns
from app.llm.validators import validate_root_causes, validate_fix_steps


async def process_session(session_id: str, db: AsyncSession):
    # Retrieve Session
    result = await db.execute(select(Session).where(Session.id == session_id))
    session = result.scalars().first()

    if not session:
        return

    session.status = "processing"
    await db.commit()

    try:
        # -------------------------
        # A) Parse Log
        # -------------------------
        parsed_data = process_log(session.raw_log)

        session.runtime_detected = parsed_data.get("runtime_detected")
        session.parsed_frames = parsed_data.get("parsed_frames")

        # -------------------------
        # B) Pattern Matching
        # -------------------------
        all_patterns = await get_all_patterns(db)

        pattern_id, confidence = find_best_match(session.raw_log, all_patterns)

        if pattern_id:
            session.matched_pattern_id = pattern_id
            session.pattern_confidence = confidence

        pattern_context = None

        if pattern_id:
            ptn_res = await db.execute(select(Pattern).where(Pattern.id == pattern_id))
            ptn = ptn_res.scalars().first()

            if ptn:
                pattern_context = (
                    f"Matched known pattern: {ptn.name}. "
                    f"Description: {ptn.description}. "
                    f"Known causes: {ptn.common_causes}."
                )

        # -------------------------
        # C) Run LLM Tasks
        # -------------------------
        router = LLMRouter()
        provider = router.get_provider_for_log(session.raw_log)

        user_prompt = build_user_prompt(
            session.raw_log,
            session.parsed_frames,
            pattern_context,
        )

        # Explanation
        explain_text = await router.get_explanation(
            provider,
            EXPLAIN_SYSTEM_V1,
            user_prompt,
        )
        session.llm_explanation = explain_text

        # Root causes
        root_causes = await router.get_json_structure(
            provider,
            ROOT_CAUSE_SYSTEM_V1,
            user_prompt,
        )

        if validate_root_causes(root_causes):
            session.root_causes = root_causes
        else:
            session.root_causes = {
                "error": "Invalid root cause schema returned by LLM"
            }

        # Fix steps
        fix_steps = await router.get_json_structure(
            provider,
            FIX_STEPS_SYSTEM_V1,
            user_prompt,
        )

        if validate_fix_steps(fix_steps):
            session.suggested_fixes = fix_steps
        else:
            session.suggested_fixes = {
                "error": "Invalid fix steps schema returned by LLM"
            }

        session.status = "completed"

    except Exception as e:
        import traceback

        traceback.print_exc()

        session.status = "failed"
        session.llm_explanation = f"Processing failed: {str(e)}"

    await db.commit()