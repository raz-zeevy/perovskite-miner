

gpt_preview_prompt = """
Your task is to extract specific data from an academic paper focused on solar cells and perovskite materials. 
You will receive the full text of the paper along with questions and a format for the answers.
IT IS VERY IMPORTANT TO NOT CHANGE THE QUESTIONS FORMAT. Answer the questions exactly as written in the input, 
in the same order, and with the exact same text. If there is no answer available in the input, output 'nan' on that 
line.
Analyze the text meticulously to identify and list down the relevant data according to the specified format. 
Ensure to capture key details such as methodologies, findings, and any numerical data presented in the paper. 
Your output should be a structured list of answers adhering to the requested format. 
Accuracy and attention to detail are paramount.
"""

preview_prompt_tokens = 200

tokens_deviation = 100
