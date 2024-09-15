import os

from absl import app, flags

from ai.openai.query import run_file_search_and_store_results
from utils.file_manager import file_search_query_example

FLAGS = flags.FLAGS
flags.DEFINE_string(
    name="input_files",
    default=None,
    required=False,
    help="Source files to process on. "
         "Multiple files can be provided and they are seperated by a comma \",\" character. "
         "File inputs can be expressed as a path to a single file or a regex."
)
flags.DEFINE_string(
    name="output_file",
    default=None,
    required=False,
    help="Path of the file that the results will be written to. "
         "Input must be a file path to a single file. "
         "Supported file formate are \".csv\", \".xlsx\", and \".json\"."
)
flags.DEFINE_string(
    name="file_search_query",
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
flags.DEFINE_string(
    name="open_ai_api_key",
    default=None,
    required=False,
    help="API key for OpenAI, necessary for file search functionalities. "
         "Alternative way to provide the API key is to set as \"OPEN_AI_API_KEY\" environment variable."
)


def main(_):
    if FLAGS.file_search_query:
        if not FLAGS.input_files:
            print("Source directory not provided.")
            exit(1)

        if not FLAGS.output_file:
            print("Destination directory not provided.")
            exit(1)

        open_ai_api_key = None

        if FLAGS.open_ai_api_key:
            open_ai_api_key = FLAGS.open_ai_api_key
        elif os.getenv("OPEN_AI_API_KEY"):
            open_ai_api_key = os.getenv("OPEN_AI_API_KEY")

        if not open_ai_api_key:
            print("OpenAI API key not provided.")
            exit(1)

        print("Starting file search process.")

        exit_code = run_file_search_and_store_results(
            open_ai_api_key=open_ai_api_key,
            input_files=FLAGS.input_files,
            output_file=FLAGS.output_file,
            file_search_query=FLAGS.file_search_query,
        )

        exit(exit_code)
    else:
        print("Type \"lm --help\" for additional info.")
        exit(1)


if __name__ == "__main__":
    app.run(main)
