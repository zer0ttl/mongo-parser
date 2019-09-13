# Python MongoDB Parser using pymongo and masscan

Read more about how I wrote this script at my blog below :

https://zerottl.com/posts/pwning-open-mongodb-servers-using-python/

### Requirements

* Python 3.7+
* pipenv
* pymongo
* masscan

### Installation

```bash
git clone https://github.com/zer0ttl/mongo-parser.git
cd mongo-parser/
pipenv shell
pipenv install pymongo
```
### Usage

```bash
python mongo_parser.py --help
usage: mongo_parser.py [-h] -x XML_FILE

optional arguments:
  -h, --help            show this help message and exit
  -x XML_FILE, --xml-file XML_FILE
                        Masscan output file in XML format
```

* Use `masscan` to search an IP range for MongoDB servers.

```bash
masscan 10.0.0.0/0 -p 27017 --rate 10000 -oX mongodb_servers.xml
```

* Use the XML output from masscan for `mongo_parser.py`

```bash
python mongo_parser.py -x mongodb_servers.xml
```
### Output

Output will be saved to `mongodb_servers.csv` file.

### Future enhancements

- [ ] Make this script async
