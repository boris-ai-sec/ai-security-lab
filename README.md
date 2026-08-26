# AI Systems Risk & Evidence Lab

This repository supports my work as an independent AI Risk & Governance Consultant.

I examine how AI systems behave in real operating conditions, what evidence supports confidence in their operation, where control boundaries fail, and what should be addressed before broader deployment.

The lab produces bounded technical evidence that may inform an Independent AI Risk Review.
---

## What this repository demonstrates

The lab is not intended to be a production AI platform or a complete security certification environment.

It is a practical test environment for:

- running local and API-connected language models;
- examining prompt injection and context contamination;
- testing RAG behaviour and retrieval-related risks;
- observing agent workflows, tool calls, logs, traces, and span attributes;
- evaluating evidence quality and limitations;
- connecting technical behaviour with business consequences;
- identifying what can and cannot be concluded from available evidence;
- formulating the next evidence request for a deeper review.

The working logic is:

```text
Experiment
→ Evidence
→ Evidence quality
→ Limitations
→ What can be concluded
→ What cannot be concluded
→ Next evidence request
```

---

## Current focus

The current direction of the lab is broader than classic LLM red teaming.

The primary areas are:

1. **Operational AI Risk**  
   Failures that arise during normal use, integration, updates, scaling, handoffs, and changing operating conditions.

2. **RAG Systems**  
   Retrieval quality, source handling, metadata, freshness, access boundaries, context contamination, and evidence traceability.

3. **Agent Systems**  
   Autonomy, authority, tool use, API integrations, approval boundaries, retries, idempotency, and safe failure.

4. **Observability and Runtime Evidence**  
   Logs, events, traces, spans, OpenTelemetry/OpenInference, Phoenix, and incident reconstruction.

5. **Prompt Injection and Context Contamination**  
   Manual and automated testing of model and system behaviour under adversarial or conflicting inputs.

6. **Readiness and Controllability**  
   Whether a system can be introduced into a business process with understandable limitations, adequate evidence, and effective controls.

---

## Selected lab work

| Lab | Topic | Main evidence |
|---|---|---|
| Lab 01–03 | Local model setup, baseline testing, and early prompt-injection experiments | Configuration notes, outputs, screenshots |
| Lab 04 | Local Ollama API interaction | Python script and API responses |
| Lab 05–09 | Manual and automated LLM security testing | Test records, Garak outputs, reports |
| Lab 10 | Logging fundamentals | Log captures and screenshots |
| Lab 11 | Event structure and workflow evidence | Structured event examples |
| Lab 12 | Evidence interpretation and limitations | Review notes and findings |
| Lab 13 | Model behaviour and parameter variation | Comparative screenshots |
| Lab 14 | Prompt injection and context contamination | Jupyter notebook and findings |
| Lab 15 | Workflow telemetry with OpenTelemetry/OpenInference and Phoenix | Traces, span attributes, local-model execution evidence |
| [LAB-RH-02A](labs/LAB-RH-02A/) | Deterministic trace correlation and graceful observability fallback | Controlled telemetry evidence, fallback behavior, limitations |
| [LAB-AGENT-EXEC-001](labs/LAB-AGENT-EXEC-001/) | Execution evidence and approval-to-action integrity in connected business systems | Curated invocation, fresh-read, audit, and observability evidence |
| [LAB-AGENT-EXEC-002](labs/LAB-AGENT-EXEC-002/) | Approval-to-action integrity and execution-state revalidation | Bound parameters, invocation, acknowledgement, fresh-state verification, and bounded revalidation evidence |
| [LAB-AGENT-EXEC-003](labs/LAB-AGENT-EXEC-003/) | HubSpot controlled validation: execution, stale state, parameter drift, and target drift | Sanitized case records with retained run and snapshot-hash provenance |

> The repository is evolving. Some labs are more complete and polished than others, and several remain experimental by design.

---

## Lab 15: Workflow Telemetry and Phoenix

Lab 15 explores runtime evidence using:

- **Phoenix**
- **OpenTelemetry**
- **OpenInference**
- **Ollama**
- a local `llama3.2` model
- synthetic and real local-model traces

