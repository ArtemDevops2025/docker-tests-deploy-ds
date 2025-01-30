import os
import requests
from datetime import datetime
import pytz

api_address = os.getenv('API_ADDRESS', 'localhost')
api_port = os.getenv('API_PORT', '8000')

users = [
    {"username": "alice", "password": "wonderland"},
    {"username": "bob", "password": "builder"},
    {"username": "clementine", "password": "mandarine"}
   # {"username": "alice", "password": "wonderland1"},   for negative case
]

def test_authentication():
    output = ''
    tz = pytz.timezone('Europe/Berlin')
    current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    
    all_tests_passed = True

    for user in users:
        r = requests.get(
            url=f'http://{api_address}:{api_port}/permissions',
            params=user
        )
        status_code = r.status_code
        if user["username"] in ["alice", "bob"]:
            expected_result = 200
        else:
            expected_result = 403
        
        test_status = 'SUCCESS' if status_code == expected_result else 'FAILURE'
        if test_status == 'FAILURE':
            all_tests_passed = False

        output += f'''
---
Authentication test {current_time}
---
request done at "/permissions"
| username="{user['username']}"
| password="{user['password']}"
expected result = {expected_result}
actual result = {status_code}
==> {test_status}
'''
    
    print(output)
    if os.getenv('LOG') == '1':
        os.makedirs('/app/logs', exist_ok=True)
        with open('/app/logs/api_test.log', 'a') as file:
            file.write(output)

if __name__ == "__main__":
    test_authentication()