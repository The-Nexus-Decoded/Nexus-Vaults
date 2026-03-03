# Research: Multi-Session Claude Code Orchestration (Nexus-Vaults #11)

**Date:** 2026-03-01  
**Investigator:** Haplo  
**Status:** Initial research

## Objective
Design a protocol/system for orchestrating multiple Claude Code (ACP harness) sessions within OpenClaw fleet. Enable parallel coding tasks, load balancing, session management, and result aggregation.

## Current OpenClaw Capabilities

### sessions_spawn with runtime="acp"
- OpenClaw supports spawning ACP (Agent Client Protocol) sessions for external harnesses like Claude Code, Codex, Pi, OpenCode, Gemini CLI.
- Key parameters:
  - `runtime: "acp"` (required)
  - `agentId`: target harness id (e.g., "codex", "claude-code")
  - `thread: true` for thread-bound persistent sessions
  - `mode: "session"` for persistent, `mode: "run"` for one-shot
  - `cwd`: working directory
- Session key pattern: `agent:<agentId>:acp:<uuid>`

### ACP vs Sub-agents
- **ACP:** External harness runtime via ACP backend plugin (acpx). For coding harnesses.
- **Sub-agent:** OpenClaw-native delegated runs.

### Thread-Bound Sessions
- Discord supports thread binding for ACP sessions.
- Follow-up messages in thread route to bound ACP session.
- Requires feature flags: `acp.enabled=true`, `acp.dispatch.enabled=true`, Discord thread bindings enabled.

### Management Commands
- `/acp spawn` for explicit operator control.
- `/acp status`, `/acp model`, `/acp permissions`, `/acp timeout`, `/acp steer`, `/acp cancel`, `/acp close`.

## Use Cases for Multi-Session Orchestration

1. **Parallel Code Reviews:** Multiple PRs reviewed simultaneously by separate Claude Code instances.
2. **Feature Development:** Different features developed in parallel sessions.
3. **Testing Suite Generation:** Generate tests for multiple modules concurrently.
4. **Documentation Generation:** Parallel documentation of different codebases.
5. **Load Balancing:** Distribute tasks across multiple Claude Code sessions to avoid rate limits.

## Challenges

1. **Session Management:** Tracking multiple active sessions, their states, tasks.
2. **Resource Allocation:** Limiting concurrent sessions based on available resources (API limits, compute).
3. **Result Aggregation:** Collecting and summarizing outputs from multiple sessions.
4. **Error Handling:** Handling failures in individual sessions.
5. **Cost Control:** Monitoring token usage across multiple sessions.

## Existing Fleet Patterns

### Lobster Workflows
- Current workflows (e.g., `patryn-workhorse`, `nexus-bridge`) chain fleet CLI commands.
- Could extend with ACP session spawning and management steps.

### Fleet CLI
- `fleet` command provides fleet-wide operations.
- Could add `fleet acp-sessions` to list/manage ACP sessions across servers.

## Proposed Architecture

### 1. ACP Session Pool Manager
- Service that maintains a pool of ACP sessions.
- Configurable pool size per harness type.
- Session health monitoring and reconnection.

### 2. Task Queue
- Queue tasks (coding requests) with metadata (repo, priority, timeout).
- Worker processes pick tasks and assign to available sessions.

### 3. Result Collector
- Aggregates outputs from sessions.
- Formats summaries, diffs, PR comments.

### 4. Monitoring Dashboard
- Real-time view of active sessions, queue length, completion rates.

## Implementation Options

### Option A: Lobster Workflow Extension
- Create new `.lobster` workflow that uses `sessions_spawn` with `runtime="acp"`.
- Steps: spawn → send task → monitor → collect → close.
- Limited to sequential tasks; parallelization would require multiple workflow instances.

### Option B: Dedicated Agent Service
- Build a new agent (maybe "Claude Orchestrator") that manages ACP sessions.
- Uses OpenClaw's messaging to communicate with sessions.
- Could be deployed as a sub-agent or separate gateway.

### Option C: Fleet CLI Extension
- Add `fleet acp-*` commands to manage sessions across fleet.
- Integrate with existing cron system for scheduled tasks.

## Current System State (2026-03-01)

### Installed Coding Agents
- **Pi:** `/usr/bin/pi` (coding agent) - installed
- **Claude Code:** Not installed (`which claude` returns empty)
- **Codex:** Not installed (`which codex` returns empty)
- **OpenCode:** Not installed (`which opencode` returns empty)

### OpenClaw ACP Configuration
- No ACP section in `/data/openclaw/openclaw.json`
- No ACP plugin installed (only discord and lobster plugins)
- No `acp.defaultAgent` configured
- ACP CLI available (`openclaw acp`) but backend not configured

### Discord Thread Binding
- Discord channel configured (#coding: 1475083038810443878)
- Unknown if `channels.discord.threadBindings.spawnAcpSessions=true` is set
- Unknown if `acp.enabled=true` and `acp.dispatch.enabled=true`

## Next Steps

### Phase 1: Configuration & Testing
1. **Check Discord ACP settings:** Verify thread binding configuration
2. **Test ACP spawning:** Attempt `sessions_spawn` with `runtime:"acp"` and `agentId:"pi"` (if Pi is ACP-enabled)
3. **Install missing harnesses:** Consider installing Claude Code/Codex if needed

### Phase 2: MVP Design
1. **Simple task queue:** Lobster workflow that spawns single ACP session
2. **Session management:** Basic monitoring and result collection
3. **Error handling:** Timeout and retry logic

### Phase 3: Multi-Session Orchestration
1. **Pool manager:** Manage multiple ACP sessions
2. **Load balancing:** Distribute tasks across sessions
3. **Result aggregation:** Combine outputs from parallel sessions

## Implementation Priority
## Findings: Pi as ACP Harness (2026-03-01)
- Pi CLI (`/usr/bin/pi`) is installed and listed as an ACP harness in OpenClaw documentation.
- However, ACP backend plugin (`acpx`) does not appear to be installed (no entry in plugins, no extensions/acpx directory).
- Discord thread binding configuration unknown (`channels.discord.threadBindings.spawnAcpSessions`).

## Implementation Priority
Given current state, recommend:
1. First verify ACP functionality works with Pi (if ACP-enabled)
2. If not, configure ACP backend and test with Pi
3. Design MVP with single session before scaling to multi-session
4. Integrate with existing Lobster workflow system

## References
- OpenClaw ACP Agents docs: `/usr/lib/node_modules/openclaw/docs/tools/acp-agents.md`
- sessions_spawn tool documentation
- Sub-agents documentation