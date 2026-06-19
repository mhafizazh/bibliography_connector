# Project Structure
```
bibliography_connector/
│
├── bibliography_connector/
│   ├── cli/
│   │   └── __init__.py
│   │   └── cmd_sync.py
│   │   └── main.py
│   ├── providers/
│   │   └── zotero.py
│   │
│   ├── exporters/
│   │   └── hugo.py
│   │
│   └── pipeline.py
│
├── pyproject.toml
└── README.md
```

# Usage
Create virtual environment
```
python3 -m venv venv
```
activate virtual environment 
```
source venv/bin/activate
```
install dependencies
```
pip install .
```

run sync all command 
```
bibliography_connector sync all --groupid 2914042 --collectionid FSK5IX4F --outdir ./output
```
expected output 
```
Fetching bibliography...
Fetched 479 items
Processed 392 items
```
run sync year XXXX
```
bibliography_connector sync year 1999 --groupid 2914042 --collectionid FSK5IX4F --outdir ./1999_output
```


# Note
This is just initial proof of concept