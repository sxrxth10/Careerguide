import openai
from dotenv import load_dotenv
import streamlit as st
import logging
import os
import random

logging.basicConfig(level=logging.DEBUG)

load_dotenv()
openai_api_key1 = os.getenv("OPENAI_API_KEY1")
client = openai.OpenAI(api_key=openai_api_key1)



def analyze_with_llm(form_data):
    # Convert form data to a readable string for the LLM
    prompt = "Analyze the following user data and suggest 3 tech domains (e.g., Full Stack, Data Science, Machine Learning, Cybersecurity, Flutter, .NET) that suit them best. Provide a short conclusion explaining your reasoning. The response should just the overall conclusion and the suggested domains.\n\n"
    prompt += "User Data:\n"
    for section, details in form_data.items():
        prompt += f"{section.capitalize()}:\n"
        for key, value in details.items():
            prompt += f"  {key.replace('_', ' ').capitalize()}: {value}\n"
        prompt += "\n"
    prompt += "Return your response in this format:\n"
    prompt += "Conclusion: [Your conclusion here]\n"
    prompt += "Suggested Domains: [Domain 1], [Domain 2], [Domain 3]"

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI career advisor specializing in tech domains."},
            {"role": "user", "content": prompt}
        ],
    )

    # Extract the response
    result_text = response.choices[0].message.content.strip()
    
    # Parse the conclusion and domains
    conclusion = result_text.split("Conclusion:")[1].split("Suggested Domains:")[0].strip()
    domains = result_text.split("Suggested Domains:")[1].strip().split(", ")
    domains = [d.strip("[]") for d in domains]  # Clean up brackets

    return {
        "conclusion": conclusion,
        "suggested_domains": domains
    }




def analyze_iq_response(question_with_response):
    """Analyze Logical IQ test responses for clarity and correctness."""
    prompt = """
    You are an expert career assistant who valuates a candidates IQ by conducting tests.

    Analyze the following Logical IQ test responses to evaluate logical reasoning, problem-solving, and pattern recognition. Analyze the candidate's answers to these questions and provide a concise conclusion that includes:

    1. **Performance Summary**  Briefly describe how well the candidate performed.
    2. **Estimated IQ Level**  Use simple labels like "Below Average", "Average", "Above Average", or "High".
    3. **Cognitive Strengths**  Highlight any noticeable strengths (e.g., analytical thinking, abstract reasoning).
    4. **Remarks**  Any other necessary observations to record or save, that may assist in making a valuation in the future.

    Keep the summary short (3-5 sentences), objective, and suitable for storing in a database.

    """
    for i, (question, response) in enumerate(question_with_response.items(), 1):
        prompt += f"Question {i}: {question}\n"
        prompt += f"Response {i}: {response}\n\n"
    prompt += "Format exactly as Summary: [Your summary here], Mark: [Score out of 10]"

    try:
        response =client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI evaluator specializing in logical reasoning assessments."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        result_text = response.choices[0].message.content.strip()

        return result_text
    
    except Exception as e:
        return f"Error analyzing response: {str(e)}"

import random

