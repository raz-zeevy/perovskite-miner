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

Through the development and deployment of our data extraction pipeline, we've reached the following noteworthy conclusions and achievements:

- **Automation:** Our pipeline adeptly automates the arduous task of extracting data from PDF documents, significantly mitigating manual effort and potential errors.

- **Data Standardization:** Extracted data is systematically structured into a CSV format, rendering it suitable for seamless integration into databases and subsequent analysis.

- **Time Efficiency:** Our pipeline has proven itself as a time-efficient solution, especially when dealing with a substantial volume of PDF documents.

- **Flexibility:** The utilization of a question protocol affords the flexibility needed to adapt the pipeline to diverse datasets and research domains.

## Future Directions

As we conclude this project, we envision several promising avenues for future development and enhancement:

- **Enhancement of NLP Techniques:** Continuing to refine and bolster the accuracy and resilience of NLP-based data extraction methods.

- **Integration:** Seamlessly integrating our pipeline with existing materials science databases for effortless data aggregation and analysis.

- **User Interface:** Pioneering the development of a user-friendly interface to broaden the pipeline's accessibility.

This project marks a significant stride toward automating the extraction of data from scientific documents. We eagerly anticipate its ongoing evolution and application within the realm of materials science research.

For any inquiries or contributions, please don't hesitate to contact us.

**Contact Information**:

- [Iris Burmistrov]: [iris.burmistrov@mail.huji.ac.il]
- [Raz Zeevy]: [raz3zeevy@gmail.com]

We appreciate your interest and support!
