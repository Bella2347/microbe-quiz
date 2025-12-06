"""What microbe are you Quiz!"""

import json
import os
import string
import numpy as np

ANSWER_OPTIONS = ["A", "B", "C", "D", "E"]


def quiz():
    """Load questions and run quiz questions. Compute which microbe fits
    the answers best.
    """
    questions = load_questions()
    answer = run_quiz(questions)

    microbes = load_microbes()
    microbe, microbe_dict = get_best_microbe_match(microbes, answer)

    print_result(microbe, microbe_dict)


def load_questions() -> dict:
    """Load questions and answer options."""

    with open("config/questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    return questions


def load_microbes() -> dict:
    """Load microbes."""

    with open("config/microbes.json", "r", encoding="utf-8") as f:
        microbes = json.load(f)

    return microbes


def run_quiz(personality_questions: dict) -> dict:
    """Run quiz and save answers in an array, summing questions for the
    same personality trait.
    """
    # Store answers
    answers = {}

    # Run the quiz
    print("\nWelcome to the 'Which Microbe Are You?' Quiz!\n")
    question_nr = 0

    for personality_trait, questions in personality_questions.items():
        trait_score = 0

        for question, options in questions.items():
            question_nr += 1
            answer_options = [
                string.ascii_uppercase[i] for i in range(len(options))
            ]

            clear()
            print(f"\n{question_nr}. {question}\n")

            for i, choice in enumerate(options):
                print(f"{string.ascii_uppercase[i]}. {choice}")

            while True:
                answer = (
                    input(
                        f"\nEnter your choice ({', '.join(answer_options)}): "
                    )
                    .strip()
                    .upper()
                )

                if answer in answer_options:
                    trait_score += answer_options.index(answer)
                    break
                else:
                    print(
                        f"Invalid input. Please enter: {', '.join(answer_options)}."
                    )

        answers[personality_trait] = trait_score

    return answers


def clear() -> None:
    """Clear console."""

    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Unix-based systems (Linux/macOS)
        os.system("clear")


def get_best_microbe_match(
    microbes: dict, answer: dict
) -> tuple[str, dict]:
    """Match answers to a microbe.

    Answer is an array of six values, ranging from 0-6. The best matching
    microbe is found by calculating the distance to each microbes answer
    array and returning the closes one.
    """
    # Convert answers to a NumPy array
    answer_array = np.array(list(answer.values()))

    # Convert all personality answer sets to a 2D NumPy array
    trait_arrays = np.array(
        [list(p["answers"].values()) for p in microbes.values()]
    )

    # Compute Euclidean distances
    distances = np.linalg.norm(trait_arrays - answer_array, axis=1)

    # Find the index of the closest personality
    closest_index = np.argmin(distances)

    # Map back to the personality key
    microbe = list(microbes.keys())[closest_index]

    return microbe, microbes[microbe]


def print_result(microbe: str, microbe_dict: dict) -> None:
    """Print result to console."""

    clear()

    print("\nQuiz Complete!")
    print(f"\n{microbe} - {microbe_dict['title']}\n")
    print(f"{microbe_dict['personality']}\n")
    print(f"{microbe_dict['frenemies']}\n")


if __name__ == "__main__":
    quiz()
