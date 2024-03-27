from flask import Flask
from flask_restx import Api
import json
from json import JSONEncoder
from src.api.newspaperNs import newspaper_ns
from src.api.issueNs import issue_ns
from src.api.editorNs import editor_ns
from src.model.agency import Agency
from src.api.subscriberNs import subscriber_ns

agency = Agency()

def create_app():
    paperroute_app = Flask(__name__)
    #need to extend this class for custom objects, so that they can be jsonified

    paperroute_api = Api(paperroute_app, title="PaperBack: An App for Newspaper Issue and Subscription Management")

    # add individual namespaces
    paperroute_api.add_namespace(newspaper_ns)
    paperroute_api.add_namespace(editor_ns)
    paperroute_api.add_namespace(subscriber_ns)
    paperroute_api.add_namespace(issue_ns)
    return paperroute_app

if __name__ == '__main__':
    create_app().run(debug=False, port=7890)