# agent-integrations-embed-patryk
Project to create a mini agent for the jan 2026 agent integrations embed program

## What it does
- Loads `config.yaml`
- Runs enabled checks on their own intervals
- Collects system metrics (CPU/mem/disk) and an example uptime metric
- Submits metrics to Datadog Metrics intake via `POST https://api.<DD_SITE>/api/v1/series` using `DD-API-KEY`

## Prereqs
- Python 3.10+

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
Set your Datadog API key (for the org you want to send metrics into):
`export DD_API_KEY="..."`

Optionally set the site (defaults to datadoghq.com) in `config.yaml`:
- datadoghq.com
- datadoghq.eu
- us3.datadoghq.com
- us5.datadoghq.com

Run:
`python3 -m miniagent --config config.yaml`

Once the miniagent runs, you should see the following metrics in your Datadog account:
- miniagent.system.cpu.pct
- miniagent.system.disk.used_pct
- miniagent.system.mem.used_pct
- miniagent.uptime


---
## Considerations for the future
If I had more time I would attempt to implement the following:
- batching metrics to reduce submission overhead
- adding retry and backoff behavior
- introducing concurrency with execution limits
- emitting self-metrics for agent health and observability
- separating integration configuration files
