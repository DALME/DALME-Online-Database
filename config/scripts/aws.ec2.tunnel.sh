#!/usr/bin/env bash

while [[ $# -gt 0 ]]; do
  case "$1" in
    --jump_host)
      jump_host="$2"
      shift 2
      ;;
    --profile)
      profile="$2"
      shift 2
      ;;
    --region)
      region="$2"
      shift 2
      ;;
    --host)
      host="$2"
      shift 2
      ;;
    --host_bind)
      host_bind="$2"
      shift 2
      ;;
    --local_bind)
      local_bind="$2"
      shift 2
      ;;
    *)
      echo "Invalid option: $1" >&2
      exit 1
      ;;
  esac
done

if [ -z "$jump_host" ] || [ -z "$profile" ] || [ -z "$region" ] || [ -z "$host" ] || [ -z "$host_bind" ] || [ -z "$local_bind" ]; then
  echo "Usage: $0 \
    --jump_host <value> \
    --profile <value> \
    --region <value> \
    --host <value> \
    --host_bind <value> \
    --local_bind <value>" >&2
  exit 1
fi

filter1="Name=tag:Name,Values=\"${jump_host}\""
filter2="Name=instance-state-name,Values=running"
query="Reservations[*].Instances[*].InstanceId"
instance_id=$( \
  aws ec2 describe-instances \
  --filter "${filter1}" \
  --filter "${filter2}" \
  --query "${query}" \
  --output text \
)

if [[ "${instance_id}" == 'None' ]]; then
  echo "No EC2 instance found named: ${jump_host}" >&2
  exit 1
else
  echo "Tunnelling to EC2 host: ${instance_id}" >&2
  echo "Forwarding ports from localhost on: ${local_bind}" >&2
  aws ssm \
    start-session \
    --profile "${profile}" \
    --region "${region}" \
    --target "${instance_id}" \
    --document-name AWS-StartPortForwardingSessionToRemoteHost \
    --parameters host="${host}",portNumber="${host_bind}",localPortNumber="${local_bind}"
fi
