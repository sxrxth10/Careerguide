import streamlit as st
from utils.utils import generate_final_suggestion

def final_suggestion_page():
    """Streamlit UI for the final suggestion module."""
    st.title("Final Domain Suggestion")
    st.write("Based on your profile, aptitude tests, and quiz results, we'll suggest the best IT domains for you.")

    if st.button("Generate Final Suggestion"):
        if (
            "user_profiling" in st.session_state.module_conclusions
            and "logical_test" in st.session_state.module_conclusions
            and "numerical_test" in st.session_state.module_conclusions
            and "Quiz_based_analysis" in st.session_state.module_conclusions
        ):
            with st.spinner("Analyzing your data..."):
                result = generate_final_suggestion()
                if result:
                    # Store result in session state
                    st.session_state.module_conclusions["final_suggestion"] = result

                    # Display results
                    st.subheader("Your Career Path Recommendation")
                    st.write(f"**Conclusion**: {result['conclusion']}")
                    st.write("**Suggested Domains**:")
                    for domain in result["suggested_domains"]:
                        st.write(f"- {domain}")

                    # Option to download report
                    report = (
                        f"Final Career Recommendation\n\n"
                        f"Conclusion: {result['conclusion']}\n"
                        f"Suggested Domains: {', '.join(result['suggested_domains'])}\n"
                    )
                    st.download_button(
                        label="Download Recommendation",
                        data=report,
                        file_name="career_recommendation.txt",
                        mime="text/plain"
                    )
        else:
            st.warning("Please complete all modules (User Profile, Aptitude Tests, and Quiz) before generating the final suggestion.")