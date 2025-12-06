import json
import numpy as np

TRAIT_ORDER = [
    "Resilience",
    "Stealth",
    "Chaos/Disruption",
    "Creativity/Innovation",
    "Teamwork/Sociability",
    "Intensity/Danger",
]


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


def get_best_microbe_match(microbes: dict, answer: dict) -> tuple[str, dict]:
    """Match answers to a microbe.

    Answer is an array of six values, ranging from 0-6. The best matching
    microbe is found by calculating the distance to each microbes answer
    array and returning the closes one.
    """
    # Convert answers to a NumPy array
    answer_list = []
    for trait in TRAIT_ORDER:
        answer_list.append(answer[trait])

    answer_array = np.array(answer_list)

    # Convert all personality answer sets to a 2D NumPy array
    trait_arrays = np.array([list(p["answers"].values()) for p in microbes.values()])

    # Compute Euclidean distances
    distances = np.linalg.norm(trait_arrays - answer_array, axis=1)

    # Find the index of the closest personality
    closest_index = np.argmin(distances)

    # Map back to the personality key
    microbe = list(microbes.keys())[closest_index]

    return microbe, microbes[microbe]
