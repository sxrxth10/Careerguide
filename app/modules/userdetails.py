import streamlit as st
from utils.utils import analyze_with_llm

def userdetails():

    st.markdown("""
        <style>
        .st-aq {
            gap: 1rem;
            flex: auto;
            display: flex;
            justify-content: space-evenly;
        }
        </style>
    """, unsafe_allow_html=True)
    

    # Title of the app
    st.title("AI Career Guidance Form")

    # Create a form
    with st.form(key="career_form"):
        st.header("Personal Information")

        # Academic Details
        st.subheader("Academic Details")

        # 10th Grade
        st.write("10th Grade")
        fav_subjects_10th = st.text_input("Favorite 2 subjects in 10th (with reason)", placeholder="e.g., Math (love problem-solving), Science (curious about experiments)")
        marks_10th = st.text_input("Marks in 10th (% or GPA)", placeholder="e.g., 85% or 3.8 GPA")
        satisfaction_10th = st.slider("Satisfaction with 10th marks (1-5)", 1, 5, 3)
        least_liked_10th = st.text_input("Least liked subject in 10th (with reason)", placeholder="e.g., History (too much memorization)")

        # Higher Secondary (12th)
        st.write("Higher Secondary (12th)")
        stream_12th = st.text_input("Stream in higher secondary", placeholder="e.g., Science, Commerce, Arts")
        happy_stream = st.radio("Happy with stream choice?", ("Yes", "No"))
        happy_stream_reason = st.text_input("Why were you happy/unhappy with the stream?", placeholder="e.g., Loved the subjects / Felt forced into it")
        fav_subjects_12th = st.text_input("Favorite 2 subjects in 12th (with reason)", placeholder="e.g., Physics (enjoy mechanics), Chemistry (like experiments)")
        marks_12th = st.text_input("Marks in 12th (% or GPA)", placeholder="e.g., 90% or 4.0 GPA")
        satisfaction_12th = st.slider("Satisfaction with 12th marks (1-5)", 1, 5, 3)
        least_liked_12th = st.text_input("Least liked subject in 12th (with reason)", placeholder="e.g., Biology (disliked dissections)")

        # Undergraduation
        st.write("Undergraduation")
        ug_course = st.text_input("Undergraduation course/subject", placeholder="e.g., B.Tech in Computer Science")
        happy_ug = st.radio("Happy with undergrad choice?", ("Yes", "No"))
        happy_ug_reason = st.text_input("Why were you happy/unhappy with undergrad?", placeholder="e.g., Enjoyed coding / Too theoretical")
        fav_subjects_ug = st.text_input("Favorite 2 subjects in undergrad (with reason)", placeholder="e.g., Algorithms (logical), Databases (structured)")
        marks_ug = st.text_input("Marks in undergrad (% or GPA)", placeholder="e.g., 75% or 3.5 GPA")
        satisfaction_ug = st.slider("Satisfaction with undergrad marks (1-5)", 1, 5, 3)
        least_liked_ug = st.text_input("Least liked subject in undergrad (with reason)", placeholder="e.g., Networking (too complex)")

        # Extracurriculars & Hobbies
        st.subheader("Extracurriculars & Hobbies")
        hobbies = st.multiselect(
            "Hobbies (select all that apply)",
            options=["Coding", "Gaming", "Reading", "Art", "Sports", "Music", "Other"],
            default=[]
        )
        if "Other" in hobbies:
            other_hobby = st.text_input("Specify other hobby", placeholder="e.g., Photography")
        achievements = st.text_area("Activities/Achievements (Arts, Science, Sports)", placeholder="e.g., Won science fair, Captain of football team")
        tech_hobby = st.radio("Tech-related hobbies?", ("Yes", "No"))
        tech_hobby_explain = st.text_input("If yes, explain", placeholder="e.g., Built a small game in Python")

        # Previous Work Experiences
        st.header("Previous Work Experiences")
        work_exp = st.text_area("Any previous work experience? (Role, duration in months/years)", placeholder="e.g., Software Intern, 6 months")
        liked_job = st.radio("Did you like that job?", ("Yes", "No", "N/A"))
        liked_job_reason = st.text_input("Why did you like/dislike it?", placeholder="e.g., Loved the team / Repetitive tasks")
        reason_left = st.text_input("Why did you leave?", placeholder="e.g., Better opportunity / Contract ended")
        other_exp = st.text_area("Any other experiences?", placeholder="e.g., Freelance web design, 3 months")

        # Current Details
        st.header("Current Details")
        why_it = st.text_area("Why did you choose the IT field?", placeholder="e.g., Passion for tech, job prospects")
        good_at = st.text_input("A profession you believe you can be good at", placeholder="e.g., Data Analyst")
        no_salary_profession = st.text_input("A profession you’d choose even without salary", placeholder="e.g., Game Developer")
        long_term_goal = st.text_area("What is your long-term goal?", placeholder="e.g., Start my own tech company")

        # Submit Button
        submit_button = st.form_submit_button(label="Submit")

    # Process the form data after submission
    if submit_button:
        form_data = {
            "10th": {
                "fav_subjects": fav_subjects_10th,
                "marks": marks_10th,
                "satisfaction": satisfaction_10th,
                "least_liked": least_liked_10th
            },
            "12th": {
                "stream": stream_12th,
                "happy": happy_stream,
                "happy_reason": happy_stream_reason,
                "fav_subjects": fav_subjects_12th,
                "marks": marks_12th,
                "satisfaction": satisfaction_12th,
                "least_liked": least_liked_12th
            },
            "undergrad": {
                "course": ug_course,
                "happy": happy_ug,
                "happy_reason": happy_ug_reason,
                "fav_subjects": fav_subjects_ug,
                "marks": marks_ug,
                "satisfaction": satisfaction_ug,
                "least_liked": least_liked_ug
            },
            "extracurriculars": {
                "hobbies": hobbies + ([other_hobby] if "Other" in hobbies and other_hobby else []),
                "achievements": achievements,
                "tech_hobby": tech_hobby,
                "tech_hobby_explain": tech_hobby_explain
            },
            "work_experience": {
                "experience": work_exp,
                "liked_job": liked_job,
                "liked_reason": liked_job_reason,
                "reason_left": reason_left,
                "other_exp": other_exp
            },
            "current_details": {
                "why_it": why_it,
                "good_at": good_at,
                "no_salary_profession": no_salary_profession,
                "long_term_goal": long_term_goal
            }
        }

        if "module_conclusions" not in st.session_state:
            st.session_state.module_conclusions = {}

        # Analyze User Profiling module with LLM
        try:
            profiling_result = analyze_with_llm(form_data)
            st.session_state.module_conclusions["user_profiling"] = profiling_result
            st.success("Form submitted and analyzed successfully!")
            
            # Display User Profiling results (temporary, until all modules are added)
            st.subheader("User Profiling Analysis")
            st.write(f"**Conclusion**: {profiling_result['conclusion']}")
            st.write(f"**Suggested Domains**: {', '.join(profiling_result['suggested_domains'])}")
            
            # Placeholder for final synthesis (to be expanded later)
            st.info("This is the analysis for the User Profiling module. Once all modules are complete, a final recommendation will be provided.")

        except Exception as e:
            st.error(f"Error analyzing data with LLM: {str(e)}")