#!/usr/bin/env bash

if [ "${IAMLIVE}" = 'true' ]; then
  BIND_IP='0.0.0.0'
  OUTPUT_FILE='/opt/tf/policy.json'
  export AWS_CSM_ENABLED=true
  export AWS_CSM_HOST="${BIND_IP}"
  export AWS_CSM_PORT=31000

  (iamlive \
    --mode csm \
    --output-file "${OUTPUT_FILE}" \
    --set-ini \
    --sort-alphabetical \
    > /dev/null &)

  "${@}"

  sleep 1
  pkill iamlive
  sleep 1

  echo ""
  printf "\033[0;32m%-6s\033[0m\n" 'AWS PERMISSIONS USED:'
  cat "${OUTPUT_FILE}"
  echo ""
else
  "${@}"
fi
