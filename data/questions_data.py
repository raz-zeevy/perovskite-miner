import pandas as pd
import jellyfish
from data_exploration.questions_const import *
from utils import load_data

DB_PATH = "../data/questions/questions_db.csv"

def format_questions_and_save_5_4(
        protocol_path='Extraction protocolls version 5_4.xlsx',
        sheet_name='Master',
        output_path='questions_5_4.txt',
        save_output=True,
        print_output=False):
    df = pd.read_excel(protocol_path, sheet_name=sheet_name)
    questions = df.iloc[:, 0].to_list()
    for i, question in enumerate(questions):
        new_question = questions[i]
        answer_format = ''
        if print_output: print(new_question)
        new_question = "What is the " + questions[i].replace(".", "")
        if "[" in new_question:
            splits = new_question.split(" [")
            answer_format = splits[1][:-1]
            new_question = splits[0] + "? Format of answer: [" + \
                           answer_format + "]"
        if df.iloc[i, 1] == df.iloc[i, 1]:
            # for some unsolvable issue the answer is converted from 0,
            # 1 to False,True. So additional conversion is needed
            example_answer = str(df.iloc[i, 1])
            if answer_format and "TRUE" not in answer_format:
                example_answer = example_answer. \
                    replace("False", "0"). \
                    replace("True", "1")
            new_question += ", Example:" + '"' + example_answer + '"'
        questions[i] = new_question
        if print_output: print(questions[i] + "\n")
    # save the questions to a txt file delimited each question by a "\n"
    if save_output:
        with open(output_path, "w") as output_path:
            for question in questions:
                output_path.write(str(question) + '\n')
    return questions


def load_questions_from_txt(questions_path):
    questions = []
    with open(questions_path, "r") as questions_path:
        for line in questions_path:
            questions.append(line.strip())
    return questions

def question_to_field(question: str):
    return best_5p_question_to_field.get(question)


def infer_field_from_question(question: str) -> (int, str):
    pervo_df = pd.read_csv(r"C:\Users\Raz_Z\Projects\perovskite-miner"
                           r"\Perovskite_database_content_all_data.csv",
                           low_memory=False)
    df_fields = pervo_df.columns
    for i, field in enumerate(df_fields):
        if jellyfish.jaro_distance(field, question) > 0.8:
            print("question: ", question)
            print("field: ", field)
            return i, field


def counted_tokens_data(questions_df : pd.DataFrame) -> pd.DataFrame:
    from prompt_engineering.prompt_engineering import count_tokens
    pervo_df = load_data()
    tokens_per_field = pervo_df.applymap(lambda x : count_tokens(str(
        x))).mean().rename_axis(FIELD_NAME).reset_index().round(1)
    merged = pd.merge(questions_df, tokens_per_field, on=FIELD_NAME,
                      how='left').rename(columns={0: TOKENS_PER_ANSWER})
    merged[TOKENS_PER_QUESTIONS] = merged[GPT_QUESTION].apply(
        lambda x: count_tokens(x))
    return merged

def create_questions_db(output_path: str) -> None:
    protocol_path = r'../data/questions/Extraction protocolls version 5_4.xlsx'
    sheet_name = 'Master'
    df = pd.read_excel(protocol_path, sheet_name=sheet_name)
    df.reset_index(inplace=True)
    df['questions'] = format_questions_and_save_5_4(
        protocol_path=protocol_path,
        save_output=False,
        print_output=False)
    df.columns = [QID, PROTOCOL_QUESTION, EXAMPLE_ANSWER,
                  GPT_QUESTION]
    df[FIELD_NAME] = df[PROTOCOL_QUESTION].apply(
        lambda question: question_to_field(question))
    df = df[[QID, PROTOCOL_QUESTION, FIELD_NAME, GPT_QUESTION,
             EXAMPLE_ANSWER]]
    df = counted_tokens_data(df)
    df.to_csv(output_path, index=False)


if __name__ == '__main__':
    create_questions_db(output_path=DB_PATH)