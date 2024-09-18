import argparse
import os

from lumei.ai.openai.query import run_file_search_and_store_results
from lumei.utils.file_manager import file_search_query_example

parser = argparse.ArgumentParser(description='Lumei file search processor')

parser.add_argument(
    "--input-files",
    default=None,
    required=False,
    help="Source files to process on. "
         "Multiple files can be provided and they are seperated by a comma \",\" character. "
         "File inputs can be expressed as a path to a single file or a regex."
)
parser.add_argument(
    "--output-file",
    default=None,
    required=False,
    help="Path of the file that the results will be written to. "
         "Input must be a file path to a single file. "
         "Supported file formate are \".csv\", \".xlsx\", and \".json\"."
)
parser.add_argument(
    "--openai-api-key",
    default=None,
    required=False,
    help="API key for OpenAI, necessary for file search functionalities. "
         "Alternative way to provide the API key is to set as \"OPENAI_API_KEY\" environment variable."
)
parser.add_argument(
    "--file-search-query",
    default=None,
    required=False,
    help="Name and description of data to search for. "
         "Input should be an array of JSON objects."
         "Name of the data to search for is the key. Name of the data will be the column name for the result dataset. "
         "The description of the data to search is the value."
         "\n\n"
         "Example:"
         f"{file_search_query_example}"
)
args = parser.parse_args()


def main():
    if args.file_search_query:
        if not args.input_files:
            print("Source directory not provided.")
            exit(1)

        if not args.output_file:
            print("Destination directory not provided.")
            exit(1)

        openai_api_key = None

        if args.openai_api_key:
            openai_api_key = args.openai_api_key
        elif os.getenv("OPEN_AI_API_KEY"):
            openai_api_key = os.getenv("OPENAI_API_KEY")

        if not openai_api_key:
            print("OpenAI API key not provided.")
            exit(1)

        print("Starting file search process.")

        exit_code = run_file_search_and_store_results(
            openai_api_key=openai_api_key,
            input_files=args.input_files,
            output_file=args.output_file,
            file_search_query=args.file_search_query,
        )

        exit(exit_code)
    else:
        print("Type \"lumei --help\" for additional info.")
        exit(1)


if __name__ == '__main__':
  main()