def select_questions(question_type):
    """Select 3 random logical IQ test questions."""
    logical_test = [
        {
            "id": 1,
            "question": "What is the next number in the sequence: 2, 6, 12, 20, 30, ?",
            "hint": "Consider the difference between consecutive numbers.",
            "solution": "42",
            "explanation": "The differences are increasing by 2: 4, 6, 8, 10, 12. So 30 + 12 = 42."
        },
        {
            "id": 2,
            "question": "If a child is born on the 29th of February, how many birthdays will they celebrate by their 20th year?",
            "hint": "Think about leap years.",
            "solution": "5",
            "explanation": "There are 5 leap years in 20 years: (4, 8, 12, 16, 20)."
        },
        {
            "id": 3,
            "question": "In a certain code, COMPUTER is written as RFUVQNPC. How is PRINTER written in the same code?",
            "hint": "Look for patterns in letter substitution.",
            "solution": "QSJOUFS",
            "explanation": "Each letter is shifted forward by one in the alphabet."
        },
        {
            "id": 4,
            "question": "If all Zips are Zaps, and some Zaps are Zops, which of the following must be true?\nA) All Zips are Zops B) Some Zips are Zops C) No Zips are Zops",
            "hint": "Use logical deduction based on set relationships.",
            "solution": "B",
            "explanation": "Some Zaps are Zops, so it’s possible that some Zips are Zops."
        },
        {
            "id": 5,
            "question": "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?",
            "hint": "Set up an equation based on the given information.",
            "solution": "5 cents",
            "explanation": "x + (x + 1) = 1.10 → 2x = 0.10 → x = 0.05"
        },
        {
            "id": 6,
            "question": "If A is the brother of B, and B is the sister of C, what is A’s relation to C?",
            "hint": "Draw a family tree.",
            "solution": "Brother",
            "explanation": "A and B are siblings, and B is C’s sister → A is C’s brother."
        },
        {
            "id": 7,
            "question": "Which number is the odd one out: 121, 144, 169, 196, 225, 256, 300?",
            "hint": "Check for perfect squares.",
            "solution": "300",
            "explanation": "All others are perfect squares; 300 is not."
        },
        {
            "id": 8,
            "question": "If in a code language, CAT = XZG, then DOG = ?",
            "hint": "Reverse the alphabet and match positions.",
            "solution": "WLT",
            "explanation": "A→Z, B→Y, ..., so C→X, A→Z, T→G → DOG = WLT."
        },
        {
            "id": 9,
            "question": "Tom is 5 ranks ahead of John in a class of 40. If John is 25th, what is Tom’s rank?",
            "hint": "Just subtract 5 from John's rank.",
            "solution": "20",
            "explanation": "25 - 5 = 20."
        },
        {
            "id": 10,
            "question": "A man walks 5 km north, turns right, walks 3 km, turns right again, walks 5 km. Where is he from the starting point?",
            "hint": "Visualize or draw the path.",
            "solution": "3 km East",
            "explanation": "He ends up 3 km east from his starting point."
        },
        {
            "id": 11,
            "question": "Find the missing number in the series: 3, 9, 27, ?, 243.",
            "hint": "Check multiplication pattern.",
            "solution": "81",
            "explanation": "Each term is multiplied by 3."
        },
        {
            "id": 12,
            "question": "Which is the next letter: A, C, F, J, O, ?",
            "hint": "Look at ASCII or position difference.",
            "solution": "U",
            "explanation": "+2, +3, +4, +5, +6 → next is +7 = U."
        },
        {
            "id": 13,
            "question": "If only one of the following statements is true, which one is it?\nA: All are false.\nB: A is true.\nC: B is false.",
            "hint": "Use truth table logic.",
            "solution": "C",
            "explanation": "Only C can be true without contradiction."
        },
        {
            "id": 14,
            "question": "A is the mother of B. C is the son of A. D is the brother of C. What is the relation of D to B?",
            "hint": "Understand the family roles.",
            "solution": "Brother",
            "explanation": "All are siblings."
        },
        {
            "id": 15,
            "question": "Which word does not belong? Apple, Banana, Mango, Carrot, Grapes",
            "hint": "Think fruits vs vegetables.",
            "solution": "Carrot",
            "explanation": "Carrot is a vegetable; others are fruits."
        },
        {
            "id": 16,
            "question": "If some pens are books and some books are papers, then which is definitely true?\nA) Some pens are papers\nB) All pens are papers\nC) None",
            "hint": "Venn diagram helps.",
            "solution": "C",
            "explanation": "No definite relationship between pens and papers."
        },
        {
            "id": 17,
            "question": "Statement 1: John is taller than Mike. Statement 2: Mike is taller than Steve. Conclusion: John is taller than Steve.",
            "hint": "Use transitive property.",
            "solution": "Yes",
            "explanation": "John > Mike > Steve → John > Steve."
        },
        {
            "id": 18,
            "question": "Which set of letters completes the series: AZ, BY, CX, ?",
            "hint": "Reverse alphabets.",
            "solution": "DW",
            "explanation": "A-Z, B-Y, C-X, D-W (next in sequence)."
        },
        {
            "id": 19,
            "question": "You see a boat filled with people, but there isn’t a single person on board. How?",
            "hint": "Play on words.",
            "solution": "All are married",
            "explanation": "“Single” means unmarried."
        },
        {
            "id": 20,
            "question": "Input: 26 13 7 4. Output after Step 1: 13 26 7 4. Step 2: 13 7 26 4. Step 3: ?",
            "hint": "Observe the shifting.",
            "solution": "13 7 4 26",
            "explanation": "The largest number is moved to the end in each step."
        },
        {
            "id": 21,
            "question": "If 'Blue is called Red', 'Red is called Green', and 'Green is called Blue', what is the color of grass?",
            "hint": "Look at the actual color vs. coded terms.",
            "solution": "Red",
            "explanation": "Grass is green, which is called Red."
        },
        {
            "id": 22,
            "question": "Find the analogy: Pen : Write :: Knife : ?",
            "hint": "Function-based analogy.",
            "solution": "Cut",
            "explanation": "Pen is used to write; Knife is used to cut."
        },
        {
            "id": 23,
            "question": "What will come in place of the question mark: 1, 1, 2, 3, 5, 8, ?",
            "hint": "Fibonacci sequence.",
            "solution": "13",
            "explanation": "Each term = sum of previous two."
        },
        {
            "id": 24,
            "question": "What is always coming, but never arrives?",
            "hint": "It's a riddle.",
            "solution": "Tomorrow",
            "explanation": "It’s always in the future."
        },
        {
            "id": 25,
            "question": "Data: Peter is older than Sam. John is younger than Peter but older than Sam. Who is the oldest?",
            "hint": "Order them by age.",
            "solution": "Peter",
            "explanation": "Peter > John > Sam."
        },
        {
            "id": 26,
            "question": "Which direction is your right hand if you face South?",
            "hint": "Turn and visualize.",
            "solution": "West",
            "explanation": "Facing South → right is West."
        },
        {
            "id": 27,
            "question": "If 2 + 3 = 13, 3 + 4 = 25, 4 + 5 = 41, what is 5 + 6?",
            "hint": "Find hidden pattern.",
            "solution": "61",
            "explanation": "2 + 3 = 5 → 5 × 2 + 3 = 13. Pattern follows."
        },
        {
            "id": 28,
            "question": "Which of the following can be a day after two days of Monday?",
            "hint": "Just count forward.",
            "solution": "Wednesday",
            "explanation": "Monday + 2 = Wednesday."
        },
        {
            "id": 29,
            "question": "If all roses are flowers and some flowers fade quickly, can we say some roses fade quickly?",
            "hint": "Syllogism type.",
            "solution": "Cannot say",
            "explanation": "Some flowers fade doesn’t imply roses fade."
        },
        {
            "id": 30,
            "question": "A man is looking at a photograph of someone. His friend asks who it is. He replies: “Brothers and sisters, I have none. But that man's father is my father's son.” Who is in the photo?",
            "hint": "Break down the sentence.",
            "solution": "His son",
            "explanation": "“My father’s son” = himself → the man in the photo is his son."
        }
    ]

    numerical_questions = [
        {
            "id": 1,
            "question": "What is the next number in the series: 3, 9, 27, 81, ?",
            "hint": "Look for a multiplication pattern.",
            "solution": "243",
            "explanation": "Each number is multiplied by 3. 81 × 3 = 243."
        },
        {
            "id": 2,
            "question": "Find the missing number: 7, 14, 28, ?, 112",
            "hint": "Check the pattern in doubling.",
            "solution": "56",
            "explanation": "Each number is multiplied by 2. 28 × 2 = 56."
        },
        {
            "id": 3,
            "question": "What is the sum of all odd numbers from 1 to 99?",
            "hint": "Use the formula for the sum of the first n odd numbers.",
            "solution": "2500",
            "explanation": "There are 50 odd numbers between 1 and 99. Sum = 50² = 2500."
        },
        {
            "id": 4,
            "question": "If 3x - 7 = 11, what is the value of x?",
            "hint": "Rearrange and solve the linear equation.",
            "solution": "6",
            "explanation": "3x = 18, so x = 6."
        },
        {
            "id": 5,
            "question": "Which number is missing in the series: 2, 4, 8, 16, ?, 64",
            "hint": "Exponential pattern.",
            "solution": "32",
            "explanation": "Each number is a power of 2: 2, 4, 8, 16, 32, 64."
        },
        {
            "id": 6,
            "question": "What is 111 × 111?",
            "hint": "Use special multiplication trick or calculate directly.",
            "solution": "12321",
            "explanation": "111 × 111 = 12321 (pattern of repeating 1s)."
        },
        {
            "id": 7,
            "question": "If 2 pencils cost 8 cents, how much do 12 pencils cost?",
            "hint": "Find cost per pencil and multiply.",
            "solution": "48",
            "explanation": "Each pencil costs 4 cents. 12 × 4 = 48 cents."
        },
        {
            "id": 8,
            "question": "What is the value of: 5 + 5 × 5 - 5",
            "hint": "Follow BODMAS/BIDMAS rules.",
            "solution": "25",
            "explanation": "5 + (5 × 5) - 5 = 5 + 25 - 5 = 25."
        },
        {
            "id": 9,
            "question": "If a train travels at 60 km/h, how far will it travel in 45 minutes?",
            "hint": "Convert time to hours.",
            "solution": "45 km",
            "explanation": "45 minutes = 0.75 hours. Distance = speed × time = 60 × 0.75 = 45 km."
        },
        {
            "id": 10,
            "question": "A rectangle has a length of 10 cm and width of 4 cm. What is its area?",
            "hint": "Area = length × width.",
            "solution": "40",
            "explanation": "10 × 4 = 40 cm²."
        },
        {
            "id": 11,
            "question": "How many 3-digit numbers are divisible by 5?",
            "hint": "Find the range of 3-digit numbers divisible by 5.",
            "solution": "180",
            "explanation": "Smallest: 100, largest: 995. (995 - 100)/5 + 1 = 180."
        },
        {
            "id": 12,
            "question": "Find the square of 25.",
            "hint": "Simple math fact or formula (a + b)².",
            "solution": "625",
            "explanation": "25 × 25 = 625."
        },
        {
            "id": 13,
            "question": "What is 1 + 2 + 3 + ... + 100?",
            "hint": "Use the sum of first n natural numbers formula.",
            "solution": "5050",
            "explanation": "Sum = n(n+1)/2 = 100 × 101 / 2 = 5050."
        },
        {
            "id": 14,
            "question": "Find the missing number: 1, 4, 9, 16, ?, 36",
            "hint": "Perfect squares.",
            "solution": "25",
            "explanation": "1², 2², 3²... next is 5² = 25."
        },
        {
            "id": 15,
            "question": "What is the cube root of 27?",
            "hint": "Think of numbers multiplied 3 times.",
            "solution": "3",
            "explanation": "3 × 3 × 3 = 27."
        },
        {
            "id": 16,
            "question": "Which number is 20% of 250?",
            "hint": "Calculate 20% of the value.",
            "solution": "50",
            "explanation": "20/100 × 250 = 50."
        },
        {
            "id": 17,
            "question": "A shopkeeper sells an item for ₹150 and gains 25%. What is the cost price?",
            "hint": "Selling Price = Cost Price + 25%.",
            "solution": "120",
            "explanation": "Let CP = x. 1.25x = 150 → x = 120."
        },
        {
            "id": 18,
            "question": "What number comes next: 0, 1, 1, 2, 3, 5, 8, ?",
            "hint": "Fibonacci series.",
            "solution": "13",
            "explanation": "Each number is the sum of the previous two: 5+8 = 13."
        },
        {
            "id": 19,
            "question": "If 6 workers can complete a task in 8 days, how many days will 4 workers take?",
            "hint": "Use work = men × days.",
            "solution": "12",
            "explanation": "6×8 = 4×x → x = 12."
        },
        {
            "id": 20,
            "question": "Find the missing number in this pattern: 10, 17, 26, 37, ?",
            "hint": "Look at the differences.",
            "solution": "50",
            "explanation": "+7, +9, +11, +13 → next is +13 → 37+13 = 50."
        },
        {
            "id": 21,
            "question": "What is the angle sum of a hexagon?",
            "hint": "Use (n-2) × 180° formula.",
            "solution": "720",
            "explanation": "6-sided → (6-2)×180 = 720°."
        },
        {
            "id": 22,
            "question": "What is 0.75 as a fraction in its simplest form?",
            "hint": "Convert decimal to fraction.",
            "solution": "3/4",
            "explanation": "0.75 = 75/100 = 3/4."
        },
        {
            "id": 23,
            "question": "If a book is sold at 10% discount on ₹500, what is the selling price?",
            "hint": "Apply the discount.",
            "solution": "450",
            "explanation": "10% of 500 = 50. 500 - 50 = 450."
        },
        {
            "id": 24,
            "question": "How many prime numbers are there between 1 and 20?",
            "hint": "List them and count.",
            "solution": "8",
            "explanation": "Primes: 2, 3, 5, 7, 11, 13, 17, 19 → total: 8."
        },
        {
            "id": 25,
            "question": "What is the least common multiple (LCM) of 6 and 8?",
            "hint": "Find the smallest number divisible by both.",
            "solution": "24",
            "explanation": "LCM of 6 and 8 is 24."
        }
    ]

    return random.sample(logical_test,3) if question_type=='logical_test' else random.sample(numerical_questions,3)

