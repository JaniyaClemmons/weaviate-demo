
from pymongo import MongoClient
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Property, DataType
from sentence_transformers import SentenceTransformer
import streamlit as st
import toml
import os
secrets = toml.load(".streamlit/secrets.toml")
os.environ.update(secrets)

# --- MongoDB Setup ---
mongo_uri = os.environ["MONGO_URI"]
print(mongo_uri)
client = MongoClient(mongo_uri)
db = client["steamdb"]
collection = db["reviews"]

# --- Load data, only english reviews ---
documents = list(collection.find(
    {"language": "english"},
    {"_id": 0, "review": 1}
))
documents = [doc for doc in documents if doc.get("review", "").strip()]

# --- Embeddings ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Weaviate Setup ---
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
)

# --- Create collection if absent ---
if not client.collections.exists("SteamReview"):
    client.collections.create(
        name="SteamReview",
        properties=[
            Property(name="review", data_type=DataType.TEXT),
        ],
    )

# --- Insert data ---
reviews = client.collections.get("SteamReview")
for doc in documents:
    text = doc["review"]
    embedding = model.encode(text).tolist()
    reviews.data.insert(properties={"review": text}, vector=embedding)

print(f"✅ Imported {len(documents)} documents into Weaviate.")


