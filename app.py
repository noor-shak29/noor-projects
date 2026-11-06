
import streamlit as st
import pandas as pd
from openai import OpenAI

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Career Path Advisor",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Career Path Advisor")

st.write(
    "Discover career opportunities, identify skill gaps, "
    "and build a personalized roadmap to prepare for internships."
)

st.divider()


# ==========================================
# 2. CAREER DATABASE
# ==========================================

Career_Database = {
    "Data Analyst": {
        "SQL", "Excel", "Python", "Statistics", "Data Visualization"
    },
    "Business Analyst": {
        "SQL", "Excel", "Requirements Analysis",
        "Communication", "Data Analysis"
    },
    "Business Intelligence Analyst": {
        "SQL", "Data Cleaning", "Power BI",
        "KPI Analysis", "Data Storytelling"
    },
    "Data Scientist": {
        "Python", "Data Cleaning", "EDA",
        "Machine Learning", "Model Evaluation"
    },
    "Product Analyst": {
        "SQL", "Product Metrics", "Funnel Analysis",
        "A/B Testing", "Data Visualization"
    },
    "Marketing Analyst": {
        "SQL", "Marketing KPIs", "Campaign Analysis",
        "Customer Segmentation", "Data Visualization"
    },
    "Financial Analyst": {
        "Excel/Financial Modeling",
        "Financial Statement Analysis",
        "Forecasting", "Financial KPIs",
        "Data Visualization"
    },
    "Project Manager": {
        "Project Planning", "Agile/Scrum",
        "Risk Management", "Stakeholder Management",
        "Project Tracking"
    },
    "IT Analyst": {
        "SQL", "Systems Analysis",
        "Requirements Gathering", "Process Mapping",
        "IT Troubleshooting"
    },
    "Cloud Analyst": {
        "Cloud Computing", "Networking",
        "Linux", "Security", "SQL"
    },
    "Cybersecurity Analyst": {
        "Log Analysis", "Threat Detection",
        "Vulnerability Assessment", "Incident Response",
        "Python/Scripting"
    },
    "Systems Analyst": {
        "Requirements Analysis", "Systems Design",
        "Process Mapping", "SQL/Database",
        "Testing & Documentation"
    }
}


# ==========================================
# 3. CAREER DEVELOPMENT RESOURCES
# ==========================================

