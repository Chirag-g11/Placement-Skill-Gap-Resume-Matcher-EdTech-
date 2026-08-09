"""
matcher.py
Core NLP engine: extracts canonical skills from raw text against the
curated taxonomy, and computes an overall resume<->JD match score using
a blend of (a) keyword/skill overlap and (b) TF-IDF cosine similarity
over the full text (captures phrasing/context beyond exact keywords).
"""
import re
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills_db import SORTED_ALIASES, ALIAS_TO_SKILL, SKILL_TAXONOMY


def _normalize(text: str) -> str:
    text = text.lower()
    # keep alphanumerics, +, #, ., / and spaces (so c++, node.js, ci/cd survive)
    text = re.sub(r"[^a-z0-9+#./\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return f" {text} "  # pad for whole-word boundary matching


def extract_skills(text: str):
    """
    Returns:
        skills_found: dict[category] -> set(canonical skill names)
        flat_set: set of all canonical skills found
        frequency: Counter of canonical skill -> occurrence count (signals importance in JD)
    """
    norm = _normalize(text)
    flat_set = set()
    frequency = Counter()
    skills_found = {cat: set() for cat in SKILL_TAXONOMY}

    for alias in SORTED_ALIASES:
        pattern = r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])"
        matches = re.findall(pattern, norm)
        if matches:
            canonical, category = ALIAS_TO_SKILL[alias]
            flat_set.add(canonical)
            skills_found[category].add(canonical)
            frequency[canonical] += len(matches)

    return skills_found, flat_set, frequency


def compute_text_similarity(resume_text: str, jd_text: str) -> float:
    """TF-IDF + cosine similarity between full resume and JD text (0-100)."""
    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=2000)
        tfidf = vectorizer.fit_transform([resume_text, jd_text])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return round(float(sim) * 100, 1)
    except Exception:
        return 0.0


def analyze(resume_text: str, jd_text: str) -> dict:
    resume_categories, resume_skills, _ = extract_skills(resume_text)
    jd_categories, jd_skills, jd_frequency = extract_skills(jd_text)

    matched_skills = sorted(resume_skills & jd_skills)
    missing_skills = sorted(jd_skills - resume_skills)
    extra_skills = sorted(resume_skills - jd_skills)  # skills candidate has beyond the JD

    # Keyword overlap score: how many of the JD's required skills does the resume cover
    if jd_skills:
        keyword_score = round((len(matched_skills) / len(jd_skills)) * 100, 1)
    else:
        keyword_score = 0.0

    text_sim_score = compute_text_similarity(resume_text, jd_text)

    # Weighted final match score: skill-overlap is the strongest signal for
    # ATS-style matching, text similarity adds context awareness.
    final_score = round((keyword_score * 0.7) + (text_sim_score * 0.3), 1)
    final_score = max(0.0, min(100.0, final_score))

    # Priority for missing skills = how often they appear in the JD (more
    # mentions => recruiter cares more => higher priority to learn first)
    missing_with_priority = sorted(
        missing_skills, key=lambda s: jd_frequency.get(s, 0), reverse=True
    )

    # Per-category breakdown for the frontend radar/bars
    category_breakdown = {}
    for cat in SKILL_TAXONOMY:
        jd_cat_skills = jd_categories.get(cat, set())
        res_cat_skills = resume_categories.get(cat, set())
        if jd_cat_skills:
            cat_score = round((len(jd_cat_skills & res_cat_skills) / len(jd_cat_skills)) * 100)
        else:
            cat_score = None  # JD doesn't require anything from this category
        category_breakdown[cat] = {
            "score": cat_score,
            "matched": sorted(jd_cat_skills & res_cat_skills),
            "missing": sorted(jd_cat_skills - res_cat_skills),
        }

    return {
        "final_match_score": final_score,
        "keyword_overlap_score": keyword_score,
        "text_similarity_score": text_sim_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_with_priority,
        "extra_skills": extra_skills,
        "jd_skill_count": len(jd_skills),
        "resume_skill_count": len(resume_skills),
        "category_breakdown": category_breakdown,
    }
