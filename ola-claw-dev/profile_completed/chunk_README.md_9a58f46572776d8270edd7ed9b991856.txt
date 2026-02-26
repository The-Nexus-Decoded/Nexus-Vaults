[REDACTED_DYNAMIC_KEY] Pryan-Fire — The Realm of Fire

**Layer:** Business Logic  
**Org:** [The-Nexus-Decoded](https://github.com/The-Nexus-Decoded)

Core business logic, agent services, and operative tools for the OpenClaw homelab.

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Structure

```
Pryan-Fire/
├── haplos-workshop/        [REDACTED_DYNAMIC_KEY] Haplo's domain — CI/CD, dev tools, process supervisor
│   ├── scripts/            [REDACTED_DYNAMIC_KEY] Automation scripts
│   ├── tools/              [REDACTED_DYNAMIC_KEY] Dev tooling
│   └── ci/                 [REDACTED_DYNAMIC_KEY] CI/CD pipeline configs
├── zifnabs-scriptorium/    [REDACTED_DYNAMIC_KEY] Zifnab's domain — orchestration, monitoring, coordination
│   ├── scripts/            [REDACTED_DYNAMIC_KEY] Orchestration scripts
│   ├── monitoring/         [REDACTED_DYNAMIC_KEY] Health checks, quota monitor, alerts
│   └── coordination/       [REDACTED_DYNAMIC_KEY] Delegation, agent coordination logic
└── hughs-forge/            [REDACTED_DYNAMIC_KEY] Hugh's domain — trading algos, financial connectors
    ├── services/           [REDACTED_DYNAMIC_KEY] Trading services (Meteora SDK, risk manager, etc.)
    └── config/             [REDACTED_DYNAMIC_KEY] Service configuration templates
```

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] Deployment Targets

| Directory | Deploys to |
|-----------|-----------|
| `haplos-workshop/` | ola-claw-dev (Haplo) |
| `zifnabs-scriptorium/` | ola-claw-main (Zifnab) |
| `hughs-forge/` | ola-claw-trade (Hugh) |

[REDACTED_DYNAMIC_KEY][REDACTED_DYNAMIC_KEY] What's NOT tracked

Per `.gitignore`:
- `strategies/` — trading strategies are private
- `.env` — API keys and tokens
- `scripts/private/` — scripts with hardcoded IPs
- `workspace/` — SOUL.md and agent context
