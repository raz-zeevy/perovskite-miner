import requests
import numpy as np


def main():
    doi_list = np.loadtxt('../dataset/papers/doi-list.txt', delimiter=",", dtype=str)
    api_key = "irisburmi@gmail.com"
    papers_data = []
    open_papers_doi = []

    with open(r"../dataset/papers/papers_metadata.txt", 'w') as fp:
        for i, doi in enumerate(doi_list):
            if i % 5 == 0:
                print(f"Done {i} papers")
            url = f"https://api.unpaywall.org/v2/{doi}?email={api_key}"

            response = requests.get(url)
            paper_data = response.json()
            fp.write("%s\n" % paper_data)
            papers_data.append(paper_data)

            if paper_data.get("is_oa", False):
                open_papers_doi.append(paper_data["doi"])

    print("got metadata for all papers")
    # save the list of open papers to a text file
    with open(r"../dataset/papers/open_papers_doi.txt", 'w') as fp:
        for doi in open_papers_doi:
            fp.write("%s, " % doi)


if __name__ == '__main__':
    main()
