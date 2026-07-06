from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=20)
    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True

def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="cat")
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task(title="Feeding", duration_minutes=10))

    assert len(pet.get_tasks()) == 1
def test_sort_by_priority_orders_high_first():
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner)

    low = Task(title="Grooming", duration_minutes=15, priority="low")
    high = Task(title="Walk", duration_minutes=20, priority="high")
    medium = Task(title="Play", duration_minutes=10, priority="medium")

    sorted_tasks = scheduler.sort_by_priority([low, high, medium])

    assert sorted_tasks == [high, medium, low]


def test_recurring_task_creates_next_occurrence():
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner)

    daily_task = Task(title="Feed", duration_minutes=10, frequency="daily", is_complete=True)
    next_task = scheduler.get_next_occurrence(daily_task)

    assert next_task is not None
    assert next_task.title == "Feed"
    assert next_task.is_complete is False


def test_detect_conflicts_flags_overlapping_times():
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner)

    task_a = Task(title="Walk", duration_minutes=30, start_time="08:00")
    task_b = Task(title="Feed", duration_minutes=20, start_time="08:15")

    conflicts = scheduler.detect_conflicts([task_a, task_b])

    assert len(conflicts) == 1
