
import os
import requests
from datetime import datetime
import pytz

api_address = os.getenv('API_ADDRESS', 'localhost')
api_port = os.getenv('API_PORT', '8000')

user = {"username": "alice", "password": "wonderland"}
sentences = [
    {"sentence": "life is beautiful", "expected_score": 1},
    {"sentence": "that sucks", "expected_score": -1}
]

def test_content():
    output = ''
    tz = pytz.timezone('Europe/Berlin')
    current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    
    all_tests_passed = True

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
            
            if test_status == 'FAILURE':
                all_tests_passed = False

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
    
    # # Write test status to shared file
    # os.makedirs('/app/logs', exist_ok=True)
    # with open('/app/logs/test_status.log', 'a') as status_file:
    #     status_file.write(f"content: {'SUCCESS' if all_tests_passed else 'FAILURE'}\n")

    # Print and write output
    print(output)
    if os.getenv('LOG') == '1':
        with open('/app/logs/api_test.log', 'a') as file:
            file.write(output)

if __name__ == "__main__":
    test_content()