import os
import requests
from dotenv import load_dotenv

load_dotenv("backend/.env")
api_key = os.getenv("APPSTORESPY_API_KEY")

headers = {"API-KEY": api_key, "Accept": "application/json"}
base_url = "https://api.appstorespy.com/v1"

print("--- /play/apps ---")
r1 = requests.get(f"{base_url}/play/apps", params={"q": "tiktok", "limit": 2}, headers=headers)
print(r1.status_code)
if r1.status_code == 200:
    for item in r1.json().get("data", r1.json())[:2]:
        print(item.get("bundle"), item.get("installs_exact"))

print("--- /play/search ---")
r2 = requests.get(f"{base_url}/play/search", params={"q": "tiktok", "limit": 2}, headers=headers)
print(r2.status_code)
if r2.status_code == 200:
    for item in r2.json().get("data", r2.json())[:2]:
        print(item.get("bundle"), item.get("installs_exact"))

