# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule
-----------------
08:00 - 08:30 | Mochi: Morning walk (30 min, high, daily)
08:30 - 08:40 | Mochi: Breakfast (10 min, high, daily)
08:40 - 08:55 | Bean: Litter box check (15 min, medium, daily)
08:55 - 09:15 | Bean: Play session (20 min, low, daily)

Why this plan was chosen
-------------------------
- Mochi's Morning walk was included because it is high priority and fits in the available time.
- Mochi's Breakfast was included because it is high priority and fits in the available time.
- Bean's Litter box check was included because it is medium priority and fits in the available time.
- Bean's Play session was included because it is low priority and fits in the available time.
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

The scheduler groups tasks from all of the owner's pets, sorts them by priority, keeps them inside the available time window, and explains why each task made it into the plan.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_tasks()` | Sorts by priority, preferred time, duration, pet name, and description. |
| Filtering | `Scheduler.build_daily_schedule()` | Skips completed tasks and tasks that do not fit in the available time. |
| Conflict handling | `Scheduler.build_daily_schedule()` | Lays tasks out sequentially so the printed schedule does not overlap. |
| Recurring tasks | `Task.frequency` | Tracks whether a task is daily, weekly, or some other repeat pattern. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Run `python main.py` to create a sample owner, two pets, and several care tasks.
2. Review the printed schedule in the terminal to see how the tasks were ordered.
3. Look at the explanation lines to understand why each task was selected.
4. Run `python -m pytest` to confirm the task status and task-adding behaviors still work.
5. Use the output as a reference when you connect the logic layer to the Streamlit UI.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
