# livetest.py
import streamlit as st
from utils.utils import select_questions, analyze_iq_response

# Initialize session state variables
def initilize_logical_test():
    if 'logical_test' not in st.session_state:
        st.session_state.logical_test = {
            "started": False,
            "completed": False,
            "questions": [],
            "responses": {"q1": "", "q2": "", "q3": ""}
        }
    if 'module_conclusions' not in st.session_state:
        st.session_state.module_conclusions = {}

def initilize_numerical_test():
    if 'numerical_test' not in st.session_state:
        st.session_state.numerical_test = {
            "started": False,
            "completed": False,
            "questions": [],
            "responses": {"q1": "", "q2": "", "q3": ""}
        }
    if 'module_conclusions' not in st.session_state:
        st.session_state.module_conclusions = {}




def start_test(test_type):
    """Start the Logical IQ test."""
    st.session_state[test_type]["started"] = True
    st.session_state[test_type]["completed"] = False
    st.session_state[test_type]["questions"] = select_questions(test_type)
    st.session_state[test_type]["responses"] = {"q1": "", "q2": "", "q3": ""}

def submit_test(test_type):
    """End the test and process the responses."""
    if st.session_state[test_type]["started"] and not st.session_state[test_type]["completed"]:
        responses = st.session_state[test_type]["responses"]
        if all(responses[key].strip() for key in responses):
            st.session_state[test_type]["completed"] = True
            # Prepare question-response pairs for LLM
            question_response_pairs = {
                q["question"]: responses[f"q{i+1}"]
                for i, q in enumerate(st.session_state[test_type]["questions"])
            }
            analysis = analyze_iq_response(question_response_pairs)
            st.session_state.module_conclusions[test_type] = {
                "questions_responses": [
                    {"question": q["question"], "response": responses[f"q{i+1}"]}
                    for i, q in enumerate(st.session_state[test_type]["questions"])
                ],
                "summary": analysis
            }
        else:
            st.warning("Please provide answers for all questions.")

def restart_test(test_type):
    """Reset the test to initial state."""
    st.session_state[test_type] = {
        "started": False,
        "completed": False,
        "questions": [],
        "responses": {"q1": "", "q2": "", "q3": ""}
    }

def live_test():
    tab1, tab2 = st.tabs(["IQ - Logical", "IQ - Numerical"])

    with tab1:
        initilize_logical_test()
        if not st.session_state["logical_test"]["started"]:
            st.markdown("""
            ## Logical IQ Test
            
            This test evaluates your logical reasoning ability. You will be presented with three logical questions to solve.
            
            **Instructions**:
            1. Click "Start Test" to begin.
            2. Type your answer and reasoning for each question.
            3. Click "Submit" when you've completed all responses.
            
            **Note**: Your responses will be analyzed to evaluate your performance.
            """)
            st.button("Start Test", key="start_logical_test", on_click=start_test, args=("logical_test",), use_container_width=True)
        
        elif st.session_state.logical_test["started"] and not st.session_state.logical_test["completed"]:
            st.subheader("Questions")
            for i, question in enumerate(st.session_state.logical_test["questions"], 1):
                st.markdown(f"""
                ### {i}. {question['question']}
                """)  # Fixed: Use question['question'] instead of question[i]
                st.session_state.logical_test["responses"][f"q{i}"] = st.text_area(
                    "Your Answer",
                    value=st.session_state.logical_test["responses"][f"q{i}"],
                    height=200,
                    key=f"logical_q{i}",
                    placeholder="Enter your answer and explain your reasoning here..."
                )
            st.button("Submit Answers", key="submit_logical_test", on_click=submit_test, args=("logical_test",), use_container_width=True)
        
        else:
            st.success("Logical Test completed! Your responses have been recorded.")
            st.subheader("Your Responses")
            for item in st.session_state.module_conclusions["logical_test"]["questions_responses"]:
                st.write(f"**Question**: {item['question']}")
                st.write(f"**Answer**: {item['response']}")
            # st.subheader("Analysis")
            # st.write(f"**Conclusion**: {st.session_state.module_conclusions['logical_test']['summary']}")
            # st.subheader("Stored Module Conclusions")
            # st.json(st.session_state.module_conclusions)
            st.markdown("""
            ### Test Information
            
            Your responses have been recorded and analyzed. You can take another test if desired.
            """)
            st.button("Take Another Test", key="restart_logical_test", on_click=restart_test, args=("logical_test",), use_container_width=True)

    with tab2:
        initilize_numerical_test()
        if not st.session_state.numerical_test["started"]:
            st.markdown("""
            ## Numerical IQ Test
            
            This test evaluates your Numerical reasoning ability. You will be presented with three Numerical questions to solve.
            
            **Instructions**:
            1. Click "Start Test" to begin.
            2. Type your answer and reasoning for each question.
            3. Click "Submit" when you've completed all responses.
            
            **Note**: Your responses will be analyzed to evaluate your performance.
            """)
            st.button("Start Test", key="start_numerical_test", on_click=start_test, args=("numerical_test",), use_container_width=True)
        
        elif st.session_state.numerical_test["started"] and not st.session_state.numerical_test["completed"]:
            st.subheader("Questions")
            for i, question in enumerate(st.session_state.numerical_test["questions"], 1):
                st.markdown(f"""
                ### {i}. {question['question']}
                """)  # Fixed: Use question['question'] instead of question[i]
                st.session_state.numerical_test["responses"][f"q{i}"] = st.text_area(
                    "Your Answer",
                    value=st.session_state.numerical_test["responses"][f"q{i}"],
                    height=200,
                    key=f"numerical_q{i}", 
                    placeholder="Enter your answer and explain your reasoning here..."
                )
            st.button("Submit Answers", key="submit_numerical_test", on_click=submit_test, args=("numerical_test",), use_container_width=True)
        
        else:
            st.success("Numerical Test completed! Your responses have been recorded.")
            st.subheader("Your Responses")
            for item in st.session_state.module_conclusions["numerical_test"]["questions_responses"]:
                st.write(f"**Question**: {item['question']}")
                st.write(f"**Answer**: {item['response']}")
            st.subheader("Analysis")
            st.write(f"**Conclusion**: {st.session_state.module_conclusions['numerical_test']['summary']}")
            st.subheader("Stored Module Conclusions")
            st.json(st.session_state.module_conclusions)
            st.markdown("""
            ### Test Information
            
            Your responses have been recorded and analyzed. You can take another test if desired.
            """)
            st.button("Take Another Test", key="restart_numerical_test", on_click=restart_test, args=("numerical_test",), use_container_width=True)
