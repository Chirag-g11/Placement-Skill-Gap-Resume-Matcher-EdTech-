# GATECHECK — Placement Skill-Gap & Resume Matcher

**This version fixes the "two servers, two ports" confusion from before.**
Now there is **exactly one server and one URL**: Flask serves both the API
*and* the web page itself. No separate frontend file to open, no port
mismatches, no CORS issues.

---

## ▶️ How to run it (Windows)

1. Unzip this folder anywhere (e.g. `Desktop\gatecheck`).
2. Double-click **`RUN_ME.bat`**.
   - A terminal window opens, installs dependencies, and starts the server.
   - Wait until you see: `Running on http://127.0.0.1:5000`
3. Open your browser and go to: **http://127.0.0.1:5000**

That's it. Don't open any `.html` file directly — always go through that
`http://127.0.0.1:5000` URL in step 3, since that's what actually connects
you to the running server.

### Mac/Linux
```bash
./start.sh
```
then open **http://127.0.0.1:5000**

### Manual (any OS)
```bash
cd backend
pip install -r requirements.txt
python app.py
```
then open **http://127.0.0.1:5000**

---

## ⚠️ If it still doesn't load

**"This site can't be reached" / connection refused:**
The terminal window running `python app.py` must stay open the entire
time you're using the app. If you closed it, reopen it and run `python
app.py` (or `RUN_ME.bat`) again.

**Check the server is really up**, in a *second* terminal:
```powershell
curl http://127.0.0.1:5000/api/health
```
Should return `{"status": "ok", ...}`. If this fails, the server isn't
running — go back to the terminal and check for red error text.

**Port 5000 already in use:**
If you see an error like `Address already in use`, something else is
already running on that port. Find and stop it:
```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```
Then run `python app.py` again.

**Do not** open `backend/static/index.html` directly by double-clicking it
— it will not work on its own anymore, since it now expects to be served
by Flask itself so it can call the API on the same origin. Always go
through `http://127.0.0.1:5000` in the browser.

---

## ✨ What it does

1. Parses your resume (PDF/DOCX/TXT) and the target job description.
2. Extracts skills from both using a curated taxonomy of 100+ real
   tech/placement skills, with alias matching (`js` → `JavaScript`,
   `k8s` → `Kubernetes`, etc.).
3. Computes a **Match Score** — weighted blend of exact skill/keyword
   overlap (70%) and TF-IDF text similarity (30%).
4. Runs an **ATS Format Audit** — contact info, section headers, strong
   action verbs, resume length.
5. Generates a **personalized study roadmap** — every missing skill mapped
   to a real learning resource with a time estimate, prioritized and laid
   out week-by-week.
6. Combines everything into one **Placement Readiness Score**.

Click **"or load a sample resume + JD"** on the page for an instant demo
without needing your own files.

---

## 🏗️ Architecture

```
gatecheck/
├── RUN_ME.bat             # double-click to start on Windows
├── start.sh               # ./start.sh to start on Mac/Linux
├── backend/
│   ├── app.py              # Flask app — serves both the API AND the frontend page
│   ├── resume_parser.py    # PDF/DOCX/TXT extraction + ATS format checks
│   ├── matcher.py          # Skill extraction (taxonomy) + TF-IDF similarity scoring
│   ├── roadmap.py          # Priority-ranked, time-boxed learning roadmap generator
│   ├── skills_db.py        # Curated skill taxonomy + learning resource mapping
│   ├── requirements.txt
│   └── static/
│       └── index.html      # The web UI — served automatically by Flask at "/"
└── sample_data/            # Demo resume + JD for instant testing
```

---

## 🎯 How the scoring works (for judges' Q&A)

| Component | Weight | What it measures |
|---|---|---|
| Keyword/Skill Overlap | 70% of Match Score | `matched skills / total JD-required skills` |
| TF-IDF Text Similarity | 30% of Match Score | Cosine similarity of full resume vs. JD text |
| ATS Format Score | 25% of Overall Readiness | 9-point rule-based checklist |
| Match Score | 75% of Overall Readiness | The blended score above |

Missing skills are ranked by frequency of mention in the JD, so the
roadmap tackles the highest-impact gaps first.

No LLM API key is required for the core feature — everything runs on
deterministic NLP (`scikit-learn` TF-IDF + the curated taxonomy), which
is faster, more explainable, and won't break your demo if wifi is flaky.
