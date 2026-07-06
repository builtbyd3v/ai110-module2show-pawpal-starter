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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
