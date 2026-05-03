# AWS CloudFormation Templates — WebApp sample (fixture)

This directory vendors a **reference CloudFormation template** used to stress-test substrate schema shapes (large single-template stacks: S3, CloudFront, WAFv2, API Gateway, Cognito, Lambda, DynamoDB).

## Source

- **Upstream**: [Solutions/WebApp/webapp.yaml](https://github.com/aws-cloudformation/aws-cloudformation-templates/blob/main/Solutions/WebApp/webapp.yaml)
- **License**: Apache-2.0 (see [repository license](https://github.com/aws-cloudformation/aws-cloudformation-templates/blob/main/LICENSE.txt))

## Purpose in this repo

- **Phase 5**: validates that seed/bundle metadata and CloudFormation extension schemas can describe a real, complex template without schema changes driven only by this sample.
- **Not authoritative**: substrate contracts are defined by ADRs under `adrs/`; this fixture is optional example material.

## Files

| File | Description |
|------|-------------|
| `webapp.yaml` | Upstream template (single stack). |
| `substrate-seed-metadata.example.json` | Example **substrate seed** document pointing at `webapp.yaml` (passes `seed.schema.json` + `cloudformation/seed-extension.schema.json` composed validation). |
| `mutation-rules.example.yaml` | Example logical-ID mutation-rules sidecar (`schemas/mutation-rules.schema.json`). |

Do **not** deploy this template in production without review; upstream warns that resources may incur charges.
