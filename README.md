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

Below is real output from running `python3 main.py`:

```
========================================
Today's Schedule for Jordan
Available time: 90 minutes
========================================
- Included 'Morning walk' (20 min, high priority).
- Included 'Feeding' (10 min, high priority).
- Included 'Evening walk' (30 min, high priority).
- Included 'Litter box cleaning' (15 min, medium priority).
----------------------------------------
Total time scheduled: 75 / 90 minutes

No conflicts detected.
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
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
collected 5 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [ 20%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 40%]
tests/test_pawpal.py::test_sort_by_priority_orders_high_first PASSED     [ 60%]
tests/test_pawpal.py::test_recurring_task_creates_next_occurrence PASSED [ 80%]
tests/test_pawpal.py::test_detect_conflicts_flags_overlapping_times PASSED [100%]

============================== 5 passed in 0.01s ===============================
```
**Confidence Level:** ⭐⭐⭐⭐☆ (4/5) — core scheduling, sorting, recurrence, and conflict detection are all tested; UI edge cases (e.g. empty task lists, invalid time formats) could use more coverage.

## 📐 Smarter Scheduling



| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_priority()` | Sorts high → medium → low priority |
| Filtering | `Scheduler.build_daily_plan()` | Greedily includes tasks by priority until time runs out |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks whose start_time windows overlap |
| Recurring tasks | `Scheduler.get_next_occurrence()` | Generates the next daily/weekly instance once a task is completed |

## 📸 Demo Walkthrough

1. Enter your name and available minutes per day, plus your pet's name and species.
2. Add care tasks with a title, duration, and priority (low/medium/high).
3. View your current task list in the table below the form.
4. Click "Generate schedule" to see the greedy scheduling algorithm pick tasks by priority until the time budget is used up, with a plain-language explanation for each included task.
5. If any tasks have overlapping start times, a warning is shown for each conflict.

Example workflow: add "Morning walk" (20 min, high), "Feeding" (10 min, high), and "Play time" (40 min, medium) with a 30-minute budget → the plan includes the walk and feeding (30/30 minutes), and play time is skipped since it doesn't fit.