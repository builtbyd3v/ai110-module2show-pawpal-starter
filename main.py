from pawpal_system import Pet, PetOwner, Scheduler, Task


def format_schedule_line(item: dict[str, str | int]) -> str:
    """Format one schedule item for terminal output."""

    return (
        f"{item['start_time']} - {item['end_time']} | "
        f"{item['pet_name']}: {item['task_description']} "
        f"({item['duration_minutes']} min, {item['priority']}, {item['frequency']})"
    )


def format_task_label(pet: Pet, task: Task) -> str:
    """Format one task for the terminal demo."""

    return (
        f"{pet.name}: {task.description} "
        f"({task.time_of_day or 'no time'}, {task.duration_minutes} min, {task.priority})"
    )


def main() -> None:
    """Build and print a sample PawPal+ daily schedule."""

    owner = PetOwner(name="Jordan")
    dog = Pet(name="Mochi", species="dog", age=5)
    cat = Pet(name="Bean", species="cat", age=3)

    dog.add_task(Task("Morning walk", 30, "high", time_of_day="08:00"))
    dog.add_task(Task("Breakfast", 10, "high", time_of_day="08:30", frequency="daily"))
    cat.add_task(Task("Litter box check", 15, "medium", time_of_day="08:25"))
    cat.add_task(Task("Play session", 20, "low", time_of_day="10:00"))
    cat.add_task(Task("Vet reminder", 5, "low", time_of_day="08:30", frequency="weekly"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner=owner, available_minutes=120, start_time="08:00")

    raw_tasks = owner.get_all_tasks()
    sorted_by_time = scheduler.sort_by_time(raw_tasks)
    filtered_for_mochi = scheduler.filter_tasks(raw_tasks, pet_name="Mochi")
    conflict_warnings = scheduler.detect_conflicts(raw_tasks)
    schedule = scheduler.build_daily_schedule()
    explanations = scheduler.explain_plan(schedule)

    print("Unsorted task list")
    print("------------------")
    for pet, task in raw_tasks:
        print(format_task_label(pet, task))

    print()
    print("Sorted by time")
    print("--------------")
    for pet, task in sorted_by_time:
        print(format_task_label(pet, task))

    print()
    print("Filtered for Mochi")
    print("-------------------")
    for pet, task in filtered_for_mochi:
        print(format_task_label(pet, task))

    print()
    print("Conflict warnings")
    print("-----------------")
    if conflict_warnings:
        for warning in conflict_warnings:
            print(f"- {warning}")
    else:
        print("- No conflicts found.")

    print()
    print("Today's Schedule")
    print("-----------------")
    for item in schedule:
        print(format_schedule_line(item))

    print()
    print("Why this plan was chosen")
    print("-------------------------")
    for explanation in explanations:
        print(f"- {explanation}")

    print()
    print("Recurring tasks after scheduling")
    print("-------------------------------")
    for pet in owner.pets:
        for task in pet.tasks:
            print(format_task_label(pet, task))


if __name__ == "__main__":
    main()