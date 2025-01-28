# test_authorization.py
import os
import requests
from datetime import datetime
import pytz

# Use the container name "fastapi_container" instead of "api"
# api_address = 'localhost'  # Docker container name
# api_port = 8000
api_address = os.getenv('API_ADDRESS', 'localhost')  # Default: localhost
api_port = os.getenv('API_PORT', '8000')  # Default: 8000

# Define the users and their passwords
users = [
    {"username": "alice", "password": "wonderland"},
    {"username": "bob", "password": "builder"}
]

# Function to test authorization
def test_authorization():
    output = ''
    tz = pytz.timezone('Europe/Berlin')
    current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    
    for user in users:
        for version in ["v1", "v2"]:
            r = requests.get(
                url=f'http://{api_address}:{api_port}/{version}/sentiment',
                params={"username": user["username"], "password": user["password"], "sentence": "test"}
            )
            status_code = r.status_code
            if user["username"] == "alice":
                expected_result = 200
            elif user["username"] == "bob" and version == "v1":
                expected_result = 200
            else:
                expected_result = 403
            
            test_status = 'SUCCESS' if status_code == expected_result else 'FAILURE'
            output += f'''
---
Authorization test {current_time}
---
request done at "/{version}/sentiment"
| username="{user['username']}"
| password="{user['password']}"
expected result = {expected_result}
actual result = {status_code}
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
    test_authorization()