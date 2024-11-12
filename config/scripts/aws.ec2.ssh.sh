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
    *)
      echo "Invalid option: $1" >&2
      exit 1
      ;;
  esac
done

if [ -z "$jump_host" ] || [ -z "$profile" ] || [ -z "$region" ]; then
  echo "Usage: $0 \
    --jump_host <value> \
    --profile <value> \
    --region <value>" >&2
  exit 1
fi

filter="Name=tag:Name,Values=\"${jump_host}\""
query="Reservations[0].Instances[0].InstanceId"
instance_id=$( \
  aws ec2 describe-instances \
  --filter "${filter}" \
  --query "${query}" \
  --output text \
)

if [[ "${instance_id}" == 'None' ]]; then
  echo "No EC2 instance found named: ${jump_host}" >&2
  exit 1
else
  echo "Secure shelling into to EC2 host: ${instance_id}" >&2
  aws ssm \
    start-session \
    --profile "${profile}" \
    --region "${region}" \
    --target "${instance_id}"
fi
