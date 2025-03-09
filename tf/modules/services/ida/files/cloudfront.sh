#!/bin/bash
set -e

query=$( \
  aws cloudfront list-distributions \
  --query "DistributionList.Items[0].{arn: ARN, domain: DomainName, id: Id}" \
  --output json \
)

echo "${query}";
