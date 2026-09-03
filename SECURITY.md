# Repository Security Policy

## Scope

This policy covers security concerns in this repository's own source files, validation tooling, published repository configuration, and evidence-integrity mechanisms.

It does not make Boris Abuzov the security contact for HubSpot, ServiceNow, MoySklad, Bitrix24, Langflow, Qdrant, Ollama, Phoenix, OpenInference, OpenTelemetry, or any other third-party product. Vulnerabilities in third-party products should be reported through the relevant vendor's security process.

## Reporting

- For a potentially sensitive repository-specific concern, contact Boris through the [email route](https://borisabuzov.com/discuss/) with only a short, non-confidential summary and identify `boris-ai-sec/ai-security-lab`. Do not include credentials, private data, exploit details, confidential artifacts, or other sensitive material in the initial message. If further technical detail is needed, an appropriate exchange method can be agreed separately.
- For non-sensitive documentation errors, broken links, or reproducible validation defects, open a [GitHub issue](https://github.com/boris-ai-sec/ai-security-lab/issues).
- Do not place credentials, private data, exploit details, or other sensitive material in a public issue.

No response-time or remediation-time commitment is implied.

## Supported state

Security and integrity corrections are evaluated against the current `main` branch and the explicit boundaries of the affected evidence package. Published tags and releases are retained as versioned snapshots; later corrections are documented through subsequent repository history or releases as appropriate.
