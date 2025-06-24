import streamlit as st
import weaviate
from weaviate.classes.init import Auth
from sentence_transformers import SentenceTransformer
import os
import toml
import atexit

# Load secrets for local dev
secrets = toml.load(".streamlit/secrets.toml")
os.environ.update(secrets)

# --- Streamlit UI ---
st.set_page_config(page_title="Steam Review Search", layout="centered")
st.title("🎮 Steam Review Semantic Search")
st.write("Enter a search query to find relevant reviews.")

query = st.text_input("Your search query:")
num_results = st.slider("Number of results to show", min_value=1, max_value=20, value=5)

# --- Connect to Weaviate ---
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.environ["WEAVIATE_URL"],
    auth_credentials=Auth.api_key(os.environ["WEAVIATE_API_KEY"]),
)

# --- Embed Query ---
model = SentenceTransformer("all-MiniLM-L6-v2", device='cpu')

if query:
    query_vector = model.encode(query).tolist()

    collection = client.collections.get("SteamReview")
    results = collection.query.near_vector(
        near_vector=query_vector,
        limit=num_results
    )

    st.subheader("🔍 Search Results:")
    for obj in results.objects:
        st.markdown(f"**Review:** {obj.properties['review']}")
        st.markdown("---")


atexit.register(client.close)