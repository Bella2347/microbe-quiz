"""Check how many answer options that map to the different microbes."""

import itertools
from collections import Counter
from quiz import load_microbes, get_best_microbe_match

# Define the range of each element
values = range(7)  # 0 to 6 inclusive

# Generate all possible arrays
all_answer_arrays = list(itertools.product(values, repeat=6))

personality_traits = [
    "Resilience",
    "Stealth",
    "Chaos/Disruption",
    "Creativity/Innovation",
    "Teamwork/Sociability",
    "Intensity/Danger",
]

matches = Counter()

for answer_array in all_answer_arrays:
    microbes = load_microbes()
    microbe, _ = get_best_microbe_match(
        microbes, dict(zip(personality_traits, answer_array))
    )

    matches[microbe] += 1

for match, count in matches.items():
    print(f"{match}: {count/len(all_answer_arrays)*100:.2f} % ({count})")
