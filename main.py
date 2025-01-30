# main.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

# Mock user database
users_db = {
    "alice": {"password": "wonderland", "permissions": ["v1", "v2"]},
    "bob": {"password": "builder", "permissions": ["v1"]}
}

# Models
class UserAuth(BaseModel):
    username: str
    password: str

class SentimentRequest(BaseModel):
    username: str
    password: str
    sentence: str

# Helper function to authenticate user
def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if user and user["password"] == password:
        return user
    return None

# Endpoints
@app.get("/status", summary="Return Status", description="returns 1 if the app is up")
def status():
    return {"status": 1}

@app.get("/permissions", summary="Return Permission", description="returns user permissions")
def permissions(username: str = Query(..., description="username"), password: str = Query(..., description="password")):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=403, detail="Authentication failed")
    return {"permissions": user["permissions"]}

@app.get("/v1/sentiment", summary="Return Sentiment V1", description="returns sentiment analysis using v1 model")
def sentiment_v1(username: str = Query(..., description="username"), password: str = Query(..., description="password"), sentence: str = Query(..., description="sentence")):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=403, detail="Authentication failed")
    if "v1" not in user["permissions"]:
        raise HTTPException(status_code=403, detail="Access denied")
    # Mock sentiment analysis for v1
    if "beautiful" in sentence.lower():
        return {"score": 1}
    elif "sucks" in sentence.lower():
        return {"score": -1}
    return {"score": 0}

@app.get("/v2/sentiment", summary="Return Sentiment V2", description="returns sentiment analysis using v2 model")
def sentiment_v2(username: str = Query(..., description="username"), password: str = Query(..., description="password"), sentence: str = Query(..., description="sentence")):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=403, detail="Authentication failed")
    if "v2" not in user["permissions"]:
        raise HTTPException(status_code=403, detail="Access denied")
    # Mock sentiment analysis for v2
    if "beautiful" in sentence.lower():
        return {"score": 1}
    elif "sucks" in sentence.lower():
        return {"score": -1}
    return {"score": 0}

# Test endpoints
@app.get("/test/authentication", include_in_schema=False)
def test_authentication():
    import requests
    api_address = "localhost"
    api_port = 8000
    users = [
        {"username": "alice", "password": "wonderland"},
        {"username": "bob", "password": "builder"},
        {"username": "clementine", "password": "mandarine"}
    ]
    output = ""
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
        output += f'''
---
Authentication test
---
request done at "/permissions"
| username="{user['username']}"
| password="{user['password']}"
expected result = {expected_result}
actual result = {status_code}
==> {test_status}
'''
    return {"output": output}

@app.get("/test/authorization", include_in_schema=False)
def test_authorization():
    import requests
    api_address = "localhost"
    api_port = 8000
    users = [
        {"username": "alice", "password": "wonderland"},
        {"username": "bob", "password": "builder"}
    ]
    output = ""
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
Authorization test
---
request done at "/{version}/sentiment"
| username="{user['username']}"
| password="{user['password']}"
expected result = {expected_result}
actual result = {status_code}
==> {test_status}
'''
    return {"output": output}

@app.get("/test/content", include_in_schema=False)
def test_content():
    import requests
    api_address = "localhost"
    api_port = 8000
    user = {"username": "alice", "password": "wonderland"}
    sentences = [
        {"sentence": "life is beautiful", "expected_score": 1},
        {"sentence": "that sucks", "expected_score": -1}
    ]
    output = ""
    for version in ["v1", "v2"]:
        for sentence in sentences:
            r = requests.get(
                url=f'http://{api_address}:{api_port}/{version}/sentiment',
                params={"username": user["username"], "password": user["password"], "sentence": sentence["sentence"]}
            )
            status_code = r.status_code
            score = r.json().get("score")
            expected_score = sentence["expected_score"]
            test_status = 'SUCCESS' if score == expected_score else 'FAILURE'
            output += f'''
---
Content test
---
request done at "/{version}/sentiment"
| username="{user['username']}"
| password="{user['password']}"
| sentence="{sentence['sentence']}"
expected score = {expected_score}
actual score = {score}
==> {test_status}
'''
    return {"output": output}
#uvicorn main:app --reload