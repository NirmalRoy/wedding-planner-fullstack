import requests
import subprocess

# Get access token using subprocess with full path
result = subprocess.run(
    ["C:\\Users\\User\\AppData\\Local\\Google\\Cloud SDK\\google-cloud-sdk\\bin\\gcloud.cmd", "auth", "print-access-token"],
    capture_output=True,
    text=True,
    check=True
)
access_token = result.stdout.strip()

# API endpoint for textembedding-gecko
url = "https://us-central1-aiplatform.googleapis.com/v1/projects/nirmal-maven/locations/us-central1/publishers/google/models/textembedding-gecko:predict"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
payload = {
    "instances": [{"content": "Test venue description"}]
}

# Make the request
response = requests.post(url, json=payload, headers=headers)
if response.status_code == 200:
    embedding = response.json()["predictions"][0]["embeddings"]["values"]
    print(f"Embedding length: {len(embedding)}")
    print(f"First few values: {embedding[:5]}")
else:
    print(f"Error: {response.text}")