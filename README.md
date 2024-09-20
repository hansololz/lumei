File search tools using OpenAI Assistant
===========================

Work in progress, still trying polish a few features and getting some initial feedback.

## Installation (pip)

    pip install lumei

## Usage

### Example

The following is an example of processing a list of pdf files and extracting the vendor and price data from the files.
The command requires an OpenAI API key which can be obtained from here https://platform.openai.com/account/api-keys.

```
lumei \
  --input-files ~/folder_1/*.pdf,~/folder_2/*.pdf \
  --output-file ~/Desktop/output.json \
  --openai-api-key=<OPENAI_API_KEY> \
  --query="[
  	{'name': 'vendor', 'search': 'Name of the vendor who issued the invoice.'}, 
  	{'name': 'price', 'search': 'Total bill from the invoice.'}
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

#### --openai-api-key [Optional]

API key for OpenAI, necessary for file search functionalities. 
Key can be obtained from here https://platform.openai.com/account/api-keys.

Alternative way to provide the API key is to set it as the "OPENAI_API_KEY" environment variable.

#### --query

Name and the description of data to search for.
Input should be an array of JSON objects.
`name` is the name of the data to search for. Name of the data will be the column name for the result dataset.
`search` is the description of the data to search for.

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
    }
]
```