from mongo_connection import get_mongo_client

def test_connection():
    client = get_mongo_client()
    try:
        # The 'admin' command 'ping' is a simple way to check connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
    except Exception as e:
        print("❌ Failed to connect to MongoDB:", e)

if __name__ == "__main__":
    test_connection() 