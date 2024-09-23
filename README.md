File search tools using OpenAI Assistant
===========================

Work in progress, still trying polish a few features and getting some initial feedback.

## Installation (pip)

```bash
pip install lumei
```

## Usage

### Example

The following is an example of processing a list of pdf files and extracting the vendor and price data from the files.
The command requires an OpenAI API key which can be obtained from here https://platform.openai.com/account/api-keys.

```bash
lumei \
  --input-files ~/folder_1/*.pdf,~/folder_2/*.pdf \
  --output-file ~/output.json \
  --openai-api-key=<OPENAI_API_KEY> \
  --query="[
  	{'name': 'vendor', 'search': 'Name of the vendor who issued the invoice.'}, 
  	{'name': 'price', 'search': 'Total bill from the invoice.'},
  	{'name': 'file path', 'attribute': 'FILE_PATH'}
  ]"
```

### Input Parameters

#### --input-files

Source files to process on. 
Multiple files can be provided, and they are seperated by a comma "," character. 
File inputs can be expressed as a path to a single file or a regex.

#### --output-file

Path of the file that the results will be written to.
Input must be a file path to a single file.
Supported file formate are ".csv", ".xlsx", and ".json".
Output file will only be written to when all results have been obtained.

#### --openai-api-key [Optional]

API key for OpenAI, necessary for file search functionalities. 
Key can be obtained from here https://platform.openai.com/account/api-keys.

Alternative way to provide the API key is to set it as the "OPENAI_API_KEY" environment variable.

#### --query

Name and the description of data to search for.
Input should be an array of JSON objects.
`name` is the name of the data to search for. Name of the data will be the column name for the result dataset.
`search` is the description of the data to search for. 
`attribute` is a piece metadata related to the query, list of possible attributes can be found below.

Example:
```
[
    {
        'name': 'vendor', 
        'search': 'Name of the vendor who issued the invoice.'
    }, 
    {
        'name': 'price', 
        'search': 'Total bill from the invoice.'
    },
    {
        'name': 'file path', 
        'attribute': 'FILE_PATH'
    }
]
```

###### Possible Attributes
`FILE_PATH`, `START_TIMESTAMP`, `END_TIMESTAMP`, `START_DATETIME`, `END_DATETIME`

### Standalone Methods

#### openai_file_search

Example of using the file search method directly without CLI.

```python
from lumei import openai_file_search
from typing import Optional

results: Optional[dict[str, str]] = openai_file_search(
  openai_api_key="<OPENAI_API_KEY>",
  input_file_path="~/example_invoice_file.pdf",
  file_search_query={
    "vendor": "Name of the vendor who issued the invoice.",
    "price": "Total bill from the invoice.",
  }
)
```
