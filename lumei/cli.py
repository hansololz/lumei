import argparse
import os

from lumei.query_executor import execute_query_and_store_results

parser = argparse.ArgumentParser(description='Lumei file processor')

parser.add_argument(
    "--input-files",
    default=None,
    required=True,
    help="Source files to process on. "
         "Multiple files can be provided and they are seperated by a comma `,` character. "
         "File inputs can be expressed as a path to a single file or a regex."
)
parser.add_argument(
    "--output-file",
    default=None,
    required=True,
    help="Path of the file that the results will be written to. "
         "Input must be a file path to a single file. "
         "Supported file formate are `.csv`, `.xlsx`, and `.json`."
)
parser.add_argument(
    "--openai-api-key",
    default=None,
    required=True,
    help="API key for OpenAI, necessary for file search functionalities. "
         "Key can be obtained from here https://platform.openai.com/account/api-keys.\n\n"
         "Alternative way to provide the API key is to set it as the `OPENAI_API_KEY` environment variable."
)
parser.add_argument(
    "--query",
    default=None,
    required=True,
    help="Name and description of data to search for. "
         "Input should be an array of JSON objects. "
         "`name` is the name of the data to search for. "
         "Name of the data will be the column name for the result dataset. "
         "`search` is the description of the data to search for."
)
args = parser.parse_args()


def main():
    if args.openai_api_key:
        openai_api_key = args.openai_api_key
    elif os.getenv("OPENAI_API_KEY"):
        openai_api_key = os.getenv("OPENAI_API_KEY")
    else:
        openai_api_key = None

    if not openai_api_key:
        print("OpenAI API key not provided.")
        exit(1)

    print("Starting file search process.")

    exit_code = execute_query_and_store_results(
        input_files=args.input_files,
        output_file=args.output_file,
        openai_api_key=openai_api_key,
        file_search_query_string=args.query,
    )

    exit(exit_code)