Career_Resources = {
    "Data Analyst": {
        "Courses": [
            "Google Data Analytics Professional Certificate",
            "Microsoft Power BI learning paths"
        ],
        "Projects": [
            "Create a sales analytics dashboard",
            "Analyze customer purchasing trends"
        ],
        "Tools": ["Excel", "SQL", "Power BI", "Python"]
    },
    "Business Analyst": {
        "Courses": [
            "Business Analysis fundamentals",
            "SQL for Data Analysis"
        ],
        "Projects": [
            "Create a business performance dashboard",
            "Analyze a company's operational processes"
        ],
        "Tools": ["Excel", "SQL", "Power BI", "Jira"]
    },
    "Business Intelligence Analyst": {
        "Courses": [
            "Microsoft Power BI learning paths",
            "SQL for Business Intelligence"
        ],
        "Projects": [
            "Build an interactive KPI dashboard",
            "Create a business performance report"
        ],
        "Tools": ["SQL", "Power BI", "Excel", "Tableau"]
    },
    "Data Scientist": {
        "Courses": [
            "Python for Data Science",
            "Machine Learning fundamentals"
        ],
        "Projects": [
            "Build a predictive analytics model",
            "Perform exploratory data analysis"
        ],
        "Tools": ["Python", "SQL", "Jupyter", "Scikit-learn"]
    },
    "Product Analyst": {
        "Courses": [
            "SQL for Data Analysis",
            "Product Analytics fundamentals"
        ],
        "Projects": [
            "Analyze user engagement metrics",
            "Perform a simulated A/B test"
        ],
        "Tools": ["SQL", "Excel", "Tableau", "Python"]
    },
    "Marketing Analyst": {
        "Courses": [
            "Marketing Analytics",
            "Google Analytics learning resources"
        ],
        "Projects": [
            "Analyze a marketing campaign",
            "Create a customer segmentation report"
        ],
        "Tools": ["Excel", "SQL", "Power BI", "Google Analytics"]
    },
    "Financial Analyst": {
        "Courses": [
            "Financial Modeling fundamentals",
            "Excel for Financial Analysis"
        ],
        "Projects": [
            "Build a financial forecasting model",
            "Analyze financial statements"
        ],
        "Tools": ["Excel", "Power BI", "SQL"]
    },
    "Project Manager": {
        "Courses": [
            "Project Management fundamentals",
            "Agile and Scrum fundamentals"
        ],
        "Projects": [
            "Develop a project management plan",
            "Create a project tracking dashboard"
        ],
        "Tools": ["Jira", "Excel", "Trello", "Microsoft Project"]
    },
    "IT Analyst": {
        "Courses": [
            "IT fundamentals",
            "SQL and database fundamentals"
        ],
        "Projects": [
            "Document an IT business process",
            "Create a systems requirements document"
        ],
        "Tools": ["SQL", "Excel", "Jira", "Visio"]
    },
    "Cloud Analyst": {
        "Courses": [
            "AWS Cloud Practitioner learning resources",
            "Microsoft Azure fundamentals"
        ],
        "Projects": [
            "Create a cloud infrastructure diagram",
            "Document a cloud migration scenario"
        ],
        "Tools": ["AWS", "Azure", "Linux", "SQL"]
    },
    "Cybersecurity Analyst": {
        "Courses": [
            "Cybersecurity fundamentals",
            "CompTIA Security+ learning resources"
        ],
        "Projects": [
            "Analyze sample security logs",
            "Create an incident response report"
        ],
        "Tools": ["Linux", "Python", "Wireshark", "SIEM"]
    },
    "Systems Analyst": {
        "Courses": [
            "Systems analysis fundamentals",
            "Database and SQL fundamentals"
        ],
        "Projects": [
            "Create a system requirements document",
            "Develop a business process flowchart"
        ],
        "Tools": ["SQL", "Excel", "Visio", "Jira"]
    }
}


# ==========================================
# 4. HELPER FUNCTIONS
# ==========================================

def normalize_skills(skill_text):
    """Clean and standardize user-entered skills."""

    synonyms = {
        "microsoft excel": "excel",
        "ms excel": "excel",
        "powerbi": "power bi",
        "structured query language": "sql",
        "python programming": "python"
    }

    skills = set()

    for skill in skill_text.split(","):
        cleaned = skill.strip().lower()

        if cleaned:
            skills.add(synonyms.get(cleaned, cleaned))

    return skills


def analyze_skills(user_skills_input, dataset):

    user_set = normalize_skills(user_skills_input)
    results = []

    for career, required_skills in dataset.items():

        required_set = {s.lower() for s in required_skills}

        matching = user_set.intersection(required_set)
        missing = required_set.difference(user_set)

        score = (
            len(matching) / len(required_set) * 100
            if required_set else 0
        )

        results.append({
            "Career": career,
            "Match Score (%)": round(score, 1),
            "Matching Skills": ", ".join(sorted(matching)).title(),
            "Missing Skills": ", ".join(sorted(missing)).title()
        })

    return pd.DataFrame(results).sort_values(
        by="Match Score (%)",
        ascending=False
    )


def get_fallback_recommendations(career, missing_skills):
    """Provide recommendations when the AI API is unavailable."""

    resources = Career_Resources[career]

    recommendations = f"""
## Recommended Development Plan

### 1. Prioritize Your Skill Gaps

Focus on developing: {", ".join(sorted(missing_skills)) if missing_skills else "Continue strengthening your current skills."}

### 2. Recommended Courses

"""

    for course in resources["Courses"]:
        recommendations += f"- {course}\n"

    recommendations += "\n### 3. Portfolio Projects\n"

    for project in resources["Projects"]:
        recommendations += f"- {project}\n"

    recommendations += "\n### 4. Tools to Practice\n"
    recommendations += ", ".join(resources["Tools"])

    return recommendations


