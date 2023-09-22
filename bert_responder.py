from transformers import BertTokenizer, BertForQuestionAnswering
from prompt_engineering.prompt_engineering_consts import preview_prompt
from prompt_engineering.prompt_engineering import read_pdf, clean_text
import torch


def access_bert():
    # Load pre-trained model and tokenizer
    model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
    model = BertForQuestionAnswering.from_pretrained(model_name)
    tokenizer = BertTokenizer.from_pretrained(model_name)

    question = "What is the Ref Lead author?, Example:\"Jacobsson et al.\""
    paper = clean_text(read_pdf("/test/pdf_mock.pdf"))

    # Tokenize input and obtain input_ids and attention_mask
    inputs = tokenizer(paper + question, preview_prompt, return_tensors='pt')
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    # Forward pass, get start and end position logits
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        start_scores, end_scores = outputs.start_logits, outputs.end_logits

    # Get the start and end positions of the answer
    start_position = torch.argmax(start_scores)
    end_position = torch.argmax(end_scores)

    # Get the answer from the input_ids
    answer_ids = input_ids[0][start_position : end_position + 1]
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(answer_ids))

    # Save the response to a file
    with open("bert_response.txt", "w") as file:
        file.write(answer)

    print("Answer:", answer)


if __name__ == '__main__':
    access_bert()
