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
Unsorted task list
------------------
Mochi: Morning walk (08:00, 30 min, high)
Mochi: Breakfast (08:30, 10 min, high)
Bean: Litter box check (08:25, 15 min, medium)
Bean: Play session (10:00, 20 min, low)
Bean: Vet reminder (08:30, 5 min, low)

Sorted by time
--------------
Mochi: Morning walk (08:00, 30 min, high)
Bean: Litter box check (08:25, 15 min, medium)
Mochi: Breakfast (08:30, 10 min, high)
Bean: Vet reminder (08:30, 5 min, low)
Bean: Play session (10:00, 20 min, low)

Filtered for Mochi
-------------------
Mochi: Morning walk (08:00, 30 min, high)
Mochi: Breakfast (08:30, 10 min, high)

Conflict warnings
-----------------
- Conflict: Mochi's Morning walk overlaps with Bean's Litter box check.
- Conflict: Bean's Litter box check overlaps with Mochi's Breakfast.
- Conflict: Bean's Litter box check overlaps with Bean's Vet reminder.
- Conflict: Mochi's Breakfast overlaps with Bean's Vet reminder.

Today's Schedule
-----------------
08:00 - 08:30 | Mochi: Morning walk (30 min, high, daily)
08:30 - 08:40 | Mochi: Breakfast (10 min, high, daily)
08:40 - 08:55 | Bean: Litter box check (15 min, medium, daily)
08:55 - 09:00 | Bean: Vet reminder (5 min, low, weekly)
09:00 - 09:20 | Bean: Play session (20 min, low, daily)

Why this plan was chosen
-------------------------
- Mochi's Morning walk was included because it is high priority and fits in the available time.
- Mochi's Breakfast was included because it is high priority and fits in the available time.
- Bean's Litter box check was included because it is medium priority and fits in the available time.
- Bean's Vet reminder was included because it is low priority and fits in the available time.
- Bean's Play session was included because it is low priority and fits in the available time.

Recurring tasks after scheduling
--------------------------------
Mochi: Morning walk (08:00, 30 min, high)
Mochi: Breakfast (08:30, 10 min, high)
Bean: Litter box check (08:25, 15 min, medium)
Bean: Play session (10:00, 20 min, low)
Bean: Vet reminder (08:30, 5 min, low)
```

## 🧪 Testing PawPal+

The current test suite covers the most important behaviors in the logic layer:
- Task completion updates status correctly.
- Adding tasks increases a pet's task list.
- Time sorting returns tasks in chronological order.
- Filtering can target a single pet.
- Recurring daily tasks create a next occurrence after scheduling.
- Conflict detection flags overlapping task windows.

### Persistence Workflow

PawPal+ can save and reload the owner tree through JSON using `save_to_json()` and `load_from_json()` in [pawpal_system.py](pawpal_system.py). The JSON file stores the owner, pets, and tasks as plain dictionaries so the Streamlit app or a CLI script can restore the same data on the next run.

Files updated for persistence:
- [pawpal_system.py](pawpal_system.py)
- [main.py](main.py)
- [README.md](README.md)

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\CodePath\AI110\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 7 items

tests\test_pawpal.py .......                                             [100%]

============================== 7 passed in 0.02s ==============================
```

Confidence Level: 4/5. The suite gives good coverage of the main scheduling behaviors and the Streamlit app now has a working logic layer, but I would still add a few more edge-case tests for empty schedules and longer multi-day planning.

## 📦 Persistence Details

The current persistence flow is:

1. Build a `PetOwner` object in memory.
2. Call `save_to_json()` to write the owner tree to `pawpal_data.json`.
3. Call `load_from_json()` to restore the same owner, pets, and tasks.
4. Use the restored object in the scheduler or Streamlit UI.

This keeps serialization outside the UI while preserving the object model used by the scheduler.

## 📐 Smarter Scheduling

The scheduler groups tasks from all of the owner's pets, sorts them by time and priority, filters by pet or completion state, checks for conflicts, keeps tasks inside the available time window, and explains why each task made it into the plan.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` / `Scheduler.sort_tasks()` | `sort_by_time()` orders tasks by preferred time; `sort_tasks()` keeps the priority-aware ordering for the final schedule. |
| Filtering | `Scheduler.filter_tasks()` / `Scheduler.build_daily_schedule()` | Filters by pet name or completion status and skips tasks that do not fit in the available time. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns warnings when task time windows overlap instead of stopping the program. |
| Recurring tasks | `Task.frequency` / `Task.next_occurrence()` | Copies daily and weekly tasks forward after completion so the next occurrence stays in the task list. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Open the Streamlit app and enter or update the owner information so the session has a real `PetOwner` object.
2. Add one or more pets, then attach tasks with times, priorities, categories, and recurrence values.
3. Click generate to view the sorted task table, the filtered tasks for the selected pet, and any conflict warnings.
4. Review the final schedule table and the explanation lines to see how the scheduler handled time and priority.
5. Run `python main.py` and `python -m pytest` to compare the terminal demo with the automated test coverage.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
