#!/usr/bin/env bash

for module in ${2}; do
  msg="Applying ops module: ${module}"
  printf -v dashes '%*s' ${#msg} ''; printf '%s\n' "${dashes// /-}" 1>&2
  echo "${msg}" 1>&2
  printf -v dashes '%*s' ${#msg} ''; printf '%s\n' "${dashes// /-}" 1>&2

  terragrunt apply \
    -auto-approve \
    --terragrunt-source-update \
    --terragrunt-non-interactive \
    --terragrunt-working-dir "${1}/${module}" \
    || exit 1;

  echo "" 1>&2
done
