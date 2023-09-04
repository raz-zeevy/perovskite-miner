
import json
import torch
from transformers import BertTokenizer, BertForQuestionAnswering
from torch.utils.data import DataLoader, Dataset


class perovskite(Dataset):
    def __init__(self, file_path):
        self.data = self.load_data(file_path)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def load_data(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        paragraphs = data['data'][0]['paragraphs']
        extracted_data = []
        for paragraph in paragraphs:
            context = paragraph['context']
            for qa in paragraph['qas']:
                question = qa['question']
                answer = qa['answers'][0]['text']
                start_pos = qa['answers'][0]['answer_start']
                extracted_data.append({
                    'context': context,
                    'question': question,
                    'answer': answer,
                    'start_pos': start_pos,
                })
        return extracted_data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        example = self.data[index]
        question = example['question']
        context = example['context']
        answer = example['answer']
        inputs = self.tokenizer.encode_plus(question,
                                            context, add_special_tokens=True,
                                            padding='max_length', max_length=512,
                                            truncation=True, return_tensors='pt')
        input_ids = inputs['input_ids'].squeeze()
        attention_mask = inputs['attention_mask'].squeeze()
        start_pos = torch.tensor(example['start_pos'])
        return input_ids, attention_mask, start_pos #, end_pos


def main():
    # Create an instance of the custom dataset
    file_path = 'perovskite.json'
    dataset = perovskite(file_path)

    # Set device (CPU or GPU)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Initialize the BERT model for question answering
    model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')
    model.to(device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    loss_fn = torch.nn.CrossEntropyLoss()
    batch_size = 8
    num_epochs = 50

    # Create data loader
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for batch in data_loader:
            # Move batch tensors to the device
            input_ids = batch[0].to(device)
            attention_mask = batch[1].to(device)
            start_positions = batch[2].to(device)

            # Zero the gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = model(input_ids, attention_mask=attention_mask,
                            start_positions=start_positions)
            loss = outputs.loss

            # Backward pass and optimization
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(data_loader)
        print(f"Epoch {epoch + 1}/{num_epochs} - Average Loss: {avg_loss:.4f}")

    # Create data loader
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    print("hi")


if __name__ == '__main__':
    main()