<img src="./media/logo.png" alt="Perovskite Miner Logo" width="300"/>


# Perovskite Miner

Welcome to the `perovskite-miner` project! This tool harnesses the power of AI, specifically Large Language Models (LLMs), to automatically extract data from perovskite research papers. The extracted data can be transformed and integrated into the Perovskite Database. Whether you're a researcher, developer, or enthusiast in the field of perovskite materials, this project offers a state-of-the-art solution to streamline data collection and database population.

**Authors: Raz Zeevy, Iris Burmistrov**

## Table of Contents

- [Introduction](#introduction)
- [About the Project](#about-the-project)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

Perovskite solar cells have emerged as a promising frontier in the realm of renewable energy. These solar cells, characterized by their unique crystallographic structure, have garnered significant attention due to their potential to revolutionize solar energy harnessing. The research landscape is vibrant, with continuous efforts aimed at developing more efficient and stable perovskite solar cells.

Given the rapid pace of advancements, a multitude of research papers are published every week, each contributing valuable insights and data to the field. The vision behind the **Perovskite Database** is to centralize this wealth of information, offering a convenient platform for filtering and analysis. Such a consolidated database can significantly enhance collaboration between research groups worldwide, propelling the pace of scientific discoveries.

Our project, `perovskite-miner`, is a pivotal step towards realizing this vision. By automating the extraction of data from the plethora of research papers, it aims to keep the Perovskite Database updated with the latest findings. This continuous influx of fresh data can serve as the driving force behind the Perovskite Database project, fostering a collaborative environment and accelerating advancements in perovskite solar cell research.

## Acknowledgment
We would like to extend our heartfelt gratitude to **Eva Unger's group** at **Helmholtz-Zentrum Berlin**. Their invaluable support, hosting, and contributions have been instrumental in the realization of this project. Their expertise and guidance have been a cornerstone in our journey, and we deeply appreciate their unwavering assistance.

## About the Project

The `perovskite-miner` project is a cutting-edge tool designed to harness the capabilities of Large Language Models (LLMs) for the purpose of extracting data from perovskite research papers. The primary objective is to transform the extracted data for integration into the perovskite database.

### Pipeline Overview

The data extraction process in `perovskite-miner` follows a sophisticated pipeline to ensure optimal results:

1. **Prompt Generator**: The raw content of a perovskite paper is transformed into a prompt suitable for a Large Language Model (LLM). This involves understanding the context, extracting key information, and formulating questions that the LLM can answer.

2. **Parsing and Truncation**: Given the token limits of commercial LLMs, the project employs parsing and truncation methods. This ensures that the paper's content, along with the generated questions and answers, fit within the LLM's constraints.

3. **LLM Integration**: The generated prompt is then sent to a commercial LLM for processing. While the current implementation is integrated with GPT, the architecture is designed to be extensible, allowing for easy integration with other commercial LLMs in the future.

4. **Answer Matching**: Once the LLM returns the answers, they are matched with the actual fields in the database. This step ensures that the AI's responses align with the posed questions and are structured correctly for subsequent parsing.

5. **Parsing and CSV Generation**: The final stage involves parsing the AI's answers and organizing them into a structured format. The output is a CSV file with corresponding fields and their answers, ready for integration into the perovskite database.

This pipeline ensures a systematic and accurate approach to extracting data from perovskite papers, leveraging the capabilities of LLMs while maintaining structure and consistency in the output.

### Evaluation Module

The `perovskite-miner` project includes an evaluation module designed to assess the performance of the model. This module provides metrics and insights into the accuracy, reliability, and efficiency of the data extraction process, ensuring that the AI's outputs meet the desired standards.

## Installation

To get started with `perovskite-miner`, follow these installation steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/raz-zeevy/perovskite-miner.git
   ```

2. Navigate to the project directory:
   ```bash
   cd perovskite-miner
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Once installed, you can utilize the various modules and scripts provided in this repository. Here's a brief overview of how to use some of the main features:

- **Data Analysis**:
  Navigate to the `data` directory and run the desired analysis script. For example:
  ```bash
  python perovskite_analysis.py
  ```

- **API Integrations**:
  The `apis` directory contains scripts for integrating with machine learning models. Run the desired API script as needed.

- **Data Scraping**:
  Use the scripts in the `scraper` directory to gather the latest research papers and data.

For detailed usage instructions and examples, refer to the individual script documentation and comments.

## Contributing

Contributions are always welcome! If you have suggestions, bug reports, or want to contribute to the code, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any questions or feedback, please reach out to raz3zeevy@gmail.com or to iris.burmistrov@mail.huji.ac.il 
