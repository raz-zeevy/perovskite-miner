
from prompt_engineering.prompt_engineering import openai_count_tokens as count_tokens
from prompt_engineering.prompt_engineering_consts import preview_prompt

from utlis import load_data, calculate_mean, calculate_std


def calculate_question_stats():
    data = load_data('../data/questions/questions_db.csv')
    gpt_questions = data[data['field_name'].notna()]['gpt_question']
    print("Questions amount: " + str(len(gpt_questions)))

    questions_joined = ' '.join(gpt_questions)
    print("Tokens amount for questions: " + str(count_tokens(questions_joined)))


def calculate_answer_stats():
    # calculate number of tokens in each answer (row).
    questions_data = load_data('../data/questions/questions_db.csv')
    filtered_question = questions_data[questions_data['field_name'].notna()]['field_name']
    data = load_data('../data/Perovskite_database_content_all_data.csv')[filtered_question]
    answers = rows_to_strings(data)
    answers_tokens = []
    for answer in answers:
        answers_tokens.append(count_tokens(answer))

    mean_token_count = calculate_mean(answers_tokens)
    std_token_count = calculate_std(answers_tokens)
    print(f"The mean number of tokens across all answers is: {int(mean_token_count)} [{int(std_token_count)}]")


def calculate_preview_stats():
    print("Tokens amount for preview_prompt: " + str(count_tokens(preview_prompt)))


def rows_to_strings(df):
    return df.apply(lambda row: ' '.join(row.astype(str)), axis=1)


if __name__ == '__main__':
    calculate_preview_stats()
    calculate_question_stats()
    calculate_answer_stats()

