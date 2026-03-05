SEED_PATTERNS = [
    {
        "name": "Python ZeroDivisionError",
        "runtime": "python",
        "regexes": [r"ZeroDivisionError: division by zero"],
        "description": "Attempted to divide a number by zero.",
        "common_causes": ["Unvalidated user input", "Empty list length calculation"],
        "common_fixes": ["Add a check if denominator is zero before division"],
        "references": ["https://docs.python.org/3/library/exceptions.html#ZeroDivisionError"]
    },
    {
        "name": "Node.js TypeError Cannot read property",
        "runtime": "node",
        "regexes": [r"TypeError: Cannot read properties of undefined \(reading '.*'\)"],
        "description": "Attempted to access a property on an undefined object.",
        "common_causes": ["Missing API response fields", "Uninitialized state"],
        "common_fixes": ["Use optional chaining (?.)", "Add defined checks"],
        "references": ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors/Cant_access_property"]
    }
]
