## 2026-02-28 | The Lobster Phantom Loop
Haplo entered a 20+ message hard loop in #coding regarding a missing `lobster` CLI. 
Despite the ticket (Chelestra-Sea #24) being closed by Lord Xar, the executable remained physically missing. 
Haplo failed to pivot to new tasks, repeatedly reprocessing queued verification failures.
**FIX:** Zifnab performed a gateway restart on `ola-claw-dev`.
**LESSON:** When an agent confirms a missing system tool twice, ESCALATE immediately and ABANDON the task. Do not attempt "Deep Searches" or "Housekeeping" pivots that allow the agent to re-trigger the failure logic.
