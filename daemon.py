import ConfigParser, datetime, json, os
from flask import Flask, request
from elasticsearch import Elasticsearch
from elasticsearch import helpers

dirname, filename = os.path.split(os.path.abspath(__file__))

Config = ConfigParser.ConfigParser()
Config.read(dirname + '/config.ini')

elastic_host = Config.get("main", "elastic_host")

es = Elasticsearch(elastic_host)

def getNameForApiKey(apiKey):
    try:
        return Config.get("hosts", apiKey)
    except ConfigParser.NoOptionError:
        return None

app = Flask(__name__)
app.debug = True

print getNameForApiKey("")

@app.route("/<apiKey>", methods=['POST'])
def put(apiKey):
    now = datetime.datetime.now()
    try:
        decoded = json.loads(request.stream.read())
    except ValueError:
        return json.dumps({"error": "invalid json message"})
    return "Hello World!"

if __name__ == "__main__":
    app.run()
