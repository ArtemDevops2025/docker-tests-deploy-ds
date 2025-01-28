# test_content.py
import os
import requests
from datetime import datetime
import pytz

# Use the container name "fastapi_container" instead of "api"
# api_address = 'localhost'  # Docker container name
# api_port = 8000
api_address = os.getenv('API_ADDRESS', 'localhost')  # Default: localhost
api_port = os.getenv('API_PORT', '8000')  # Default: 8000

# Define the user and their password
user = {"username": "alice", "password": "wonderland"}

# Define the sentences to test
sentences = [
    {"sentence": "life is beautiful", "expected_score": 1},
    {"sentence": "that sucks", "expected_score": -1}
]

# Function to test content
def test_content():
    output = ''
    tz = pytz.timezone('Europe/Berlin')
    current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    
    for version in ["v1", "v2"]:
        for sentence in sentences:
            r = requests.get(
                url=f'http://{api_address}:{api_port}/{version}/sentiment',
                params={"username": user["username"], "password": user["password"], "sentence": sentence["sentence"]}
            )
            status_code = r.status_code
            if status_code == 200:
                score = r.json().get("score")
                expected_score = sentence["expected_score"]
                if (expected_score == 1 and score > 0) or (expected_score == -1 and score < 0):
                    test_status = 'SUCCESS'
                else:
                    test_status = 'FAILURE'
            else:
                score = None
                test_status = 'FAILURE'
            
            output += f'''
---
Content test {current_time}
---
request done at "/{version}/sentiment"
| username="{user['username']}"
| password="{user['password']}"
| sentence="{sentence['sentence']}"
expected score = {expected_score}
actual score = {score}
==> {test_status}
'''
    
    print(output)
    
    if os.getenv('LOG') == '1':
        # Ensure the logs directory exists
        os.makedirs('/app/logs', exist_ok=True)
        #os.makedirs('/app/logs', exist_ok=True)
        with open('/app/logs/api_test.log', 'a') as file:
            file.write(output)

if __name__ == "__main__":
    test_content()