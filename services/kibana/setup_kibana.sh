#!/bin/bash

KIBANA_URL="http://localhost:5601"
INDEX_PATTERN="my-logs-*"
TIME_FIELD="@timestamp"
INITIAL_WAIT=10
RETRY_INTERVAL=10
MAX_RETRIES=5

check_kibana_status() {
  # make a request to kibana status endpoint, writing response code to stdout
  status=$(curl -s -o /dev/null -w "%{http_code}" "$KIBANA_URL/api/status")
  if [ "$status" -eq 200 ]; then
    return 0
  else
    return 1
  fi
}

/usr/local/bin/kibana-docker &

sleep $INITIAL_WAIT

for ((i=1; i<=MAX_RETRIES; i++)); do
  if check_kibana_status; then
    echo "Kibana is ready."
    break
  fi
  if [ "$i" -eq "$MAX_RETRIES" ]; then
    echo "Kibana did not become ready within the expected time."
    exit 1
  fi
  echo "Kibana is not ready yet. Retrying in $RETRY_INTERVAL seconds (Attempt $i of $MAX_RETRIES)"
  sleep $RETRY_INTERVAL
done

http_response=$(curl -s -w "\n%{http_code}" -X POST "$KIBANA_URL/api/saved_objects/index-pattern" \
    -H 'kbn-xsrf: true' \
    -H 'Content-Type: application/json' \
    -d "{
    \"attributes\": {
      \"title\": \"$INDEX_PATTERN\",
      \"timeFieldName\": \"$TIME_FIELD\"
    }
  }")

http_code=$(echo "$http_response" | tail -n1)
response_body=$(echo "$http_response" | sed '$d')

if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
    echo "Index pattern '$INDEX_PATTERN' ready."
else
    echo "Failed to setup index pattern. HTTP status code: $http_code"
    echo "Response: $response_body"
    exit 1
fi

wait