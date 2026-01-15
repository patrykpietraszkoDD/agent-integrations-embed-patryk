# Design

## Goal

The goal of this project is to build a minimal, agent-like system that demonstrates the core responsibilities of a metrics agent without recreating the full Datadog Agent.

The system is designed to:
- run integrations (“checks”) on a schedule
- collect basic host-level metrics
- submit metrics to Datadog

The design prioritizes simplicity, clarity, and correctness over completeness.

---

## High-Level Architecture

At a high level, the system is composed of three logical parts:

Checks → Agent Loop → Datadog Intake

- **Checks** collect metrics
- **Agent loop** coordinates execution and scheduling
- **Datadog intake** receives the collected metrics

Each component has a single responsibility and communicates through simple data structures.

---

## Core Concepts

### Checks

Checks represent integrations that know how to collect a specific set of metrics (for example, system metrics or process uptime).

- Checks are lightweight and self-contained
- They return metric data instead of sending it directly
- They do not manage scheduling, networking, or retries

This keeps integrations easy to reason about and extend.

---

### Agent Loop

The agent loop is responsible for orchestration rather than metric collection.

- Loads configuration
- Determines when each check should run
- Executes checks on their configured intervals
- Forwards collected metrics for submission

The loop is intentionally single-threaded to keep behavior predictable and easy to debug.

---

### Metric Submission

Metric submission is handled by a dedicated component.

- Translates internal metric data into Datadog’s intake format
- Handles HTTP concerns such as endpoints and authentication

By isolating this logic, metric collection remains decoupled from transport details.

---

## Design Principles

### Separation of responsibilities

Each component has a clear, narrow role:
- checks collect data
- the agent loop coordinates execution
- the sender handles delivery
