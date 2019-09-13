# Python MongoDB Parser using pymongo and masscan

### Requirements

* Python 3.7+
* pymongo
* masscan

### Usage

```bash
python mongo_parser.py --help
usage: mongo_parser.py [-h] -x XML_FILE

optional arguments:
  -h, --help            show this help message and exit
  -x XML_FILE, --xml-file XML_FILE
                        Masscan output file in XML format
```

1. Use `masscan` to search an IP range for MongoDB servers.

```bash
masscan 10.0.0.0/0 -p 27017 --rate 10000 -oX mongodb_servers.xml
```

2. Use the XML output from masscan for `mongo_parser.py`

```bash
python mongo_parser.py -x mongodb_servers.xml
```
### Output
