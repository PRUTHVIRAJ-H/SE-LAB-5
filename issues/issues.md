# Lab 5: Static Code Analysis Issues

**Student:** Pruthviraj H  
**SRN:** PES2UG24CS381  
**Program:** `pharmacy_system.py`

## Issue Table

| Issue | Type | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| SQL injection risk | Security, medium | 21 | The patient name was joined directly into an SQL string. A crafted name could change the query. Bandit reported B608. | Used a parameterized query with a `?` placeholder and passed the name separately. |
| Mutable default argument | Bug | 24 | `batch_log=[]` was shared between calls, so previous calls could affect later results. Pylint reported W0102. | Changed the default to `None` and created a new list inside the function. |
| Bare exception in dispensing | Reliability | 38 | A bare `except` hid every error, including programming errors, and made debugging difficult. Pylint and Flake8 reported it. | Caught only the expected `IndexError` and `KeyError` cases. |
| Bare exception while loading stock | Security, low | 58 | The exception was silently ignored with `pass`, hiding invalid or missing input. Bandit reported B110. | Used `FileNotFoundError` and `json.JSONDecodeError` explicitly and reset stock safely. |
| Unmanaged file handles | Quality | 50, 57 | Files were opened without `with` blocks and without an explicit encoding. Pylint reported R1732 and W1514. | Used context managers and `encoding="utf-8"` for JSON files. |
| SQL string formatting | Quality | 21 | Percent formatting made the SQL construction harder to read and contributed to the injection risk. | Removed string interpolation completely by parameterizing the query. |
| Unused import and style issues | Style | 3, multiple | `os` was unused, function spacing was inconsistent, and `printStock` did not follow snake_case. | Removed the unused import, formatted functions, and renamed the function to `print_stock`. |

## Final Results

| Tool | Final result |
|---|---|
| Pylint | 10.00/10 |
| Bandit | No issues identified |
| Flake8 | No issues identified |
