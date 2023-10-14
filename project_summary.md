# Project Summary

## Project Overview

In this project, we've crafted a data extraction pipeline tailored to simplify the retrieval of experimental data from PDF documents. Our primary objective was to streamline the extraction process for a perovskite database, leveraging a predefined question protocol. The pipeline takes a PDF file's path as input and generates a structured CSV file containing the extracted experimental data.

## Pipeline and Module Description

### PDF Data Extraction Pipeline

Our data extraction pipeline comprises several pivotal components:

1. **Input PDF Parsing:** To begin, the pipeline parses the user-provided PDF document, focusing solely on textual content. As of now, it does not process graphical elements, images, or tables.

2. **Question Protocol:** We've harnessed the question protocol designed for the Perovskite database. Out of approximately 400 fields, we aim to populate around 70 using an AI model. This protocol serves as a blueprint for data extraction.

3. **Data Extraction:** Leveraging Natural Language Processing (NLP) techniques and regular expressions, we extract pertinent experimental data from the PDF documents, adhering to the question protocol. Currently, we utilize ChatGPT, with the aspiration of offering a choice among several Language Models (LMs) in the future, potentially integrating them seamlessly.

4. **Data Validation:** Extracted data undergoes thorough validation to ensure precision and consistency.

5. **CSV Output:** The pipeline's end product is a CSV file that houses the extracted data in a structured format, facilitating easy accessibility for further analysis.

### Perovskite Database

Our project places a specific emphasis on harvesting data related to perovskite materials, which hold substantial importance in materials science and energy research. Our objective is to swiftly and efficiently contribute data to the Perovskite Database. For more information, visit: [Perovskite Database](https://www.perovskitedatabase.com/)

## Conclusions

Through the development and implementation of this data extraction pipeline, we have achieved the following conclusions and outcomes:

- Automation: The pipeline successfully automates the process of data extraction from PDF documents, significantly reducing manual effort and potential errors.

- Data Standardization: The extracted data is standardized into a structured CSV format, making it suitable for integration into databases and further analysis.

- Time Efficiency: Our pipeline has proven to be a time-efficient solution for extracting experimental data from a large number of PDF documents.

- Flexibility: The use of a question protocol provides flexibility in adapting the pipeline to different datasets and research domains.

# Future Directions

As we conclude this project, we envision several potential directions for future development and improvement:

- **Analysis of Images, Graphs, and Tables:** Expanding our capabilities to extract data from images, graphs, and tables within PDF documents.

- **Enhancement of NLP Techniques:** Exploring the use of different Natural Language Processing (NLP) models and comparing their effectiveness in data extraction.

- **Integration:** Seamlessly integrating the pipeline with existing materials science databases to facilitate streamlined data aggregation and analysis.

- **User Interface:** Developing a user-friendly interface to enhance accessibility, making the pipeline more user-friendly for a broader audience.

This project represents a significant step toward automating data extraction from scientific documents, and we eagerly anticipate its continued development and application in materials science research.

For any inquiries or contributions, please feel free to contact us.

**Contact Information**:

- Iris Burmistrov: iris.burmistrov@mail.huji.ac.il
- Raz zeevy: raz3zeevy@gmail.com

Thank you for your interest and support!
