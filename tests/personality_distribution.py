import itertools
from collections import Counter
from quiz import load_personalities, get_personality_matches

# Define the range of each element
values = range(7)  # 0 to 6 inclusive

# Generate all possible arrays
all_arrays = list(itertools.product(values, repeat=6))

personalities =  [
    "Resilience",
    "Stealth",
    "Chaos/Disruption",
    "Creativity/Innovation",
    "Teamwork/Sociability",
    "Intensity/Danger",
]

matches = Counter()

for array in all_arrays:
    loaded_personalities = load_personalities()
    microbe, _ = get_personality_matches(loaded_personalities, dict(zip(personalities, array)))

    matches[microbe] += 1

for match, count in matches.items():
    print(f"{match}: {count} ({count/len(all_arrays)*100:.2f} %)")
