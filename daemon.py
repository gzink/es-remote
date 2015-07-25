import ConfigParser, datetime, json, os, pytz
from flask import Flask, request
from elasticsearch import Elasticsearch
from elasticsearch import helpers

dirname, filename = os.path.split(os.path.abspath(__file__))

Config = ConfigParser.ConfigParser()
Config.read(dirname + '/config.ini')

elastic_host = Config.get("main", "elastic_host")
elastic_index_name = Config.get("main", "elastic_index_prefix")
elastic_show_name = Config.get("main", "elastic_show_name")

es = Elasticsearch(elastic_host)

def getNameForApiKey(apiKey):
    try:
        return Config.get("hosts", apiKey)
    except ConfigParser.NoOptionError:
        return None

app = Flask(__name__)
app.debug = True

print getNameForApiKey("")

@app.route("/<apiKey>/<_type>", methods=['POST'])
def put(apiKey, _type):
    now = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
    name = getNameForApiKey(apiKey)
    if name is None:
        return json.dumps({"error": "invalid api key"})
    try:
        decoded = json.loads(request.stream.read())
    except ValueError:
        return json.dumps({"error": "invalid json message"})
    index = elastic_index_name + '-' + now.strftime('%Y-%m-%d')

    if type(decoded) is dict:
        decoded = [decoded]

    for row in decoded:
        row['@timestamp'] = now
        row['_index'] = index
        row['_type'] = _type
        if elastic_show_name:
            row['name'] = name

    print helpers.bulk(es, decoded)

    return "Hello World!"

if __name__ == "__main__":
    app.run()
