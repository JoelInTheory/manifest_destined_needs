from flask import Flask
from flask_restful import Api

import requests
import json
import lxml.etree as ET

import os
from sys import exit

url = os.environ.get('MANIFEST_URL')
# [{'xpath': <xpath>,
#   'attrib': <attrib to change>,
#   'newvalue': <newvalue for attrib @ xpath>}]
filter_json = json.loads(os.environ.get('FILTER_JSON'))


if not url:
    sys.exit() 

app = Flask(__name__)
api = Api(app)

def get_manifest(url):
    r = requests.get(url)
    headers = r.headers.items()
    xmlr = ET.fromstring(r.content)
    return xmlr, headers

@app.route("/manifest.xml", methods=["GET"])
def respond_with_manifest(url = url):
    xmlr, headers = get_manifest(url)
    for fjson in filter_json:
        xpath = fjson['xpath']
        attrib = fjson['attrib']
        newvalue = fjson['newvalue']
        xmlr.xpath(xpath)[0].attrib[attrib] = newvalue
    return ET.tostring(xmlr), 200, headers

if __name__ == '__main__':
    x = ManApp()
