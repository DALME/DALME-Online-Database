#!/usr/bin/env bash
set -e

error_handler() {
  echo "Error encountered while applying dependency graph" >&2
  exit 1
}

trap 'error_handler' ERR

for module in ${2}; do
  msg="Applying ops module: ${module}"
  printf -v dashes '%*s' ${#msg} ''; printf '%s\n' "${dashes// /-}" 1>&2
  echo "${msg}" 1>&2
  printf -v dashes '%*s' ${#msg} ''; printf '%s\n' "${dashes// /-}" 1>&2

  terragrunt apply \
    -auto-approve \
    --terragrunt-source-update \
    --terragrunt-non-interactive \
    --terragrunt-working-dir "${1}/${module}"

  echo "" 1>&2
done
