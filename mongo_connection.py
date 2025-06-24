import os
from pymongo import MongoClient
import toml

def get_mongo_client():
    secrets = toml.load(".streamlit/secrets.toml")
    os.environ.update(secrets)
    mongo_uri = os.environ["MONGO_URI"]
    client = MongoClient(mongo_uri)
    return client 