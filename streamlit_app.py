import streamlit as st
from dotenv import load_dotenv
import os
from groq import Groq
import groq

# env_path = os.path.join("groq_env", ".env")
# load_dotenv(env_path)  # Load environment variables from groq_env/.env

# # Retrieve API Key from environment variable
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")


load_dotenv()  # This assumes .env is in the root directory
api_key = os.getenv("GROQ_API_KEY")


# Initialize Groq Client
client = groq.Groq(api_key=api_key)

# ---------- step 2 FUNCTION TO GENERATE PLAN ---------- #
def generate_fitness_plan(goal, height, weight):
    prompt = f"""
Create a personalized and detailed **fitness and diet plan** for someone who wants to {goal}, is {height} cm tall, and weighs {weight} kg.

**Diet Plan Instructions:**
- Include meals for breakfast, lunch, and dinner.
- Provide a **nutritional breakdown** including approximate daily intake of:
  - Protein (grams)
  - Calcium (mg)
  - Fiber (grams)
  - Carbs and Fats (optional but preferred)
- Recommend water intake as well.
- Present the diet plan in **tabular format** for clarity.

**Exercise Plan Instructions:**
- Provide a **3-day muscle-based split** workout plan:
  - Day 1: Core + Chest
  - Day 2: Back + Legs
  - Day 3: Shoulders + Biceps + Triceps
- Each day should include 4–5 exercises with reps and sets.
- Present the workout schedule in **table format** as well.

Keep everything beginner-friendly and easy to follow.
"""


    completion = client.chat.completions.create(

        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            response += content
    return response

# ---------- 🖥️ STREAMLIT UI ---------- #
st.title("💪 AI Fitness Plan Generator (Groq - LLaMA 4)")

goal = st.selectbox("What's your goal?", ["Lose Weight", "Gain Muscle", "Stay Fit"])
height = st.number_input("Enter your height (cm):", min_value=100, max_value=250)
weight = st.number_input("Enter your weight (kg):", min_value=30, max_value=200)

if st.button("Generate Plan"):
    with st.spinner("Generating your personalized plan..."):
        plan = generate_fitness_plan(goal, height, weight)
        st.success("Here’s your fitness plan:")
        st.markdown(plan)
