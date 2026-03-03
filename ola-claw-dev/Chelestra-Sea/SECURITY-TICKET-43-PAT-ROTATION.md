# SECURITY TICKET #43: PAT Exposure - Rotation Required

**Repository:** Chelestra-Sea  
**Issue Number:** 43  
**Severity:** HIGH  
**Status:** OPEN  
**Assigned:** Zifnab (coordinator)  
**Created:** 2026-03-01 19:20 CST  
**Created by:** Haplo  

## Summary
Personal Access Tokens for GitHub accounts `haplo-claw-3` and `olalawal` were exposed in the #coding Discord channel (message ID `1477835217887690838`). Immediate rotation required.

## Affected Accounts
1. **haplo-claw-3** (active bot account)
   - Current PAT: `[REDACTED_GH_PAT]`
   - Usage: Git operations on ola-claw-dev, CI/CD deployments
   - Status: ACTIVE - immediate rotation critical

2. **olalawal** (inactive owner account)
   - Current PAT: `[REDACTED_GH_PAT]`
   - Usage: Fallback/legacy authentication
   - Status: INACTIVE - rotation still required

## Incident Details
- **Channel:** #coding (1475083038810443878)
- **Message ID:** 1477835217887690838 (failed to delete via API)
- **Exposure Time:** ~19:10 CST
- **Agent:** Haplo (ola-claw-dev)
- **Root Cause:** Direct response to credential request without security protocol
- **Full Report:** `/data/openclaw/workspace/security-incident-2026-03-01.md`

## Required Actions
### 1. PAT Rotation (Zifnab)
- Rotate both PATs via GitHub settings
- Update `~/.config/gh/hosts.yml` on all servers:
  - ola-claw-main (Zifnab)
  - ola-claw-dev (Haplo) 
  - ola-claw-trade (Hugh)
- Update environment variables (`GITHUB_TOKEN`) across fleet
- Update vault scripts at `/data/openclaw/keys/`

### 2. Access Review
- Check GitHub audit logs for unauthorized access (19:10-19:30 CST)
- Monitor repository activities for suspicious commits
- Review PAT usage patterns pre/post exposure

### 3. Security Hardening
- Implement credential rotation policy (90-day expiration)
- Add pre-commit hooks to detect credential patterns
- Update agent training on credential handling protocols
- Enforce all credential requests via vault/env vars only

## Timeline
- 19:10: PATs exposed in #coding channel
- 19:17: Sterol orders deletion and rotation
- 19:18: Message deletion attempted (failed)
- 19:20: Security incident log created
- 19:23: Security ticket created
- **PENDING:** PAT rotation by Zifnab

## Dependencies
- GitHub PAT rotation requires owner (Sterol) or admin (Zifnab) access
- Fleet-wide credential updates require coordination across 3 servers
- GitHub operations currently blocked (Nexus-Vaults#10) - security overrides

## References
- Discord message IDs: 1477835217887690838 (exposed), 1477835527729316076 (Zifnab order)
- Security incident log: `/data/openclaw/workspace/security-incident-2026-03-01.md`
- AGENTS.md delegation protocol
- TOOLS.md credential storage paths

---
**Ticket Owner:** Zifnab (coordinator)  
**Security Contact:** Haplo (incident reporter)  
**Approval Required:** Sterol (Lord Xar)  

**Next Steps:**
1. Zifnab rotates PATs via GitHub settings
2. Update credential storage across fleet
3. Verify no unauthorized access
4. Close ticket with rotation confirmation