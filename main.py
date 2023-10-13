import argparse
import os
from paper_data_extractor import mine_paper


def main():
    print("Starting...")
    parser = argparse.ArgumentParser(description="Extract data from a given PDF using the paper_data_extractor module.")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file to extract data from.")

    # Make fake an optional flag
    parser.add_argument("--fake", action="store_true",
                        help="Flag that indicates if model is fake or not. If present, model is considered fake.")

    args = parser.parse_args()
    results_dir = 'results/'

    if not os.path.exists(args.pdf_path):
        print(f"Error: The file '{args.pdf_path}' does not exist.")
        return

    csv_filename = (os.path.basename(args.pdf_path)[:-4] + '_api_results.csv')

    mine_paper(args.pdf_path, fake=args.fake)

    print(f"Data extracted and saved to: {os.path.join(results_dir, csv_filename)}")


if __name__ == "__main__":
    main()
