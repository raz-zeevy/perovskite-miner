from prompt_engineering.prompt_engineering import openai_count_tokens as count_tokens, read_pdf, clean_text
from utils import calculate_mean, calculate_std

import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt


def calculate_papers_stats(paper_db_path):
    df = pd.read_csv(paper_db_path)
    token_counts = df['tokens'].to_list()
    clean_token_counts = df['clean_tokens'].to_list()
    print_length_statistics(clean_token_counts, token_counts)
    plot_text_tokens_length(clean_token_counts)


def create_paper_db(directory_path):
    token_counts, clean_token_counts = [], []
    rows_data = []
    for root, dirs, files in os.walk(directory_path):
        for i, file in enumerate(files):
            if i % 100 == 0:
                print(f"processing file {i} out of {len(files)}")
            if file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                try:
                    text = read_pdf(file_path)
                    token_counts.append(count_tokens(text))
                    cleaned_text = clean_text(text)
                    clean_token_counts.append(count_tokens(cleaned_text))
                    row_data = [file[:-4], len(text), len(cleaned_text), count_tokens(text),
                                count_tokens(cleaned_text), text]
                    rows_data.append(row_data)

                except Exception as e:
                    with open('../dataset/corrupted_pdf.txt', 'a') as f:
                        f.write(f"Could not read file '{file}' due to: {str(e)}\n")
                    print(f"Could not read file '{file}' due to: {str(e)}")

    df = pd.DataFrame(rows_data, columns=['DOI', 'length', 'clean_length', 'tokens', 'clean_tokens', 'text'])
    df.to_csv('../dataset/papers_db.csv', index=False)


def print_length_statistics(clean_token_counts, token_counts):
    mean_token_count = calculate_mean(token_counts)
    mean_clean_token_count = calculate_mean(clean_token_counts)
    std_token_count = calculate_std(token_counts)
    std_clean_token_count = calculate_std(clean_token_counts)
    print("The number of PDFs is: " + str(len(token_counts)))
    print(f"The mean number of tokens across all PDFs is: {int(mean_token_count)} [{int(std_token_count)}]")
    print(f"The mean number of tokens across all clean PDFs is: {int(mean_clean_token_count)} " +
          f"[{int(std_clean_token_count)}]")
    token_counts.sort(reverse=True)
    print(f"Number of papers with length greater than 14500 tokens: " +
          f"{len([x for x in token_counts if x > 14500])}")


def plot_text_tokens_length(text_tokens_lengths):
    n_bins = 50
    plt.hist(np.array(text_tokens_lengths), bins=n_bins)
    plt.title("Histogram of \"clean\" text lengths")
    plt.xlabel("Text length in tokens")
    plt.ylabel("Number of papers")
    plt.savefig('../plots/text_lengths_hist.png')
    plt.show()


if __name__ == '__main__':
    dir_path = "../dataset/papers"
    calculate_papers_stats('../dataset/papers_db.csv')
