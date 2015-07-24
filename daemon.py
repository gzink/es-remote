from flask import Flask
import ConfigParser
import os

dirname, filename = os.path.split(os.path.abspath(__file__))

Config = ConfigParser.ConfigParser()
Config.read(dirname + '/config.ini')

elastic_host = Config.get("main", "elastic_host")

def getNameForApiKey(apiKey):
    try:
        return Config.get("hosts", apiKey)
    except ConfigParser.NoOptionError:
        return None

app = Flask(__name__)

print getNameForApiKey("AzqhcPJ7jy0agh9xraFnRWJPAXNBmjb6z3zaBMr0")

@app.route("/<apiKey>")
def put(apiKey):
    return "Hello World!"

if __name__ == "__main__":
    app.run()
