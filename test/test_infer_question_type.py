import pytest

from data.questions_data import infer_question_type


def test_infer_question_type():
    assert infer_question_type("T. Jesper Jacobsson") == "string", "Unexpected question type"
    assert infer_question_type("333") == "int", "Unexpected question type"
    assert infer_question_type("3.1") == "float", "Unexpected question type"
    assert infer_question_type("-0.1") == "string", "Unexpected question type"
    assert infer_question_type("1900-03-24 02:03:14") == "date", "Unexpected question type"
    assert infer_question_type("What is the |  meaning of life?") == "sequence of string", "Unexpected question type"
    assert infer_question_type("[TRUE/FALSE | TRUE/FALSE | ]") == "sequence of boolean", "Unexpected question type"
    assert infer_question_type("1 | 3") == "sequence of int", "Unexpected question type"
    assert infer_question_type("0.1 | 5.9") == "sequence of float", "Unexpected question type"
    assert infer_question_type("0") == "int", "Unexpected question type"


if __name__ == "__main__":
    pytest.main([__file__])
