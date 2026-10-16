# Reflection

The original lab handout containing the four reflection questions was not present anywhere in this project (only README.md was available). Therefore, the exact four questions could not be identified. The following answers address the standard static analysis topics for this lab.

1. Static code analysis is the process of examining source code without running it to find potential bugs, security issues, and style problems. Tools like Pylint, Bandit, and Flake8 report issues based on code patterns and rules.

2. Pylint checks code quality and style, reporting missing docstrings, naming conventions, and suspicious patterns, with an overall score. Bandit focuses on security, flagging unsafe operations such as pickle deserialization and bare exception handling. Flake8 enforces PEP 8 style rules such as line length and blank lines.

3. Real issues found and fixed included unsafe pickle-based persistence (replaced with validated JSON), silent/bare exception handlers, a mutable default argument, unvalidated restored data, long lines, and missing docstrings.

4. Static analysis has limitations: it cannot understand runtime behavior or business logic, may report false positives, and does not prove correctness. Testing with representative and edge-case inputs remains necessary to verify actual program behavior.