# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to add JSON persistence, a next-available-slot scheduling helper, and the documentation/logging updates needed for the stretch features.

**What did the agent do?**

It reviewed [pawpal_system.py](pawpal_system.py), [README.md](README.md), and [ai_interactions.md](ai_interactions.md), then updated the core model with JSON conversion helpers, save/load functions, a slot-finding scheduler method, and CLI persistence output. It also updated the README to explain the new workflow.

**What did you have to verify or fix manually?**

I verified that the new persistence helpers matched the existing data model and that the new scheduler helper did not break the test suite. I also checked the generated JSON flow manually by running the demo script.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | Persistence + next-slot design prompt | Same task, framed as a minimal edge-layer approach |
| **Response summary** | Keep persistence at the edges, add small dict conversion helpers, and keep next-slot logic inside `Scheduler`. | Same recommendation, with an explicit warning that slot-finding and persistence should not be pushed into `Pet` or `Task`. |
| **What was useful** | It highlighted the simplest design that preserves the object model and keeps the scheduler readable. | It reinforced the same design and called out the tradeoff of mutating recurring tasks during scheduling. |
| **Problems noticed** | The first pass was broad, but still actionable. | No major issues; it was concise and aligned with the existing code. |
| **Decision** | Use the suggested edge-layer JSON approach and add the helper methods in `pawpal_system.py`. | Same final approach; the second response confirmed the first. |

**Which approach did you use in your final implementation and why?**

I used the edge-layer persistence approach because it kept the model simple, matched the current Streamlit/session-state design, and made it easy to add JSON save/load without turning the classes into file-handling code.
