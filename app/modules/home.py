import streamlit as st

def home_page():
    """Streamlit home page with instructions for the career guidance app."""
    st.title("Welcome to CareerPath IT")
    st.subheader("Find Your Ideal IT Career Path")
    
    st.write("""
    CareerPath IT is designed to help you discover the best IT domain for your skills and interests, 
    even if you're new to tech. Through a series of steps, we'll collect your details, test your 
    abilities, and analyze your preferences to recommend a career path like Software Testing, 
    Web Development, AI/ML, or more.
    """)

    st.markdown("### How It Works")
    st.write("""
    You'll complete five modules in order. Each step builds on the previous one to create a 
    personalized recommendation. Use the sidebar to navigate to each module when you're ready. 
    Please complete them in sequence for the best results.
    """)

    # Module Instructions
    with st.expander("Step 1: User Details Collection", expanded=True):
        st.write("""
        **What to Expect**: Share basic information about yourself, like your background, 
        education, and interests. This helps us understand your starting point.
        - **Why**: Tailors suggestions to your unique profile.
        - **How**: Fill out a simple form with details like name, experience, and goals.
        - **Navigation**: Select *User Details* from the sidebar to start.
        """)

    with st.expander("Step 2: Aptitude Test - Logical Test"):
        st.write("""
        **What to Expect**: Answer questions that test your reasoning and problem-solving skills, 
        like puzzles or pattern recognition.
        - **Why**: Measures your logical thinking, key for domains like Game Development or Cybersecurity.
        - **How**: Solve a set of multiple-choice questions. Take your time to think through each one.
        - **Navigation**: After completing User Details, select *Logical Test* from the sidebar.
        """)

    with st.expander("Step 3: Aptitude Test - Numerical Test"):
        st.write("""
        **What to Expect**: Solve problems involving numbers, calculations, or data interpretation.
        - **Why**: Assesses your numerical ability, important for fields like AI/ML or DevOps.
        - **How**: Answer a series of math-based questions. A calculator is optional but not required.
        - **Navigation**: After Logical Test, select *Numerical Test* from the sidebar.
        """)

    with st.expander("Step 4: Quiz-Based Data Collection Analysis"):
        st.write("""
        **What to Expect**: Take a quiz to gauge your interests in various IT domains, like 
        designing apps or securing systems.
        - **Why**: Identifies which tech areas excite you most, ensuring a good fit.
        - **How**: Respond to statements with options like Agree, Neutral, or Disagree. Be honest!
        - **Navigation**: After Numerical Test, select *Quiz* from the sidebar.
        """)

    with st.expander("Step 5: Detailed Suggestion"):
        st.write("""
        **What to Expect**: Receive a personalized recommendation of three IT domains best suited 
        for you, with an explanation of why they fit.
        - **Why**: Combines all your inputs—details, aptitude, and interests—for a clear career path.
        - **How**: View your results, including a conclusion and suggested domains like UI/UX or Mobile Development.
        - **Navigation**: After Quiz, select *Final Suggestion* from the sidebar.
        """)

    # Optional: Mention ML Classifier (Self-Assessment)
    with st.expander("Optional: Self-Assessment (Rate Your Qualities)", expanded=False):
        st.write("""
        **What to Expect**: Rate yourself on qualities like creativity or problem-solving to get 
        an additional domain suggestion.
        - **Why**: Offers another perspective on your strengths, especially if you're unsure about your skills.
        - **How**: Use sliders to score yourself from 1 to 10 on 10 qualities. Takes just a minute!
        - **Navigation**: Select *Self-Assessment* from the sidebar at any time, but we recommend doing it before Final Suggestion.
        """)

    st.markdown("### Get Started")
    st.write("""
    Ready to explore your IT career path? Start with *User Details* in the sidebar. 
    Complete each module in order, and by the end, you'll have a clear direction for your tech journey!
    """)
    
    # Optional: Progress Indicator
    if "module_conclusions" in st.session_state:
        completed = len(st.session_state.module_conclusions)
        st.progress(min(completed / 5, 1.0))
        st.write(f"Progress: {completed}/5 modules completed")
