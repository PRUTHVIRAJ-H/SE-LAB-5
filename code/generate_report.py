"""Generate the Lab 5 static-analysis submission PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).parent.parent
REPORT_ROOT = ROOT / "issues"
OUTPUT = ROOT / "Lab5_Static_Code_Analysis_Pruthviraj_H.pdf"


def paragraph(text, style):
    """Create a paragraph with simple Markdown-style emphasis removed."""
    return Paragraph(text.replace("**", ""), style)


def build_report():
    """Build the final student-friendly PDF report."""
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "ReportTitle", parent=styles["Title"], alignment=TA_CENTER,
        fontSize=20, leading=24, textColor=colors.HexColor("#17365D"),
    )
    heading = ParagraphStyle(
        "ReportHeading", parent=styles["Heading2"], spaceBefore=10,
        spaceAfter=6, textColor=colors.HexColor("#17365D"),
    )
    body = ParagraphStyle(
        "ReportBody", parent=styles["BodyText"], fontSize=9.5,
        leading=13, spaceAfter=6,
    )
    small = ParagraphStyle(
        "ReportSmall", parent=body, fontSize=8, leading=10,
    )
    code = ParagraphStyle(
        "ReportCode", parent=styles["Code"], fontName="Courier",
        fontSize=7.2, leading=9,
    )

    story = [
        Paragraph("Lab 5: Static Code Analysis", title),
        Spacer(1, 8),
        paragraph("<b>Student:</b> Pruthviraj H", body),
        paragraph("<b>SRN:</b> PES2UG24CS381", body),
        paragraph("<b>Program:</b> pharmacy_system.py", body),
        Spacer(1, 10),
        paragraph(
            "This report documents the use of Pylint, Bandit, and Flake8 to improve "
            "the quality, security, and style of a small pharmacy stock tracker.",
            body,
        ),
        Paragraph("Issue Table", heading),
    ]

    rows = [
        ["Issue", "Type", "Line(s)", "Description", "Fix approach"],
        ["SQL injection risk", "Security", "21", "User input was joined directly into an SQL query.", "Used a parameterized query."],
        ["Mutable default argument", "Bug", "24", "A default list was shared across calls.", "Used None and created a new list."],
        ["Bare exceptions", "Reliability", "38, 58", "Errors were hidden by bare except blocks.", "Caught only expected exception types."],
        ["Unsafe file handling", "Quality", "50, 57", "Files lacked context managers and encoding.", "Used with blocks and UTF-8 encoding."],
        ["Style and unused import", "Style", "3, multiple", "Unused os import and naming/spacing issues.", "Removed, renamed, and formatted code."],
    ]
    table_data = []
    for row in rows:
        table_data.append([paragraph(cell, small) for cell in row])
    issue_table = Table(table_data, colWidths=[29 * mm, 22 * mm, 18 * mm, 48 * mm, 52 * mm], repeatRows=1)
    issue_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9AAABD")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F3F6F9")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F6F9")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.extend([issue_table, Spacer(1, 10), Paragraph("Final Results", heading)])
    result_table = Table([
        [paragraph("Tool", small), paragraph("Result", small)],
        [paragraph("Pylint", small), paragraph("10.00/10", small)],
        [paragraph("Bandit", small), paragraph("No issues identified", small)],
        [paragraph("Flake8", small), paragraph("No issues identified", small)],
    ], colWidths=[45 * mm, 124 * mm], repeatRows=1)
    result_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9AAABD")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F6F9")]),
    ]))
    story.extend([result_table, PageBreak(), Paragraph("Reflection", title), Spacer(1, 8)])
    reflections = [
        ("1. Which issues were the easiest to fix, and which were the hardest? Why?", "The easiest issues were the unused import, spacing, naming, and line-length warnings because they only required small formatting or cleanup changes. The hardest issue was the SQL injection risk because it required understanding parameterized SQL and changing the query without changing the program's result."),
        ("2. Did the static analysis tools report any false positives? If so, describe one example.", "There were no important false positives in this analysis. The Bandit SQL warning was reported with low confidence, but it was still a valid concern because the code directly inserted a user-provided name into the SQL query. The fix improved the code even though the sample inputs were harmless."),
        ("3. How would you integrate static analysis tools into your actual software development workflow?", "I would run Flake8 and Pylint locally before committing code, and run Bandit as part of the continuous integration pipeline. The pipeline could fail for high-severity security findings and important style or quality errors, while still allowing review of lower-priority warnings."),
        ("4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?", "The code became easier to read through clear function names, docstrings, consistent formatting, and context managers. It became more robust through specific exceptions and removal of the mutable default argument, and safer through the parameterized query. Pylint improved from 6.90/10 to 10.00/10, with no Bandit or Flake8 findings."),
    ]
    for question, answer in reflections:
        story.append(Paragraph(question, heading))
        story.append(paragraph(answer, body))
    story.extend([PageBreak(), Paragraph("Analyzer Output", title), Spacer(1, 8)])
    for name in ("pylint_report.txt", "bandit_report.txt", "flake8_report.txt"):
        story.append(Paragraph(name, heading))
        report = (REPORT_ROOT / name).read_text(encoding="utf-8")
        story.append(Preformatted(report or "No findings.", code))
        story.append(Spacer(1, 8))

    SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=15 * mm, leftMargin=15 * mm,
        topMargin=15 * mm, bottomMargin=15 * mm,
        title="Lab 5 Static Code Analysis - Pruthviraj H",
    ).build(story)


if __name__ == "__main__":
    build_report()