#!/usr/bin/env bash
set -eou pipefail

usage() {
  cat <<EOF
Deploy a new ECS service revision and wait for it to stabilise.
Usage: $0 [options]

Required:
  --cluster  <value>   ECS cluster name
  --service  <value>   ECS service name
  --task     <value>   Task definition family name

Optional:
  -h, --help           Show this help and exit
EOF
}

if [[ $# -eq 0 ]]; then
  usage >&2
  exit 1
fi

cluster=""
service=""
task_family=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cluster)
      cluster="$2"
      shift 2
      ;;
    --service)
      service="$2"
      shift 2
      ;;
    --task)
      task_family="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Invalid option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [ -z "${cluster}" ] || [ -z "${service}" ] || [ -z "${task_family}" ]; then
  usage >&2
  exit 1
fi

echo "Fetching current task definition: ${task_family}" >&2
task_def=$(aws ecs describe-task-definition \
  --task-definition "${task_family}" \
  --query 'taskDefinition' \
  --output json)

echo "Registering new task definition revision" >&2
tmp=$(mktemp)
trap 'rm -f "${tmp}"' EXIT
echo "${task_def}" | python3 -c "
import json, sys
td = json.load(sys.stdin)
for key in ['taskDefinitionArn', 'revision', 'status', 'requiresAttributes',
            'compatibilities', 'registeredAt', 'registeredBy', 'deregisteredAt']:
    td.pop(key, None)
print(json.dumps(td))
" > "${tmp}"
new_task_def_arn=$(aws ecs register-task-definition \
    --cli-input-json "file://${tmp}" \
    --query 'taskDefinition.taskDefinitionArn' \
    --output text)

echo "Registered: ${new_task_def_arn}" >&2

echo "Updating service: ${service}" >&2
aws ecs update-service \
  --cluster "${cluster}" \
  --service "${service}" \
  --task-definition "${new_task_def_arn}" \
  --output json > /dev/null

echo "Waiting for service to stabilise..." >&2
timeout=900
interval=15
elapsed=0
while [ "${elapsed}" -lt "${timeout}" ]; do
  state=$(aws ecs describe-services \
    --cluster "${cluster}" \
    --services "${service}" \
    --query 'services[0].deployments[?status==`PRIMARY`].[rolloutState,taskDefinition]' \
    --output text)

  rollout_state=$(echo "${state}" | awk '{print $1}')
  active_task_def=$(echo "${state}" | awk '{print $2}')

  if [ "${rollout_state}" = "COMPLETED" ]; then
    if [ "${active_task_def}" = "${new_task_def_arn}" ]; then
      echo "Deploy complete." >&2
      exit 0
    else
      echo "Deployment rolled back to previous revision. Active: ${active_task_def}" >&2
      exit 1
    fi
  fi

  if [ "${rollout_state}" = "FAILED" ]; then
    echo "Deployment rollout failed." >&2
    exit 1
  fi

  echo "  rolloutState=${rollout_state} (${elapsed}s elapsed)" >&2
  sleep "${interval}"
  elapsed=$((elapsed + interval))
done

echo "Timed out after ${timeout}s waiting for service to stabilise." >&2
exit 1
