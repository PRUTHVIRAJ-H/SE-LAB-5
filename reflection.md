# Lab 5: Reflection

**Student:** Pruthviraj H  
**SRN:** PES2UG24CS381

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest issues were the unused import, spacing, naming, and line-length warnings because they only required small formatting or cleanup changes. The hardest issue was the SQL injection risk because it required understanding parameterized SQL and changing the query without changing the program's result.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

There were no important false positives in this analysis. The Bandit SQL warning was reported with low confidence, but it was still a valid concern because the code directly inserted a user-provided name into the SQL query. The fix improved the code even though the sample inputs were harmless.

## 3. How would you integrate static analysis tools into your actual software development workflow?

I would run Flake8 and Pylint locally before committing code, and run Bandit as part of the continuous integration pipeline. The pipeline could fail for high-severity security findings and important style or quality errors, while still allowing review of lower-priority warnings.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The code became easier to read through clear function names, docstrings, consistent formatting, and context managers. It became more robust through specific exceptions and removal of the mutable default argument, and safer through the parameterized query. Pylint improved from 6.90/10 to 10.00/10, with no Bandit or Flake8 findings.
