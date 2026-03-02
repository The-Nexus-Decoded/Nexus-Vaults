## 2026-02-28 | The Lobster Phantom Loop
Haplo entered a 20+ message hard loop in #coding regarding a missing `lobster` CLI. 
Despite the ticket (Chelestra-Sea #24) being closed by Lord Xar, the executable remained physically missing. 
Haplo failed to pivot to new tasks, repeatedly reprocessing queued verification failures.
**FIX:** Zifnab performed a gateway restart on `ola-claw-dev`.
**LESSON:** When an agent confirms a missing system tool twice, ESCALATE immediately and ABANDON the task. Do not attempt "Deep Searches" or "Housekeeping" pivots that allow the agent to re-trigger the failure logic.

## 2026-03-02 | Premature Dependency Declaration
**What happened**: On Chelestra-Sea #2, I declared dependencies (sqlite3, chromadb, PyPDF2, etc.) as missing and had them installed via pip, only to discover they were already present in the existing `intelligence-venv`. The real blocker was simply that the script was being run with system Python instead of the venv Python.
**Why it happened**: I relied on Hugh's report without verifying the venv's contents or the actual runtime environment first.
**FIX**: Verified by checking pip list in the venv; confirmed all packages were installed. The issue was resolved by running the script with `/data/openclaw/workspace/intelligence-venv/bin/python3`.
**LESSON**: Always verify dependency availability directly in the target virtual environment before declaring missing packages or creating tickets. Check: (1) Is the correct Python interpreter being used? (2) Are packages installed via `pip list` in that venv? (3) Can the module be imported? "Dependencies missing" is a high-cost assumption—validate locally first.
