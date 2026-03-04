# Zendesk ↔ Asana HIPAA-Compliant Integration
AWS Cloudwatch log:
<img width="943" height="654" alt="image" src="https://github.com/user-attachments/assets/b28cf749-fc54-4105-aaea-372c8cf75a2f" />

Zendesk Ticket Example:
<img width="393" height="650" alt="image" src="https://github.com/user-attachments/assets/6768ff14-e8af-4b66-a9a4-534141e8d61d" />

Resulting Asana Task:
<img width="398" height="725" alt="image" src="https://github.com/user-attachments/assets/32c3ad32-0c90-44e1-9cd5-5a5de6999e6e" />

Zendesk Webhook Trigger:
<img width="821" height="588" alt="image" src="https://github.com/user-attachments/assets/8e381a77-07e1-49d9-bfb9-d034443c7ab3" />


## Overview

This project enables secure collaboration between:

- **Zendesk Agent (User A)** – Communicates with customers and manages tickets.
- **Asana Specialist (User B)** – Reviews and works on claim-related tasks.

Both users operate in their native platforms while collaborating on the same case.

The system synchronizes ticket and task data while ensuring Protected Health Information (PHI) remains secure and compliant.

---

## Problem Statement

User A and User B need to collaborate on the same case:

- A ticket exists in Zendesk.
- A corresponding task exists in Asana.
- Updates should flow between systems.
- Communication remains inside each platform.
- PHI must remain protected.

---

## Compliance & Security

We operate under:

- OAuth-based authentication for system integrations.
- Executed Business Associate Agreements (BAAs) with:
  - Zendesk
  - Asana
  - AWS

Security principles:

- Minimal data persistence.
- Restricted permissions via scoped OAuth tokens.
- Encrypted storage of secrets.
- Full audit logging.
- Controlled webhook ingestion.

AWS functions as the secure serverless orchestration layer.

---

## Tools Used

### Zendesk Enterprise

- Main support and admin platform (sandbox used for development/testing).
- Features leveraged:
  - Triggers
  - Webhooks
  - OAuth (client + token authentication)
  - BAA agreement

Zendesk events initiate the sync process.

---

### Asana

- Dedicated workspace for claims processing.
- Components:
  - Custom workspace
  - Application integration (can remain unpublished)
  - Webhooks
  - OAuth (client + token authentication)
  - BAA agreement

Asana task updates propagate back to Zendesk through webhooks.

---

### AWS

Serverless integration layer handling orchestration and processing.

Components:

- IAM – Role-based access control for services and Lambda. (Custom Policy and roles used)
- Secrets Manager – Secure storage for OAuth tokens and credentials.
- Lambda – Business logic for event processing and synchronization. (2 functions used, one for each direction)
- API Gateway – Webhook endpoints and request routing.
- DynamoDB – Lightweight state tracking, mapping tickets to tasks, event tracking.
- CloudWatch – Logging, monitoring, debugging, and audit visibility.
- BAA agreement – Compliance coverage for PHI processing. (required for all 3 platforms)

AWS acts as the central event processor without storing unnecessary data.

---

## Architecture

### Core Flow (PROOF OF CONCEPT COMPLETE)

1. Ticket created/updated in Zendesk.
2. Trigger invokes a webhook.
3. Webhook hits API Gateway endpoint.
4. Lambda processes event.
5. Task is created/updated in Asana.

Reverse flow: (WIP)

1. Task updated in Asana.
2. Webhook triggers AWS endpoint.
3. Lambda processes update.
4. Ticket is updated in Zendesk.

---

## Design Goals

- Minimize technical debt.
- Reduce blast radius via isolated serverless components.
- Modular function design.
- Clear separation of concerns.
- Strong logging and observability.
- Easy traceability for debugging.
- Secure handling of PHI.

A technically proficient engineer should understand the system and data flow quickly.

---

## Logging & Observability

The system includes:

- Structured logging for every webhook request.
- Correlation IDs linking tickets and tasks.
- Request/response logging for API calls.
- Error tracking and failure visibility.
- CloudWatch monitoring.
