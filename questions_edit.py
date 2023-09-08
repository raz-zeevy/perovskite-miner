import numpy as np
import pandas as pd
import openpyxl

def format_questions_and_save(
        protocol_path ='Extraction protocolls version 5_4.xlsx',
        sheet_name = 'Master',
        output_path ='questions_5_4.txt',
        save_output = True,
        print_output = False):
    df = pd.read_excel(protocol_path, sheet_name=sheet_name)
    questions = df.iloc[:,0].to_list()
    for i, question in enumerate(questions):
        new_question = questions[i]
        answer_format = ''
        if print_output : print(new_question)
        new_question = "What is the " + questions[i].replace(".","")
        if "[" in new_question:
            splits = new_question.split(" [")
            answer_format = splits[1][:-1]
            new_question = splits[0] + "? Format of answer: [" + \
                           answer_format + "]"
        if df.iloc[i,1] == df.iloc[i,1]:
            # for some unsolvable issue the answer is converted from 0,
            # 1 to False,True. So additional conversion is needed
            example_answer = str(df.iloc[i,1])
            if answer_format and "TRUE" not in answer_format:
                example_answer = example_answer.\
                    replace("False", "0").\
                    replace("True", "1")
            new_question += ", Example:" + '"'+ example_answer + '"'
        questions[i] = new_question
        if print_output : print(questions[i] + "\n")
    # save the questions to a txt file delimited each question by a "\n"
    if save_output:
        with open(output_path, "w") as output_path:
            for question in questions:
                output_path.write(str(question) + '\n')

if __name__ == '__main__':
    questions_path = 'questions_5_4.txt'
    format_questions_and_save(output_path=questions_path,
                              save_output=True,
                              print_output=False)