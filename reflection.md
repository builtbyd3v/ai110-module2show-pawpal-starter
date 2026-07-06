# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My initial UML design uses four classes: `PetOwner`, `Pet`, `Task`, and `Scheduler`.
- `PetOwner` stores the owner's name and care preferences, `Pet` stores the pet's basic information, `Task` stores each care task's title, duration, and priority, and `Scheduler` turns the tasks into a daily plan.
- This keeps the data classes separate from the planning logic, which makes the system easier to explain and easier to change later.

**Step 2: Building blocks**

- `PetOwner` holds the owner's name, preferences, and pets; it can add pets and update preferences.
- `Pet` holds the pet's name, species, age, and tasks; it can add tasks and return the current list of tasks.
- `Task` holds the task title, duration, priority, category, and whether it repeats; it represents one care activity that may be scheduled.
- `Scheduler` holds the owner, the pet being planned for, the available time, and the plan-making behavior; it can sort tasks, build a schedule, and explain the result.

**b. Design changes**

- Yes. I first thought about using one planning class, but I separated the data model from the scheduling behavior after reviewing the app flow.
- I also adjusted the scheduler so it explicitly knows which pet it is planning for instead of only holding owner-level data.
- That change made the design more modular and better matched the Streamlit starter app.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers time of day, priority, pet ownership, whether a task is already completed, and whether a task repeats daily or weekly.
- I treated time and priority as the main constraints because they control what actually fits into a short daily schedule, while pet name and completion status help narrow the task list.

**b. Tradeoffs**

- One tradeoff is that conflict detection is lightweight: it warns about overlapping time windows instead of trying to fully resolve every possible clash automatically.
- That is reasonable here because the project is a planner first, so surfacing the problem clearly is more useful than silently changing the user's intended task order.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI to help turn the UML idea into concrete Python classes, to draft small scheduling methods, and to tighten the Streamlit wiring and docs.
- The most helpful prompts were the ones that named a specific file and a specific behavior, like asking how to sort tasks by time, filter by pet, or keep task state in `st.session_state`.
- Using separate chat sessions by phase helped keep the design conversation, the scheduling implementation, and the UI polish work from bleeding into one another.

**b. Judgment and verification**

- I did not accept the first scheduling draft as-is because it was too shallow for the assignment.
- I verified the final behavior by running the demo script, checking the terminal output for ordering and conflict warnings, and running `pytest` on the task and scheduler behaviors.
- I also kept the final UML and README in sync with the code so the written deliverables matched the implementation rather than describing an older draft.

---

## 4. Testing and Verification

**a. What you tested**

- I tested task completion, task addition, sorting by time, filtering by pet name, recurring task rollover, and conflict detection.
- These tests mattered because they covered the core logic that the UI depends on and made sure the planner still behaved correctly after the scheduling changes.

**b. Confidence**

- I am moderately confident in the current scheduler because the main workflow is covered by a demo run and automated tests.
- If I had more time, I would test edge cases like empty schedules, multiple tasks with the same start time, and longer recurring sequences across several days.

---

## 5. Reflection

**a. What went well**

- I am most satisfied that the UI, logic layer, and documentation now match each other instead of feeling like separate pieces.

**b. What you would improve**

- In another iteration, I would improve the conflict resolution so the scheduler can suggest alternate times instead of only warning about overlaps.

**c. Key takeaway**

- I learned that a small, well-tested model with clear responsibilities is much easier to extend than a single large planning function.
