#!/bin/sh

KIBANA_URL="http://localhost:5601"

status=$(curl -s -o /dev/null -w "%{http_code}" "$KIBANA_URL/api/status")
[ "$status" -eq 200 ] || exit 1
