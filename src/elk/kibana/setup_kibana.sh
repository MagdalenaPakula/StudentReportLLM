#!/bin/bash

KIBANA_URL="http://localhost:5601"
INDEX_PATTERN="my-logs-*"
TIME_FIELD="@timestamp"
RETRY_INTERVAL=5
MAX_RETRIES=12

check_kibana_status() {
  status_code=$(curl -s -o /dev/null -w "%{http_code}" "$KIBANA_URL/api/status")
  if [ "$status_code" -eq 200 ]; then
    return 0
  else
    return 1
  fi
}

echo "Waiting for Kibana to connect to Elasticsearch..."
retry_count=0

until check_kibana_status; do
  if [ "$retry_count" -ge "$MAX_RETRIES" ]; then
    echo "Kibana did not connect to Elasticsearch within the expected time."
    exit 1
  fi
  echo "Kibana is not ready yet. Retrying in $RETRY_INTERVAL seconds..."
  sleep $RETRY_INTERVAL
  retry_count=$((retry_count + 1))
done

echo "Kibana is connected to Elasticsearch."

response=$(curl -s -w "%{http_code}" -o /dev/null -X POST "$KIBANA_URL/api/saved_objects/index-pattern" \
    -H 'kbn-xsrf: true' \
    -H 'Content-Type: application/json' \
    -d "{
    \"attributes\": {
      \"title\": \"$INDEX_PATTERN\",
      \"timeFieldName\": \"$TIME_FIELD\"
    }
  }")

if [ "$response" -eq 200 ]; then
    echo "Index pattern '$INDEX_PATTERN' created successfully."
else
    echo "Failed to create index pattern. HTTP status code: $response"
fi