def get_quiz_data():
    
    # Define the quiz questions organized by domain
    quiz_data = {
        "Software Testing": [
            "I enjoy noticing small mistakes in things, like when an app doesn’t work the way it should.",
            "I’m curious about figuring out why something, like a website or game, isn’t working properly.",
            "I feel satisfied when I spot a problem and can suggest how to make it better.",
            "I like imagining different ways people might use an app to see if it breaks or acts strangely.",
            "I don’t mind repeating a task several times to make sure everything works correctly.",
            "I often pay attention to tiny details when using apps or tools, like buttons or menus that seem off."
        ],
        "DevOps": [
            "I enjoy finding ways to make tasks faster and easier, like setting up shortcuts for repetitive work.",
            "I’m curious about how apps or websites stay running smoothly all the time, even with lots of users.",
            "I like the idea of helping different teams work together to get a project done quickly.",
            "I find it interesting to learn how online tools, like file-sharing apps, store and manage information.",
            "I enjoy figuring out how to connect different tools or systems to make them work better together.",
            "I’m excited by the idea of keeping a system up and running without needing constant fixes."
        ],
        "Cybersecurity": [
            "I’m curious about how people try to sneak into apps or websites and how to stop them.",
            "I like learning simple ways to keep my information safe, like using strong passwords.",
            "I enjoy thinking about how to protect things, like accounts or devices, from being misused.",
            "I find it interesting to hear about how companies keep our data private and secure.",
            "I’d like to try testing a system by pretending to break into it to make it safer.",
            "I often notice warnings or tips about staying safe online and think about why they matter."
        ],
        "AI/ML/Data Science": [
            "I enjoy solving problems by looking for patterns or trends in information.",
            "I’m curious about how apps or tools can learn to make decisions, like recommending songs or movies.",
            "I like working with numbers or data to figure out what they mean, even in simple ways.",
            "I find it fun to solve puzzles or challenges that need step-by-step thinking.",
            "I’m excited by the idea of making tasks easier by teaching a computer to do them.",
            "I enjoy turning messy information into something clear, like organizing a list or chart."
        ],
        "UI/UX": [
            "I enjoy making things look neat and organized, like notes, slides, or a workspace.",
            "I often notice if an app or website is easy to use or confusing when I try it.",
            "I like thinking about how to make something more enjoyable for others to use.",
            "I’m excited by the idea of creating designs that are both nice to look at and simple to use.",
            "I enjoy tweaking things, like a layout or design, after seeing how people interact with it.",
            "I find it fun to create visuals that tell a story, like posters or app screens."
        ],
        "Mobile Development": [
            "I like imagining ideas for apps that could make daily tasks quicker or more fun.",
            "I often notice how fast or smooth an app feels when I use it on my phone.",
            "I’m curious about how apps work differently on various phones or with slow internet.",
            "I enjoy thinking about creating tools people can use anywhere, like on their phone.",
            "I find it exciting to design features that make an app addictive or satisfying to use.",
            "I like the idea of solving real-world problems by building a mobile app."
        ],
        "Web Development": [
            "I enjoy exploring websites and noticing how they’re set up to help users find what they need.",
            "I’m curious about how websites work behind the scenes, like how they store or show information.",
            "I like the idea of building a website that anyone can visit from anywhere.",
            "I find it fun to think about adding features to a website, like a search tool or sign-up form.",
            "I notice when a website feels smooth and quick to use, and I wonder how it’s made.",
            "I’m excited by creating something online that looks good and works well for everyone."
        ],
        "Game Development": [
            "I enjoy thinking about how to turn everyday ideas into fun challenges or stories for a game.",
            "I’m curious about how games are built to keep players interested and having fun.",
            "I like imagining what goes into making a game, like its characters, levels, or sounds.",
            "I find it exciting to create something interactive that others can play and enjoy.",
            "I often notice details, like visuals or music, in games and think about how they’re made.",
            "I’m interested in designing game features, like points or rewards, to make it more fun."
        ]
    }

    

    return quiz_data

# Function to calculate scores
def calculate_scores(responses):
    # Scoring system
    scoring = {
        "Strongly Agree": 2,
        "Agree": 1,
        "Neutral": 0,
        "Disagree": -1,
        "Strongly Disagree": -2
    }
    quiz_data = get_quiz_data()
    domain_scores = {domain: 0 for domain in quiz_data.keys()}
    for (domain, question_idx), response in responses.items():
        domain_scores[domain] += scoring[response]
    return domain_scores

# Function to get top 3 domains
def get_top_3_domains_from_quiz(scores):
    # Sort domains by score in descending order
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    # Return top 3 (or fewer if less than 3 domains)
    return sorted_scores[:3]