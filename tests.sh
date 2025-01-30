#!/bin/bash

pip install pytz requests

status_response=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/status)
if [ "$status_response" -ne 200 ]; then
    echo "----------------------------"
    echo "Error! Check if FastAPI runs!"
    echo "----------------------------"
    exit 1
else
    echo "----------------------------"
    echo "Status Api OK, you can work!"
    echo "----------------------------"
fi

run_test() {
    test_script=$1
    output=$(python3 $test_script)
    echo "$output"
    
    if echo "$output" | grep -q "==> FAILURE"; then
        echo "FAILURE: $test_script"
        return 1
    else
        echo "SUCCESS: $test_script"
        return 0
    fi
}

run_test test_authentication.py
auth_result=$?

run_test test_authorization.py
authz_result=$?

run_test test_content.py
content_result=$?

if [ $auth_result -eq 0 ] && [ $authz_result -eq 0 ] && [ $content_result -eq 0 ]; then
    echo "All tests passed successfully."
else
    echo "Error: Some tests failed."
fi