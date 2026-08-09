"""
skills_db.py
Curated taxonomy of tech/placement-relevant skills used for keyword
extraction, plus a mapping of each skill to learning resources used
to auto-generate personalized study roadmaps.

This is intentionally a plain Python data module (no external DB needed)
so the project runs anywhere with zero setup friction — perfect for a
hackathon demo.
"""

# ---------------------------------------------------------------------------
# 1. SKILL TAXONOMY
# Each category maps to a dict of {canonical_skill: [aliases...]}
# Canonical name is what gets displayed; aliases are how it might appear
# in resumes / job descriptions.
# ---------------------------------------------------------------------------

SKILL_TAXONOMY = {
    "Programming Languages": {
        "Python": ["python", "python3"],
        "Java": ["java"],
        "C++": ["c++", "cpp"],
        "C": ["c programming", " c "],
        "JavaScript": ["javascript", "js", "es6", "ecmascript"],
        "TypeScript": ["typescript", "ts"],
        "Go": ["golang", "go lang"],
        "Rust": ["rust"],
        "Kotlin": ["kotlin"],
        "Swift": ["swift"],
        "PHP": ["php"],
        "Ruby": ["ruby"],
        "R": ["r programming", "r language"],
        "SQL": ["sql", "structured query language"],
        "Scala": ["scala"],
        "C#": ["c#", "csharp", ".net"],
    },
    "Frontend": {
        "React": ["react", "react.js", "reactjs"],
        "Angular": ["angular", "angularjs"],
        "Vue.js": ["vue", "vue.js", "vuejs"],
        "HTML/CSS": ["html", "css", "html5", "css3"],
        "Tailwind CSS": ["tailwind", "tailwindcss"],
        "Bootstrap": ["bootstrap"],
        "Redux": ["redux"],
        "Next.js": ["next.js", "nextjs"],
        "Sass": ["sass", "scss"],
        "Webpack": ["webpack"],
    },
    "Backend": {
        "Node.js": ["node.js", "nodejs", "node js"],
        "Express.js": ["express", "express.js", "expressjs"],
        "Django": ["django"],
        "Flask": ["flask"],
        "FastAPI": ["fastapi"],
        "Spring Boot": ["spring boot", "spring framework", "springboot"],
        "REST API": ["rest api", "restful", "rest apis", "api development"],
        "GraphQL": ["graphql"],
        "Microservices": ["microservices", "microservice architecture"],
        ".NET Core": [".net core", "dotnet core", "asp.net"],
    },
    "Databases": {
        "MySQL": ["mysql"],
        "PostgreSQL": ["postgresql", "postgres"],
        "MongoDB": ["mongodb", "mongo"],
        "Redis": ["redis"],
        "SQLite": ["sqlite"],
        "Oracle DB": ["oracle db", "oracle database"],
        "Firebase": ["firebase", "firestore"],
        "Elasticsearch": ["elasticsearch", "elastic search"],
        "Cassandra": ["cassandra"],
    },
    "Cloud & DevOps": {
        "AWS": ["aws", "amazon web services", "ec2", "s3 bucket"],
        "Azure": ["azure", "microsoft azure"],
        "Google Cloud": ["gcp", "google cloud", "google cloud platform"],
        "Docker": ["docker", "containerization"],
        "Kubernetes": ["kubernetes", "k8s"],
        "CI/CD": ["ci/cd", "continuous integration", "continuous deployment", "jenkins"],
        "Git": ["git", "version control"],
        "GitHub Actions": ["github actions"],
        "Terraform": ["terraform", "infrastructure as code", "iac"],
        "Linux": ["linux", "unix", "bash scripting", "shell scripting"],
        "Nginx": ["nginx"],
    },
    "Data Science & ML": {
        "Machine Learning": ["machine learning", "ml"],
        "Deep Learning": ["deep learning", "neural networks", "dl"],
        "NLP": ["nlp", "natural language processing"],
        "Computer Vision": ["computer vision", "cv", "opencv"],
        "TensorFlow": ["tensorflow"],
        "PyTorch": ["pytorch"],
        "Scikit-learn": ["scikit-learn", "sklearn"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "Data Visualization": ["data visualization", "matplotlib", "seaborn", "power bi", "tableau"],
        "Data Structures & Algorithms": ["data structures", "algorithms", "dsa"],
        "Statistics": ["statistics", "statistical analysis"],
        "Big Data": ["big data", "hadoop", "spark", "pyspark"],
    },
    "Tools & Practices": {
        "Agile/Scrum": ["agile", "scrum", "sprint planning"],
        "JIRA": ["jira"],
        "Postman": ["postman", "api testing"],
        "Testing/QA": ["unit testing", "test automation", "selenium", "junit", "pytest", "jest"],
        "System Design": ["system design", "distributed systems", "scalability"],
        "OOP": ["oop", "object oriented programming", "object-oriented"],
        "Design Patterns": ["design patterns"],
        "Figma": ["figma", "ui/ux design", "wireframing"],
    },
    "Soft Skills": {
        "Communication": ["communication skills", "verbal communication"],
        "Teamwork": ["teamwork", "collaboration", "team player"],
        "Problem Solving": ["problem solving", "analytical skills", "critical thinking"],
        "Leadership": ["leadership", "team lead", "mentoring"],
        "Time Management": ["time management", "prioritization"],
    },
}

# Flattened lookup: alias(lowercase) -> (canonical_skill, category)
ALIAS_TO_SKILL = {}
for category, skills in SKILL_TAXONOMY.items():
    for canonical, aliases in skills.items():
        for alias in aliases + [canonical.lower()]:
            ALIAS_TO_SKILL[alias.strip().lower()] = (canonical, category)

# Sort aliases by length (desc) so multi-word phrases are matched before
# their substrings (e.g. "machine learning" before "learning").
SORTED_ALIASES = sorted(ALIAS_TO_SKILL.keys(), key=len, reverse=True)

# ---------------------------------------------------------------------------
# 2. LEARNING ROADMAP RESOURCES
# Maps each canonical skill -> curated resource + realistic time estimate.
# Used to build a personalized "bridge the gap" study plan.
# ---------------------------------------------------------------------------

LEARNING_RESOURCES = {
    "Python": {"resource": "Python Official Docs + CS50P (Harvard)", "time": "2 weeks", "difficulty": "Beginner"},
    "Java": {"resource": "Java Programming Masterclass / GeeksforGeeks Java", "time": "2 weeks", "difficulty": "Beginner"},
    "C++": {"resource": "Striver's C++ DSA Sheet", "time": "3 weeks", "difficulty": "Intermediate"},
    "SQL": {"resource": "SQLBolt + LeetCode SQL 50", "time": "1 week", "difficulty": "Beginner"},
    "JavaScript": {"resource": "JavaScript.info + freeCodeCamp", "time": "2 weeks", "difficulty": "Beginner"},
    "TypeScript": {"resource": "TypeScript Handbook (official)", "time": "1 week", "difficulty": "Intermediate"},
    "React": {"resource": "React Official Docs (react.dev) + build 2 projects", "time": "2 weeks", "difficulty": "Intermediate"},
    "Node.js": {"resource": "Node.js Docs + \"Node.js API Masterclass\"", "time": "2 weeks", "difficulty": "Intermediate"},
    "Express.js": {"resource": "Express.js official guide + REST API project", "time": "1 week", "difficulty": "Intermediate"},
    "Django": {"resource": "Django official tutorial (polls app) + DRF", "time": "2 weeks", "difficulty": "Intermediate"},
    "Flask": {"resource": "Flask Mega-Tutorial by Miguel Grinberg", "time": "1 week", "difficulty": "Beginner"},
    "FastAPI": {"resource": "FastAPI official docs (very hands-on)", "time": "1 week", "difficulty": "Intermediate"},
    "REST API": {"resource": "\"REST API Design Best Practices\" + build a CRUD API", "time": "1 week", "difficulty": "Beginner"},
    "GraphQL": {"resource": "How to GraphQL (howtographql.com)", "time": "1 week", "difficulty": "Intermediate"},
    "MySQL": {"resource": "MySQL Tutorial (W3Schools) + practice schema design", "time": "1 week", "difficulty": "Beginner"},
    "PostgreSQL": {"resource": "PostgreSQL Exercises (pgexercises.com)", "time": "1 week", "difficulty": "Beginner"},
    "MongoDB": {"resource": "MongoDB University M001 (free)", "time": "1 week", "difficulty": "Beginner"},
    "Redis": {"resource": "Redis University RU101", "time": "3 days", "difficulty": "Intermediate"},
    "AWS": {"resource": "AWS Cloud Practitioner Essentials (free tier labs)", "time": "3 weeks", "difficulty": "Intermediate"},
    "Azure": {"resource": "Microsoft Learn: Azure Fundamentals (AZ-900)", "time": "3 weeks", "difficulty": "Intermediate"},
    "Google Cloud": {"resource": "Google Cloud Skills Boost - Core Infrastructure", "time": "3 weeks", "difficulty": "Intermediate"},
    "Docker": {"resource": "Docker Official Get Started Guide + containerize a project", "time": "1 week", "difficulty": "Beginner"},
    "Kubernetes": {"resource": "Kubernetes Basics (kubernetes.io/docs/tutorials)", "time": "2 weeks", "difficulty": "Advanced"},
    "CI/CD": {"resource": "GitHub Actions docs + set up a pipeline", "time": "1 week", "difficulty": "Intermediate"},
    "Git": {"resource": "\"Git & GitHub Crash Course\" + practice branching/PRs", "time": "3 days", "difficulty": "Beginner"},
    "Terraform": {"resource": "HashiCorp Learn: Terraform Get Started", "time": "1 week", "difficulty": "Advanced"},
    "Linux": {"resource": "Linux Journey (linuxjourney.com)", "time": "1 week", "difficulty": "Beginner"},
    "Machine Learning": {"resource": "Andrew Ng's Machine Learning Specialization (Coursera)", "time": "4 weeks", "difficulty": "Intermediate"},
    "Deep Learning": {"resource": "deeplearning.ai Deep Learning Specialization", "time": "5 weeks", "difficulty": "Advanced"},
    "NLP": {"resource": "Hugging Face NLP Course (free)", "time": "3 weeks", "difficulty": "Advanced"},
    "Computer Vision": {"resource": "OpenCV Python Tutorials + PyImageSearch", "time": "3 weeks", "difficulty": "Advanced"},
    "TensorFlow": {"resource": "TensorFlow official \"Basics\" tutorials", "time": "2 weeks", "difficulty": "Intermediate"},
    "PyTorch": {"resource": "PyTorch official 60-minute blitz + build a CNN", "time": "2 weeks", "difficulty": "Intermediate"},
    "Pandas": {"resource": "Kaggle's \"Pandas\" micro-course (free)", "time": "3 days", "difficulty": "Beginner"},
    "NumPy": {"resource": "NumPy official quickstart", "time": "2 days", "difficulty": "Beginner"},
    "Data Structures & Algorithms": {"resource": "Striver's SDE Sheet / NeetCode 150", "time": "6 weeks", "difficulty": "Intermediate"},
    "Statistics": {"resource": "Khan Academy Statistics & Probability", "time": "2 weeks", "difficulty": "Beginner"},
    "Big Data": {"resource": "\"Big Data Analysis with Spark\" (edX)", "time": "3 weeks", "difficulty": "Advanced"},
    "System Design": {"resource": "\"System Design Primer\" (GitHub) + Grokking System Design", "time": "3 weeks", "difficulty": "Advanced"},
    "OOP": {"resource": "\"Object-Oriented Design\" course + refactor a project", "time": "1 week", "difficulty": "Beginner"},
    "Design Patterns": {"resource": "Refactoring.guru design patterns catalog", "time": "1 week", "difficulty": "Intermediate"},
    "Testing/QA": {"resource": "\"Test Automation University\" (free, by Applitools)", "time": "1 week", "difficulty": "Intermediate"},
    "Agile/Scrum": {"resource": "Scrum.org \"Learning Series\" (free)", "time": "3 days", "difficulty": "Beginner"},
    "JIRA": {"resource": "Atlassian JIRA official tutorials", "time": "2 days", "difficulty": "Beginner"},
    "Postman": {"resource": "Postman official \"API Fundamentals\" course", "time": "2 days", "difficulty": "Beginner"},
    "Figma": {"resource": "Figma official beginner tutorials", "time": "1 week", "difficulty": "Beginner"},
    "HTML/CSS": {"resource": "freeCodeCamp Responsive Web Design", "time": "2 weeks", "difficulty": "Beginner"},
    "Tailwind CSS": {"resource": "Tailwind CSS official docs + rebuild a UI", "time": "3 days", "difficulty": "Beginner"},
    "Next.js": {"resource": "Next.js official \"Learn\" course", "time": "1 week", "difficulty": "Intermediate"},
    "Microservices": {"resource": "\"Microservices.io\" patterns + sample project", "time": "2 weeks", "difficulty": "Advanced"},
    "Spring Boot": {"resource": "Spring Boot official guides + build a REST service", "time": "2 weeks", "difficulty": "Intermediate"},
    "Firebase": {"resource": "Firebase official \"Get Started\" docs", "time": "3 days", "difficulty": "Beginner"},
    "Communication": {"resource": "Practice via mock interviews + Toastmasters resources", "time": "Ongoing", "difficulty": "Soft Skill"},
    "Teamwork": {"resource": "Contribute to a team/open-source project", "time": "Ongoing", "difficulty": "Soft Skill"},
    "Problem Solving": {"resource": "Daily DSA practice on LeetCode/Codeforces", "time": "Ongoing", "difficulty": "Soft Skill"},
    "Leadership": {"resource": "Lead a college club/team project", "time": "Ongoing", "difficulty": "Soft Skill"},
    "Time Management": {"resource": "Follow a sprint-based personal planning system", "time": "Ongoing", "difficulty": "Soft Skill"},
}

# Fallback for any skill in taxonomy but missing a curated resource
DEFAULT_RESOURCE = {"resource": "Search official docs + a top-rated YouTube crash course", "time": "1-2 weeks", "difficulty": "Intermediate"}

# Strong action verbs recruiters / ATS parsers favor (used in resume ATS check)
ACTION_VERBS = [
    "built", "developed", "designed", "implemented", "led", "created",
    "optimized", "architected", "engineered", "launched", "automated",
    "improved", "reduced", "increased", "deployed", "managed", "spearheaded",
    "collaborated", "delivered", "streamlined", "resolved", "integrated",
    "migrated", "refactored", "mentored", "analyzed", "achieved",
]

RESUME_SECTION_KEYWORDS = {
    "Contact Info": ["email", "@", "phone", "linkedin", "github"],
    "Education": ["education", "b.tech", "university", "college", "degree", "cgpa", "gpa"],
    "Experience": ["experience", "internship", "worked", "intern"],
    "Projects": ["project", "projects"],
    "Skills": ["skills", "technical skills", "technologies"],
}
