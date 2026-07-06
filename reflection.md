# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

For PawPal+, I settled on four classes: `Task`, `Pet`, `Owner`, and `Scheduler`.

`Task`, `Pet`, and `Owner` are implemented as Python dataclasses because their main
job is to hold data rather than make decisions. A `Task` stores a title, duration,
priority, frequency, and completion status. A `Pet` stores its name, species, and a
list of `Task` objects. An `Owner` stores their name, how many minutes per day they
have available for pet care, and a list of `Pet` objects. This mirrors the real-world
relationship: an owner has multiple pets, and each pet has its own set of care tasks.

`Scheduler` is different — it's a plain class, not a dataclass, because it doesn't
really hold data of its own beyond a reference to the `Owner` it's working with.
Its job is entirely behavioral: sorting tasks by priority, building a daily plan
that fits within the owner's available time, detecting conflicts between tasks,
and explaining why each task was included or skipped. Separating "data" classes
from the one "decision-making" class keeps each piece easy to reason about and
test on its own.

Based on the README, I identified three core actions the app needs to support:
1. Letting a user enter basic owner and pet info (name, species).
2. Letting a user add care tasks with a duration and a priority level.
3. Generating a daily plan that fits tasks into the owner's available time,
   ordered by priority, along with an explanation of why each task made
   it into (or got left out of) the plan.

These three actions became the foundation for the UML diagram and the class
skeletons in `pawpal_system.py`.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
