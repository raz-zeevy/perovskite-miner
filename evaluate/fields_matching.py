# Running the provided code to see the output
import jellyfish
import numpy as np
from collections import defaultdict

MINIMUM_SIMILARITY_THRESHOLD = 0.8


def calculate_similarity(field1, field2):
    """
    Calculate string similarity between two strings using the Jaro-Winkler and MRA metrics.

    Jaro-Winkler:
        - A string similarity measure that gives more weight to the prefix of the strings.
        - Score is normalized between 0 (no similarity) and 1 (identical strings).
        - Especially suitable for short strings and for strings with slight variations in the prefix.
        - More information: https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance

    Match Rating Approach (MRA):
        - A phonetic algorithm that breaks a word down into a set of phonetic keys.
        - It then uses these keys to calculate a similarity rating between two strings.
        - Can identify phonetically equivalent names or words with different spellings.
        - More information: https://en.wikipedia.org/wiki/Match_rating_approach

    Damerau Levenshtein: The Damerau-Levenshtein distance metric counts the number of edits
          (insertions, deletions, substitutions, and transpositions of two adjacent characters)
          to change one string into another. A lower Damerau-Levenshtein distance indicates the strings are more similar.
          More info: https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
    """

    def pre_proccess(field):
        new_field = field.replace("_", " ").lower().replace(":", "").replace(
            "?", "")
        return new_field

    field1 = pre_proccess(field1)
    field2 = pre_proccess(field2)
    jaro_winkler = jellyfish.jaro_winkler_similarity(field1, field2)
    mra = jellyfish.match_rating_comparison(field1, field2)
    max_len = max(len(field1), len(field2))
    damaro_lev = 1 - (jellyfish.damerau_levenshtein_distance(field1,
                                                             field2) / max_len)
    metrics = [metric for metric in [mra,damaro_lev,jaro_winkler]
               if metric is not None]
    return np.mean(metrics)


def match_fields(real_fields, ai_fields) -> dict:
    """
    Match AI fields to real fields based on similarity scores.
    """
    matched_fields = {}
    used_fields = set()

    for ai_field in ai_fields:
        max_similarity = 0
        best_match = None

        for real_field in real_fields:
            if real_field not in used_fields:
                similarity = calculate_similarity(ai_field, real_field)
                if similarity > max_similarity and \
                        similarity > MINIMUM_SIMILARITY_THRESHOLD:
                    max_similarity = similarity
                    best_match = real_field

        if best_match:
            matched_fields[ai_field] = best_match
            used_fields.add(best_match)

    return matched_fields


def rearrange_output(data, matched_fields):
    """
    Rearrange AI output based on matched fields.
    """
    rearranged_data = defaultdict(list)

    for ai_field, real_field in matched_fields.items():
        rearranged_data[real_field] = data[ai_field]

    return rearranged_data

def match_api_output(real_fields, ai_output) -> (dict, dict):
    ai_fields = list(ai_output.keys())
    matched_fields = match_fields(real_fields, ai_fields)
    # match the data
    matched_data = rearrange_output(ai_output, matched_fields)
    # invert the dict
    matched_fields = {v: k for k, v in matched_fields.items()}
    return matched_fields, matched_data

if __name__ == '__main__':
    # Sample data
    real_fields = ["not_existing_field", "Cell_stack_sequence", "Empty_field",
                   "Cell_area_measured",
                   "Cell_architecture", "not_existing_field"]
    ai_fields = ["Cell Stack sequence", "Cell Area Measured", "Cell Architecture"]
    ai_output = {
        "Cell Stack sequence": "SLG | FTO | TiO2-c | TiO2-mp | Perovskite | ITO",
        "Cell Area Measured": "0.096",
        "Cell Architecture": "nip"
    }
    rearranged_data = match_api_output(real_fields,ai_output)
    print(rearranged_data)
    print("done")