def generate_ai_recommendations(career, existing_skills, missing_skills):
    """Generate personalized recommendations using the OpenAI API."""

    try:
        api_key = st.secrets.get("OPENAI_API_KEY")

        if not api_key:
            return None

        client = OpenAI(api_key=api_key)

        prompt = f"""
You are a career development advisor helping students prepare
for internships.

Target career: {career}

Student's existing skills:
{", ".join(sorted(existing_skills)) if existing_skills else "None listed"}

Skills the student should develop:
{", ".join(sorted(missing_skills)) if missing_skills else "No listed skill gaps"}

Create a personalized internship preparation plan.

Include:

1. An assessment of the student's current preparation.
2. The three most important skills to prioritize.
3. Specific learning recommendations for each skill.
4. Two practical portfolio project ideas.
5. Relevant software and industry tools to practice.
6. A realistic four-week preparation roadmap.
7. Three internship interview questions to practice.

Make the recommendations practical, beginner-friendly, and
appropriate for a college student.

Do not claim the student has experience they did not list.
Do not guarantee internship eligibility or employment.
Use clear headings and bullet points.
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output_text

    except Exception as error:
        st.warning(
            "AI recommendations could not be generated. "
            "Showing standard recommendations instead."
        )
        return None


# ==========================================
# 5. CAREER MODE SELECTION
# ==========================================

st.header("Explore Your Career Goals")

career_mode = st.radio(
    "How can we help you?",
    [
        "Explore careers based on my existing skills",
        "I know my desired career and want to prepare for internships"
    ]
)


# ==========================================
# 6. MODE 1: CAREER EXPLORATION
# ==========================================

if career_mode == "Explore careers based on my existing skills":

    st.subheader("Discover Your Career Matches")

    user_skills = st.text_input(
        "Enter your current skills (separated by commas):",
        placeholder="Example: SQL, Excel, Python, Power BI"
    )

    if st.button("Find My Career Matches"):

        if user_skills.strip():

            results_df = analyze_skills(
                user_skills,
                Career_Database
            )

            st.subheader("Your Top 3 Career Matches")

            columns = st.columns(3)

            for i, (_, row) in enumerate(results_df.head(3).iterrows()):
                with columns[i]:
                    st.metric(
                        row["Career"],
                        f"{row['Match Score (%)']}%"
                    )

            st.subheader("All Career Matches")

            st.dataframe(
                results_df,
                use_container_width=True,
                hide_index=True
            )

            best_match = results_df.iloc[0]

            st.subheader("Recommended Skills to Develop")

            st.write(
                f"Based on your highest match, consider developing "
                f"these skills for **{best_match['Career']}**:"
            )

            st.write(
                best_match["Missing Skills"]
                if best_match["Missing Skills"]
                else "You listed all the skills in this career profile."
            )

            st.caption(
                "Note: Match scores represent skill overlap with this "
                "app's career database, not hiring probabilities."
            )

        else:
            st.warning("Please enter at least one skill.")


# ==========================================
# 7. MODE 2: INTERNSHIP PREPARATION
# ==========================================

elif career_mode == "I know my desired career and want to prepare for internships":

    st.subheader("Build Your Internship Preparation Plan")

    desired_career = st.selectbox(
        "Select your desired career:",
        list(Career_Database.keys())
    )

    current_skills = st.text_input(
        "Enter the skills you currently have:",
        placeholder="Example: Excel, SQL, Communication"
    )

    if st.button("Generate My Career Roadmap"):

        if current_skills.strip():

            required_skills = Career_Database[desired_career]

            user_set = normalize_skills(current_skills)

            required_set = {
                skill.lower() for skill in required_skills
            }

            matching = user_set.intersection(required_set)
            missing = required_set.difference(user_set)

            readiness = (
                len(matching) / len(required_set) * 100
            )

            # Save the roadmap in session state.
            # This prevents it from disappearing on reruns.

            st.session_state["roadmap"] = {
                "career": desired_career,
                "existing_skills": matching,
                "missing_skills": missing,
                "readiness": readiness
            }

            # Generate AI recommendations.

            with st.spinner("Generating your personalized recommendations..."):

                ai_recommendations = generate_ai_recommendations(
                    desired_career,
                    matching,
                    missing
                )

            if ai_recommendations:

                st.session_state["recommendations"] = ai_recommendations
                st.session_state["recommendation_type"] = "AI-generated"

            else:

                st.session_state["recommendations"] = (
                    get_fallback_recommendations(
                        desired_career,
                        missing
                    )
                )

                st.session_state["recommendation_type"] = "Standard"

        else:
            st.warning(
                "Please enter your current skills to generate your roadmap."
            )

    # ==========================================
    # 8. DISPLAY SAVED ROADMAP
    # ==========================================

    if "roadmap" in st.session_state:

        roadmap = st.session_state["roadmap"]

        # Only show the saved roadmap for the selected career.

        if roadmap["career"] == desired_career:

            career = roadmap["career"]
            matching = roadmap["existing_skills"]
            missing = roadmap["missing_skills"]
            readiness = roadmap["readiness"]

            st.success(f"Your selected career: {career}")

            st.subheader("Your Internship Skill Assessment")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Skill Match",
                f"{readiness:.1f}%"
            )

            col2.metric(
                "Matching Skills",
                len(matching)
            )

            col3.metric(
                "Skills to Develop",
                len(missing)
            )

            st.progress(int(readiness))

            # Existing skills

            st.subheader("1. Your Existing Skills")

            if matching:
                st.write(", ".join(sorted(matching)).title())
            else:
                st.info("Start by building foundational skills.")

            # Missing skills

            st.subheader("2. Skills You Should Develop")

            if missing:
                for skill in sorted(missing):
                    st.write(f"- {skill.title()}")
            else:
                st.success(
                    "You listed all the skills in this career profile!"
                )

            # AI recommendations

            st.divider()

            st.subheader("3. Personalized Career Recommendations")

            recommendation_type = st.session_state.get(
                "recommendation_type",
                "Standard"
            )

            if recommendation_type == "AI-generated":
                st.caption("Personalized recommendations generated using AI.")
            else:
                st.caption(
                    "Standard recommendations. Add your OpenAI API key "
                    "to enable AI-generated personalization."
                )

            st.markdown(
                st.session_state.get("recommendations", "")
            )

            # ==========================================
            # 9. INTERACTIVE PROGRESS TRACKER
            # ==========================================

            st.divider()

            st.subheader("4. Track Your Career Preparation")

            st.write(
                "Complete each task as you prepare for your internship. "
                "Your progress will update automatically."
            )

            tasks = [
                "Identify my missing skills",
                "Complete relevant courses",
                "Practice industry-standard tools",
                "Complete at least one portfolio project",
                "Update my resume",
                "Practice internship interview questions",
                "Apply for relevant internships"
            ]

            # Use stable keys tied to the selected career.

            progress_keys = [
                f"progress_{career}_{i}"
                for i in range(len(tasks))
            ]

            if st.button("Reset My Progress"):
                for key in progress_keys:
                    if key in st.session_state:
                        del st.session_state[key]

                st.rerun()

            completed = 0

            for i, task in enumerate(tasks):

                is_completed = st.checkbox(
                    task,
                    key=progress_keys[i]
                )

                if is_completed:
                    completed += 1

            total_tasks = len(tasks)

            progress_percentage = completed / total_tasks

            st.progress(progress_percentage)

            col1, col2 = st.columns(2)

            col1.metric(
                "Tasks Completed",
                f"{completed}/{total_tasks}"
            )

            col2.metric(
                "Overall Progress",
                f"{progress_percentage * 100:.0f}%"
            )

            if completed == total_tasks:
                st.success(
                    "Congratulations! You completed your preparation checklist."
                )


# ==========================================
# 10. FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Career Path Advisor | Explore Careers. "
    "Develop Skills. Prepare for Opportunities."
)