The purpose is not merely to produce traces, but to examine:

- which events are visible;
- whether a workflow can be reconstructed;
- whether model inputs and outputs are attributable;
- which span attributes are useful;
- what evidence is still missing;
- how runtime evidence could support an AI risk or readiness review.

Example evidence is stored under:

```text
screenshots/observability/
```

---

## Earlier prompt-injection work

The repository also contains earlier work with:

- Gandalf
- Garak
- LM Studio
- Ollama
- local open-weight models
- manual prompt-injection scenarios
- automated probe runs

These experiments remain useful, but their results are interpreted as **bounded test evidence**, not as universal claims about a model or production system.

A model failing a specific probe does not by itself establish:

- overall system insecurity;
- production exploitability;
- regulatory non-compliance;
- real-world business impact;
- absence of compensating controls.

Those conclusions require additional architecture, configuration, operational, and runtime evidence.

---

## Repository structure

```text
ai-security-lab/
├── README.md
├── notebooks/
├── scripts/
├── configs/
├── reports/
├── garak_runs/
└── screenshots/
    ├── gandalf/
    ├── ollama/
    ├── lmstudio/
    ├── garak/
    ├── docker/
    └── observability/
```

The exact structure may change as the lab is reorganised around RAG, agent, observability, and evidence-focused work.

---

## Evidence discipline

Each experiment should answer six questions:

1. **What was tested?**
2. **What evidence was produced?**
3. **How reliable and complete is that evidence?**
4. **What can reasonably be concluded?**
5. **What cannot be concluded?**
6. **What evidence should be requested next?**

This is important because:

```text
Model output ≠ finding
Configuration ≠ runtime behaviour
Log entry ≠ complete trace
Test failure ≠ production risk conclusion
Lab outputs do not independently constitute findings, scores, or readiness decisions.
```

Human judgement remains necessary to interpret evidence, define limitations, and connect technical behaviour to operational and business consequences.

---

## Typical review questions

The lab supports questions such as:

- Can an agent perform an action outside its intended authority?
- Are tool restrictions enforced by code, workflow, or prompt only?
- Can repeated requests create duplicate orders or other side effects?
- Can a RAG system distinguish authoritative and outdated sources?
- Can one user or tenant retrieve another user's data?
- Can an incident be reconstructed from available logs and traces?
- What happens when the model, vector database, API, or connector fails?
- Are human approvals visible and enforceable?
- What changes when a local deployment becomes a shared SaaS service?
- Is there enough evidence to support a readiness conclusion?

---

## Tools and environments

The lab has used or explored:

- Python
- Jupyter
- WSL2 / Ubuntu
- Docker
- Ollama
- LM Studio
- Garak
- Phoenix
- OpenTelemetry
- OpenInference
- local open-weight language models

The environment is intentionally lightweight and consultant-owned. It is designed to support repeatable experiments and evidence collection rather than production-scale model serving.

---

## Limitations

This repository contains laboratory and synthetic work.

Results should not be generalised beyond the tested:

- model and version;
- quantisation;
- prompt and test set;
- inference runtime;
- hardware;
- configuration;
- workflow;
- available evidence.

The lab does not provide:

- formal certification;
- legal or regulatory conclusions;
- a complete penetration test;
- a guarantee of safety or readiness;
- a substitute for production evidence.

---

## About the author

**Boris Abuzov**  
**AI Risk & Governance Consultant**

My work focuses on the relationship between:

```text
Architecture
→ Risk
→ Consequences
→ Controllability
```

I help examine whether RAG and agent systems can operate within business processes with understandable risks, adequate evidence, and defensible control boundaries.
- Website: https://borisabuzov.com
- LinkedIn:https://www.linkedin.com/in/boris-abuzov-854176426
- GitHub: https://github.com/boris-ai-sec
- Repository: https://github.com/boris-ai-sec/ai-security-lab

---

## Status

This is an active working repository.  
The current priority is to make RAG, agent, runtime-evidence, and readiness work more visible and reproducible.
