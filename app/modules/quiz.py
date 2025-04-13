import streamlit as st
from utils.utils import get_quiz_data, calculate_scores, get_top_3_domains_from_quiz

def quiz():
    # Streamlit UI
    st.title("IT Career Interest Quiz")
    st.write("Answer the following questions to discover which IT field matches your interests! Choose one option for each question.")

    quiz_data = get_quiz_data()
    # Form to collect responses
    with st.form(key="quiz_form"):
        responses = {}
        
        # Display questions by domain
        for domain, questions in quiz_data.items():
            st.subheader(domain)
            for idx, question in enumerate(questions):
                # Unique key for each radio button
                response = st.radio(
                    question,
                    ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"],
                    key=f"{domain}_{idx}",
                    index=2  # Default to Neutral
                )
                responses[(domain, idx)] = response
        
        # Submit button
        submit_button = st.form_submit_button(label="Submit Quiz")

    # Calculate and display results after submission
    if submit_button:
        if "module_conclusions" not in st.session_state:
            st.session_state.module_conclusions = {}

        top_3 = get_top_3_domains_from_quiz(scores)
        st.session_state.module_conclusions["Quiz_based_analysis"] = [{"domain": domain, "score": score} for domain, score in top_3]

        st.success("Quiz submitted! Here are your results:")
        scores = calculate_scores(responses)
        
        # # Display scores
        # st.write("### Your Scores by Domain")
        # for domain, score in scores.items():
        #     st.write(f"**{domain}**: {score} points")
        
        # # Optional: Highlight top domain
        # if scores:
        #     max_score = max(scores.values())
        #     top_domains = [domain for domain, score in scores.items() if score == max_score]
        #     st.write("### Your Top Interest(s)")
        #     for domain in top_domains:
        #         st.write(f"You seem most interested in **{domain}** with a score of {max_score} points!")
