# Static Site Delivery — ADR Context

## Why this building block exists

Serving static web assets at scale on AWS requires a consistent, secure composition of
CloudFront, S3, WAF, and access logging. Each org does this slightly differently; this block
captures the opinionated baseline used in the reference-webapp pattern.

## Architecture decisions embodied

- **OAC over OAI**: Origin Access Control (sigv4) is the current AWS best practice for
  restricting S3 access to CloudFront; legacy Origin Access Identity is not used.
- **WAFv2 CLOUDFRONT scope**: WAF must be deployed in us-east-1 to associate with CloudFront;
  the block assumes this and the deploying stack must be in that region.
- **Versioning + replication**: Content bucket is versioned and replicated to a secondary
  bucket to support DR patterns and object recovery.
- **Compliance log retention**: Access log bucket uses S3 Object Lock (COMPLIANCE, 1 year)
  for immutable audit trail.
- **HTTPS-only bucket policy**: Deny all non-TLS S3 access on the content bucket.

## Constraints this block introduces

- WAF scope is `CLOUDFRONT`; stack must be in us-east-1.
- `SiteContentBucket.BucketName` encodes `${AppName}-content-${Region}-${AccountId}`;
  name cannot change after creation (CloudFormation replacement = new empty bucket).
- `SiteContentBucketPolicy` references `SiteDistribution.Id` — distribution must be in
  the same stack or this bundle used in a seed that provides both.

## Trade-offs accepted

- Single CloudFront default cache behaviour (no path-based routing to multiple origins).
  Extend the distribution separately rather than modifying this block.
- Default CloudFront certificate (no custom domain). Consumers add `Aliases` and
  `ACMCertificateArn` in a downstream override — not baked into this block.
- No WAF rate-based rule by default. Add to `SiteWebACL.Properties.Rules` (append-only).

## Alternatives considered

- **CloudFront Function for URL rewriting**: not included; single-page app assumes
  CloudFront returns `index.html` for all paths via `DefaultRootObject`.
- **S3 Transfer Acceleration**: out of scope for this pattern; would break OAC trust policy.
