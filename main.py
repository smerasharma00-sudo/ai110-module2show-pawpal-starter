from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    jordan = Owner(name="Jordan", available_minutes_per_day=90)

    mochi = Pet(name="Mochi", species="cat")
    mochi.add_task(Task(title="Morning walk", duration_minutes=20, priority="high"))
    mochi.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    mochi.add_task(Task(title="Litter box cleaning", duration_minutes=15, priority="medium"))

    biscuit = Pet(name="Biscuit", species="dog")
    biscuit.add_task(Task(title="Evening walk", duration_minutes=30, priority="high"))
    biscuit.add_task(Task(title="Playtime", duration_minutes=25, priority="low"))

    jordan.add_pet(mochi)
    jordan.add_pet(biscuit)
    scheduler = Scheduler(jordan)
    plan = scheduler.build_daily_plan()
    explanations = scheduler.explain_plan(plan)
    conflicts = scheduler.detect_conflicts(plan)

    print("=" * 40)
    print(f"Today's Schedule for {jordan.name}")
    print(f"Available time: {jordan.available_minutes_per_day} minutes")
    print("=" * 40)

    total_minutes = 0
    for task, explanation in zip(plan, explanations):
        print(f"- {explanation}")
        total_minutes += task.duration_minutes

    print("-" * 40)
    print(f"Total time scheduled: {total_minutes} / {jordan.available_minutes_per_day} minutes")

    if conflicts:
        print("\nWarnings:")
        for warning in conflicts:
            print(f"- {warning}")
    else:
        print("\nNo conflicts detected.")
if __name__ == "__main__":
    main()