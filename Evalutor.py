import numpy as np


def compute_error(model_output, expected_output, float_tolerance=1e-5):
    """
    Compute the error between the model output and the expected output.

    Parameters:
    model_output (list of tuples): The output from the ML model
    expected_output (list of tuples): The expected output
    float_tolerance (float): The tolerance for float comparisons

    Returns:
    float: The error rate
    """
    if len(model_output) != len(expected_output):
        raise ValueError("The length of model output and expected output must be equal")

    total_entries = len(model_output)
    incorrect_entries = 0

    for (model_val, expected_val) in zip(model_output, expected_output):
        if type(model_val[1]) != type(expected_val[1]):
            incorrect_entries += 1
        elif isinstance(model_val[1], float):
            if not np.isclose(model_val[1], expected_val[1], atol=float_tolerance):
                incorrect_entries += 1
        else:
            if model_val[1] != expected_val[1]:
                incorrect_entries += 1

    error_rate = (incorrect_entries / total_entries) * 100
    return error_rate


def main():
    # Usage example
    model_output = [(1, 'True'), (2, False), (3, 3.5), (4, 'hello'), (5, 6)]
    expected_output = [(1, 'True'), (2, True), (3, 3.49999), (4, 'hello'), (5, 6)]

    error_rate = compute_error(model_output, expected_output)
    print(f"Error rate: {error_rate}%")


if __name__ == '__main__':
    main()
