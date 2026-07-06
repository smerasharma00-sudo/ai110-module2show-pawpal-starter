# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

For PawPal+, I settled on four classes: `Task`, `Pet`, `Owner`, and `Scheduler`.

`Task`, `Pet`, and `Owner` are implemented as Python dataclasses because their main
job is to hold data rather than make decisions. A `Task` stores a title, duration,
priority, frequency, start time, and completion status. A `Pet` stores its name,
species, and a list of `Task` objects. An `Owner` stores their name, how many
minutes per day they have available for pet care, and a list of `Pet` objects.
This mirrors the real-world relationship: an owner has multiple pets, and each
pet has its own set of care tasks.

`Scheduler` is different — it's a plain class, not a dataclass, because it doesn't
really hold data of its own beyond a reference to the `Owner` it's working with.
Its job is entirely behavioral: sorting tasks by priority, building a daily plan
that fits within the owner's available time, detecting conflicts between tasks,
explaining why each task was included or skipped, and generating the next
occurrence of a recurring task. Separating "data" classes from the one
"decision-making" class keeps each piece easy to reason about and test on its own.

Based on the README, I identified three core actions the app needs to support:
1. Letting a user enter basic owner and pet info (name, species, available time).
2. Letting a user add care tasks with a duration and a priority level.
3. Generating a daily plan that fits tasks into the owner's available time,
   ordered by priority, along with an explanation of why each task made
   it into (or got left out of) the plan.

These three actions became the foundation for the UML diagram and the class
skeletons in `pawpal_system.py`.

**b. Design changes**

My design changed in two main ways as I moved from skeleton to implementation.
First, I originally planned for `Scheduler.detect_conflicts()` to only catch
tasks with duplicate titles, since that was the simplest thing to implement in
Phase 2. In Phase 4, I realized this didn't actually detect real scheduling
conflicts — two tasks with different titles could still be scheduled at the
same time. I added a `start_time` field to `Task` and rewrote conflict
detection to compare actual time windows and flag genuine overlaps.

Second, I added a `Scheduler.get_next_occurrence()` method that wasn't in my
original UML diagram. Once I implemented `frequency` on `Task`, I realized the
scheduler needed some way to actually generate the next instance of a daily or
weekly task once it was marked complete, rather than just storing the frequency
as an unused label. I updated my final UML diagram in Phase 6 to reflect both
of these additions.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers two constraints: the owner's available minutes per day
and each task's priority (low/medium/high). I decided priority mattered most,
so `build_daily_plan()` sorts tasks by priority first, then greedily adds tasks
in that order as long as they still fit in the remaining time. Time available
acts as a hard cutoff — once the budget is used up, no more tasks are added,
regardless of their priority.

**b. Tradeoffs**

The scheduler uses a greedy algorithm rather than an optimal one: it can skip a
better combination of tasks in favor of an earlier, slightly wasteful choice.
For example, a large medium-priority task might get skipped in favor of two
smaller low-priority tasks that fit afterward, even though the medium-priority
task is arguably more valuable to fit in. I chose greedy because it's simple,
fast, and easy to explain to a user — an optimal solution (like a knapsack
algorithm) would be more complex and harder to justify in plain language for a
pet-care app. Similarly, my conflict detection only checks exact time-window
overlaps between tasks that have a `start_time` set; tasks without a start time
are simply skipped in that check, which is a reasonable simplification given
that not every task needs a fixed time slot.

---

## 3. AI Collaboration

**a. How you used AI**

I used my AI coding assistant throughout: generating class skeletons from my
UML diagram, implementing the Scheduler's greedy algorithm, writing the
time-overlap conflict detection logic, and drafting pytest tests. It was most
helpful for translating a written plan (like a UML diagram) into working code
structure, and for explaining Python patterns like dataclasses, lambda
functions, and the `if __name__ == "__main__":` guard. Working through each
method in isolation before combining them, and testing each one manually before
writing automated tests, kept me from getting lost when something eventually
broke (like a missing `PRIORITY_WEIGHT` constant).

**b. Judgment and verification**

When my AI assistant first suggested conflict detection based only on duplicate
task titles, I accepted it for Phase 2's scope, but revisited it in Phase 4
since duplicate titles don't actually capture real scheduling conflicts. I
verified this by writing an explicit test with two tasks at overlapping times
and confirming the upgraded time-based logic caught it while the title-based
version wouldn't have.

---

## 4. Testing and Verification

**a. What you tested**

I tested: task completion status, task addition to a pet, priority-based
sorting, recurring task generation, and time-overlap conflict detection. These
cover the core "smart" behaviors of the app — without them, a bug in sorting or
conflict detection could silently produce a wrong daily plan that looks correct
at a glance.

**b. Confidence**

I'm confident (4/5) in the core scheduling logic since it's covered by passing
tests. I'd want to add edge case tests next: an owner with zero available
minutes, a pet with no tasks at all, and tasks with identical priority and
identical start times.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the `Scheduler` class — separating sorting, planning,
conflict detection, and explanation into distinct, individually-tested methods
made the whole system easy to reason about and debug, even as I added new
behavior in later phases.

**b. What you would improve**

With another iteration, I'd replace the greedy algorithm with a smarter
optimization approach, and let recurring tasks automatically reappear in the
schedule rather than requiring a separate call to `get_next_occurrence()`.

**c. Key takeaway**

Building small, tested pieces before combining them into bigger behavior
(`Task` → `Pet` → `Owner` → `Scheduler`) made debugging much easier than writing
everything at once. AI was fastest at generating boilerplate and explaining
unfamiliar syntax, but I still had to verify every piece of logic myself with
real tests and manual terminal checks before trusting it.