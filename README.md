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
│   └── utils
│       └── date_parser.py
│
├── pyproject.toml
└── README.md
```

# Usage
Create virtual environment
```
python3 -m venv .venv
```
activate virtual environment 
```
source .venv/bin/activate
```
install dependencies
```
pip install -e .
```

run sync all command 
```
bibliography_connector sync all --groupid 6588052 --collectionid J2TGC2ZT -o .sync_all
```
expected output 
```
Fetching bibliography...
Fetched 6 items
Processed 6 items
```
Filter by year XXXX format
```
bibliography_connector sync date "2026" --groupid 6588052 --collectionid J2TGC2ZT -o .sync_2026
```
Filter by year by MM XXXX format
```
bibliography_connector sync date "May 2026" --groupid 6588052 --collectionid J2TGC2ZT -o .sync_May_2026
```
Filter by year by DD-MM-XXXX format
```
bibliography_connector sync date "16 May 2026" --groupid 6588052 --collectionid J2TGC2ZT -o .sync_16_may_2026
```


# Note
This is just initial proof of concept