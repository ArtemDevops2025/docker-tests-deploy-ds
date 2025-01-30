#!/bin/bash

docker-compose down
# Optional
mkdir -p ./logs
chmod -R 777 ./logs

> ./logs/api_test.log

docker-compose build
docker-compose up --abort-on-container-exit

#------------For debug--------------------------
#echo "=== Test Authentication Logs ==="
#docker logs test_authentication_container

#echo "=== Test Authorization Logs ==="
#docker logs test_authorization_container

#echo "=== Test Content Logs ==="
#docker logs test_content_container

#echo "=== Summary Log ==="
docker logs summary_container