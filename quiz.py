import json
import os
import sys
import math
import string
import numpy as np

# Mapping answer choices to Greek letter groups
ANSWER_OPTIONS = ["A", "B", "C", "D", "E"]


def quiz():
    questions = load_questions()
    answers = run_quiz(questions)

    personalities = load_personalities()
    microbe, personality = get_personality_matches(personalities, answers)

    print_result(microbe, personality)


def load_questions() -> dict:
    # Questions and answer choices
    with open("config/questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    return questions


def load_personalities() -> dict:
    with open("config/personalities.json", "r", encoding="utf-8") as f:
        personalities = json.load(f)

    return personalities


def run_quiz(personalities: dict) -> dict:
    # Store answers
    answers = {}

    # Run the quiz
    print("\nWelcome to the 'Which Microbe Are You?' Quiz!\n")
    question_nr = 0

    for personality, questions in personalities.items():
        personality_score = 0

        for question, choices in questions.items():
            question_nr += 1
            answer_options = [string.ascii_uppercase[i] for i in range(len(choices))]

            clear()
            print(f"\n{question_nr}. {question}\n")

            for i, choice in enumerate(choices):
                print(f"{string.ascii_uppercase[i]}. {choice}")

            while True:
                answer = (
                    input(f"\nEnter your choice ({', '.join(answer_options)}): ")
                    .strip()
                    .upper()
                )

                if answer in answer_options:
                    personality_score += answer_options.index(answer)
                    break
                else:
                    print(
                        f"Invalid input. Please enter: {', '.join(answer_options)}."
                    )

        answers[personality] = personality_score

    return answers


def clear() -> None:
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix-based systems (Linux/macOS)
        os.system('clear') 


def get_personality_matches(personalities: dict, answers: dict) -> tuple[str, dict]:
    # Convert answers to a NumPy array
    answer_array = np.array(list(answers.values()))
    
    # Convert all personality answer sets to a 2D NumPy array
    personality_arrays = np.array([
        list(p["answers"].values()) for p in personalities.values()
    ])
    
    # Compute Euclidean distances
    distances = np.linalg.norm(personality_arrays - answer_array, axis=1)
    
    # Find the index of the closest personality
    closest_index = np.argmin(distances)
    
    # Map back to the personality key
    microbe = list(personalities.keys())[closest_index]
    
    return microbe, personalities[microbe]


def print_result(microbe: str, personality: dict) -> None:
    clear()

    print("\nQuiz Complete!")
    print(f"\n{microbe} - {personality['title']}\n")
    print(f"{personality['personality']}\n")
    print(f"{personality['frenemies']}\n")


if __name__ == "__main__":
    quiz()
