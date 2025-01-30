
import os
import requests
from datetime import datetime
import pytz

api_address = os.getenv('API_ADDRESS', 'localhost')
api_port = os.getenv('API_PORT', '8000')

users = [
    {"username": "alice", "password": "wonderland"},
    {"username": "bob", "password": "builder"}
]

def test_authorization():
    output = ''
    tz = pytz.timezone('Europe/Berlin')
    current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    
    all_tests_passed = True

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
            if test_status == 'FAILURE':
                all_tests_passed = False

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
    
    # # Write test status to shared file
    # os.makedirs('/app/logs', exist_ok=True)
    # with open('/app/logs/test_status.log', 'a') as status_file:
    #     status_file.write(f"authorization: {'SUCCESS' if all_tests_passed else 'FAILURE'}\n")

    # Print and write output
    print(output)
    if os.getenv('LOG') == '1':
        with open('/app/logs/api_test.log', 'a') as file:
            file.write(output)

if __name__ == "__main__":
    test_authorization()