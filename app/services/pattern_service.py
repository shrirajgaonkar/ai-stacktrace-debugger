from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Pattern
from app.patterns.seed_patterns import SEED_PATTERNS
import asyncio

async def seed_patterns_if_empty(db: AsyncSession):
    result = await db.execute(select(Pattern).limit(1))
    if result.scalars().first():
        return
        
    for p in SEED_PATTERNS:
        new_pattern = Pattern(
            name=p["name"],
            runtime=p["runtime"],
            regexes=p["regexes"],
            description=p["description"],
            common_causes=p["common_causes"],
            common_fixes=p["common_fixes"],
            references=p["references"]
        )
        db.add(new_pattern)
    await db.commit()

async def get_all_patterns(db: AsyncSession):
    result = await db.execute(select(Pattern))
    return result.scalars().all()
