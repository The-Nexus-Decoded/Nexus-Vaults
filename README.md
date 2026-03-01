# Nexus-Vaults — The Nexus

**Layer:** Operations & Snapshots  
**Org:** [The-Nexus-Decoded](https://github.com/The-Nexus-Decoded)

Workspace snapshots, fleet documentation, operational scripts, and secrets management for the OpenClaw homelab.

## The Nexus Decoded

<pre>
The-Nexus-Decoded/
├── Pryan-Fire/          — Business logic, agent services, tools
├── Chelestra-Sea/       — Networking, communication, integration
├── Arianus-Sky/         — UIs, dashboards, visualizations
├── Abarrach-Stone/      — Data, schemas, storage
└── <b>Nexus-Vaults/</b>        — Workspace snapshots, fleet docs                 ◀ you are here
</pre>

## Structure

```
Nexus-Vaults/
├── docs/                   # Fleet scheduling, runbooks, architecture
│   └── FLEET-SCHEDULING.md
├── scripts/                # Operational scripts
│   ├── memory-guard.sh     # Memory backup guard
│   └── redact-and-sync.sh  # Redact secrets + sync to repo
├── ola-claw-main/          # Zifnab workspace snapshot
│   ├── SOUL.md, TOOLS.md, MEMORY.md, ACTIVE-TASKS.md
│   ├── skills/
│   └── ...
├── ola-claw-dev/           # Haplo workspace snapshot
│   ├── SOUL.md, TOOLS.md, MEMORY.md, ACTIVE-TASKS.md
│   ├── skills/
│   └── ...
└── ola-claw-trade/         # Hugh workspace snapshot
    ├── SOUL.md, TOOLS.md, MEMORY.md, ACTIVE-TASKS.md
    ├── skills/
    └── ...
```

## Server Snapshots

Each `ola-claw-*` directory contains a redacted snapshot of that server workspace:

| Directory | Server | Agent |
|-----------|--------|-------|
| `ola-claw-main/` | Zifnab | Coordinator |
| `ola-claw-dev/` | Haplo | Developer |
| `ola-claw-trade/` | Hugh | Trader |

Snapshots are synced daily by `redact-and-sync.sh` (2 AM CT). Sensitive data is stripped before commit.
