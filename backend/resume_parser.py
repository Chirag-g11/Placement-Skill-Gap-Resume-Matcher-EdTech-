"""
resume_parser.py
Extracts raw text from uploaded resumes (PDF/DOCX/TXT) and runs
ATS-friendliness checks (contact info, sections present, action verbs,
resume length) — the kind of automated screening real ATS systems do
before a human ever sees the resume.
"""
import io
import re

import pdfplumber

from skills_db import ACTION_VERBS, RESUME_SECTION_KEYWORDS

try:
    import docx  # python-docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Dispatch to the right extractor based on file extension."""
    filename = (filename or "").lower()

    if filename.endswith(".pdf"):
        return _extract_from_pdf(file_bytes)
    elif filename.endswith(".docx") and DOCX_AVAILABLE:
        return _extract_from_docx(file_bytes)
    elif filename.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        # Best-effort fallback: try PDF first, then plain decode
        try:
            return _extract_from_pdf(file_bytes)
        except Exception:
            return file_bytes.decode("utf-8", errors="ignore")


def _extract_from_pdf(file_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n".join(text_parts)


def _extract_from_docx(file_bytes: bytes) -> str:
    document = docx.Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in document.paragraphs)


def check_contact_info(text: str) -> dict:
    email_found = bool(re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))
    phone_found = bool(re.search(r"(\+?\d{1,3}[-.\s]?)?\d{10}", text))
    linkedin_found = "linkedin.com" in text.lower() or "linkedin" in text.lower()
    github_found = "github.com" in text.lower() or "github" in text.lower()
    return {
        "email": email_found,
        "phone": phone_found,
        "linkedin": linkedin_found,
        "github": github_found,
    }


def check_sections(text: str) -> dict:
    lower = text.lower()
    found = {}
    for section, keywords in RESUME_SECTION_KEYWORDS.items():
        found[section] = any(kw in lower for kw in keywords)
    return found


def check_action_verbs(text: str) -> dict:
    lower = text.lower()
    used = sorted({v for v in ACTION_VERBS if re.search(r"\b" + re.escape(v) + r"\b", lower)})
    return {"count": len(used), "verbs_used": used, "total_available": len(ACTION_VERBS)}


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def run_ats_checks(text: str) -> dict:
    """
    Rule-based ATS friendliness audit — mirrors checks real ATS/parsers
    (like Workday, Greenhouse, Taleo) implicitly perform.
    """
    contact = check_contact_info(text)
    sections = check_sections(text)
    verbs = check_action_verbs(text)
    wc = word_count(text)

    checklist = []

    checklist.append({
        "check": "Email address present",
        "passed": contact["email"],
        "tip": "Add a professional email address near the top of your resume." if not contact["email"] else None,
    })
    checklist.append({
        "check": "Phone number present",
        "passed": contact["phone"],
        "tip": "Add a reachable phone number." if not contact["phone"] else None,
    })
    checklist.append({
        "check": "LinkedIn profile linked",
        "passed": contact["linkedin"],
        "tip": "Add your LinkedIn URL — recruiters check it 90%+ of the time." if not contact["linkedin"] else None,
    })
    checklist.append({
        "check": "GitHub / portfolio linked",
        "passed": contact["github"],
        "tip": "Add your GitHub/portfolio link, especially for tech roles." if not contact["github"] else None,
    })
    checklist.append({
        "check": "Education section detected",
        "passed": sections["Education"],
        "tip": "Include a clearly labeled Education section." if not sections["Education"] else None,
    })
    checklist.append({
        "check": "Skills section detected",
        "passed": sections["Skills"],
        "tip": "Add a dedicated Skills section — ATS bots weight this heavily." if not sections["Skills"] else None,
    })
    checklist.append({
        "check": "Projects/Experience section detected",
        "passed": sections["Projects"] or sections["Experience"],
        "tip": "Add a Projects or Experience section with measurable outcomes." if not (sections["Projects"] or sections["Experience"]) else None,
    })
    checklist.append({
        "check": "Uses strong action verbs",
        "passed": verbs["count"] >= 4,
        "tip": f"Only {verbs['count']} strong action verbs found (e.g. 'built', 'led', 'optimized'). Use more to sound impact-driven." if verbs["count"] < 4 else None,
    })
    checklist.append({
        "check": "Appropriate resume length",
        "passed": 150 <= wc <= 1100,
        "tip": ("Resume seems too short — add more detail on projects/impact." if wc < 150
                else "Resume may be too long for a 1-page ATS-friendly scan — trim to essentials." if wc > 1100 else None),
    })

    passed_count = sum(1 for c in checklist if c["passed"])
    ats_format_score = round((passed_count / len(checklist)) * 100)

    return {
        "ats_format_score": ats_format_score,
        "checklist": checklist,
        "word_count": wc,
        "action_verbs": verbs,
        "contact_info": contact,
        "sections_found": sections,
    }
