from pymongo import MongoClient
import argparse
from pymongo.errors import (OperationFailure, ServerSelectionTimeoutError,
                            ConnectionFailure, ConfigurationError)
import xml.etree.ElementTree as ET
import logging

global output_file


def xml_parse(xml_file):

    with open(xml_file) as f:
        tree = ET.parse(f)
        root = tree.getroot()
        ips = [
            elem.attrib['addr'] for elem in (root.iter())
            if elem.tag == 'address'
        ]
    return ips


def get_collections(ip, db):
    client = MongoClient(ip, 27017, serverSelectionTimeoutMS=30000)
    output = []
    for collection in client[db].list_collection_names():
        output.append(
            f"get_one_document('{ip}', '{db}', '{collection}'):{client[db][collection].estimated_document_count()}"
        )
    return output


def get_one_document(ip, db, collection):
    client = MongoClient(ip, 27017, serverSelectionTimeoutMS=30000, connect=False)
    print(f"c = MongoClient('{ip}', 27017)")
    print(f"{collection} = c['{db}']['{collection}'].find()\n")
    return client[db][collection].find_one()


def check_mongo_server(ip, port=27017):
    client = MongoClient(ip, port, serverSelectionTimeoutMS=1000)
    try:
        databases = client.list_database_names()
        print(f'Open Mongo Server: {ip} --> {databases}')
    except OperationFailure:
        print(f'Auth required: {ip}')


def main(ips):

    count = 0
    for ip in ips:
        client = MongoClient(ip, port, serverSelectionTimeoutMS=1000)
        client.server_selection_timeout
        try:
            print(f"Now processing {ip}")
            databases = client.list_database_names()
            print(f"\nOpen mongodb server found at : {ip}")
            count = count + 1
            for database in databases:
                db = client[database]
                objects = db.command('dbstats')['objects']
                logging.info(
                    f"Database '{database}' found on server {ip} with {objects} objects"
                )
                parse_mongo_server(ip, database, objects, output_file)
        except (ConnectionFailure, OperationFailure,
                ServerSelectionTimeoutError, ConfigurationError,
                KeyError) as e:
            logging.error(f"Unable to connect to server {ip}")
            pass

        client.close()
    return count


def parse_mongo_server(ip, database, objects, output_file):

    with open(output_file, 'a') as f:
        f.write(f"get_collections('{ip}', '{database}'):{objects}\n")
        try:
            output = get_collections(ip, database)
            [f.write(i + '\n') for i in output]
            logging.info(f"Details for {database} at {ip} written to file.")
        except:
            pass

    f.close()
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-x",
                        "--xml-file",
                        help="Masscan output file in XML format",
                        dest="xml_file",
                        required=True)
    args = parser.parse_args()

    xml_file = args.xml_file

    logfile = xml_file.split('.x')[0] + '.log'
    output_file = xml_file.split('.x')[0] + '.csv'

    logging.basicConfig(filename=logfile,
                        filemode='w',
                        format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    count = 0
    port = 27017

    ips = xml_parse(xml_file)
    main(ips)
