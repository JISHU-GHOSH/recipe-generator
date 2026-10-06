import os
import sys
from dotenv import load_dotenv
from groq import Groq

# Ensure UTF-8 output in Windows consoles
sys.stdout.reconfigure(encoding='utf-8')

# Load API key from .env file or environment variable
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY is not set. Please add it to your .env file or environment.")
    sys.exit(1)

client = Groq(api_key=api_key)

def generate_recipe(dish_name: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful culinary chef. When given a dish name, generate a clear, "
                    "easy-to-follow recipe formatted in markdown. Include:\n"
                    "1. Dish Name & brief description\n"
                    "2. Prep Time, Cook Time, and Servings\n"
                    "3. Ingredients list with measurements\n"
                    "4. Step-by-step numbered cooking instructions\n"
                    "5. A quick pro chef tip"
                )
            },
            {
                "role": "user",
                "content": f"Give me a complete recipe for: {dish_name}"
            }
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

def main():
    if len(sys.argv) > 1:
        dish_name = " ".join(sys.argv[1:])
    else:
        dish_name = input("Enter dish name: ").strip()

    if not dish_name:
        print("Please provide a valid dish name.")
        return

    print(f"\n[Generating recipe for '{dish_name}' using Groq AI...]\n")
    try:
        recipe = generate_recipe(dish_name)
        print(recipe)
    except Exception as e:
        print(f"Error calling Groq API: {e}")

if __name__ == "__main__":
    main()
