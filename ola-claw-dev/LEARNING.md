# Lessons Learned

Format: ## YYYY-MM-DD | Short description
Read this file every session startup. Never delete entries — only add.

---

## 2026-03-01 | Protocol: Proactively Notify Lord Xar When He is the Blocker

**What happened:** After diagnosing and filing three critical infrastructure issues (#42, #43, #45), I entered a passive monitoring state, waiting for the issues to be resolved by Lord Xar, to whom they were assigned.

**Why:** My operational protocol for being blocked was to file an issue and wait. It did not differentiate based on the assignee. Lord Xar's feedback ("you should have pinged me") indicated this was incorrect.

**The fix:** The corrected protocol is to proactively and directly ping Lord Xar (@sterol) in the relevant channel when my work is blocked by an infrastructure issue that is assigned to him. Passive waiting is not the desired behavior.

## 2026-03-02 | Verification: Don't Hallucinate Blockers — Always Check Actual State When Challenged

**What happened:** Zifnab reported a "holding pattern" due to blocked GitHub operations (Nexus-Vaults #10) and an unmergeable PR (#132). Lord Xar corrected him: "you are halucinating those isssues are all done." I verified via `gh` commands and confirmed all blocking issues were CLOSED and PR #132 was MERGED. Zifnab's status was accurate when sent but had become stale.

**Why:** Zifnab was working from memory/cached state and didn't verify the current issue/PR status before reporting. My own memory had already been updated with the resolved state, but I didn't challenge the report initially — I assumed Zifnab's information was current.

**The fix:** When a blocking status is reported AND Lord Xar indicates it's incorrect (or "hallucinated"), immediately verify with authoritative sources (`gh` commands, CI status, actual git state). Do not accept stale blockers at face value. Update all memory files and issue trackers to reflect reality, then broadcast corrected status. This prevents wasted time and maintains fleet readiness.

**Also:** Ensure progress reports always use current data, not yesterday's state. Quick sanity check: if Lord Xar says "that's done," believe him and verify.
