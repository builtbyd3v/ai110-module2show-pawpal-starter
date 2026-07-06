from pawpal_system import Pet, PetOwner, Scheduler, Task


def format_schedule_line(item: dict[str, str | int]) -> str:
    """Format one schedule item for terminal output."""

    return (
        f"{item['start_time']} - {item['end_time']} | "
        f"{item['pet_name']}: {item['task_description']} "
        f"({item['duration_minutes']} min, {item['priority']}, {item['frequency']})"
    )


def main() -> None:
    """Build and print a sample PawPal+ daily schedule."""

    owner = PetOwner(name="Jordan")
    dog = Pet(name="Mochi", species="dog", age=5)
    cat = Pet(name="Bean", species="cat", age=3)

    dog.add_task(Task("Morning walk", 30, "high", time_of_day="08:00"))
    dog.add_task(Task("Breakfast", 10, "high", time_of_day="08:40"))
    cat.add_task(Task("Litter box check", 15, "medium", time_of_day="09:00"))
    cat.add_task(Task("Play session", 20, "low", time_of_day="10:00"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner=owner, available_minutes=120, start_time="08:00")
    schedule = scheduler.build_daily_schedule()
    explanations = scheduler.explain_plan(schedule)

    print("Today's Schedule")
    print("-----------------")
    for item in schedule:
        print(format_schedule_line(item))

    print()
    print("Why this plan was chosen")
    print("-------------------------")
    for explanation in explanations:
        print(f"- {explanation}")


if __name__ == "__main__":
    main()