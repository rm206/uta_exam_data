from dotenv import load_dotenv
import os
import requests

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

response = requests.get(f"{url}/rest/v1/buildings", headers={"apikey": key})
