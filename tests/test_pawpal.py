from pawpal_system import Pet, PetOwner, Scheduler, Task


def test_mark_complete_changes_status() -> None:
    task = Task("Morning walk", 30, "high")

    task.mark_complete()

    assert task.completed is True


def test_adding_a_task_increases_task_count() -> None:
    pet = Pet("Mochi", "dog")

    pet.add_task(Task("Breakfast", 10, "high"))
    pet.add_task(Task("Playtime", 20, "low"))

    assert len(pet.get_tasks()) == 2


def test_sort_by_time_orders_tasks_by_preferred_time() -> None:
    owner = PetOwner("Jordan")
    pet_one = Pet("Mochi", "dog")
    pet_two = Pet("Bean", "cat")
    pet_one.add_task(Task("Late walk", 15, "medium", time_of_day="10:00"))
    pet_two.add_task(Task("Early check", 10, "high", time_of_day="08:00"))
    owner.add_pet(pet_one)
    owner.add_pet(pet_two)

    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())

    assert [task.description for _, task in sorted_tasks] == ["Early check", "Late walk"]


def test_filter_tasks_can_target_one_pet() -> None:
    owner = PetOwner("Jordan")
    pet_one = Pet("Mochi", "dog")
    pet_two = Pet("Bean", "cat")
    pet_one.add_task(Task("Breakfast", 10, "high"))
    pet_two.add_task(Task("Playtime", 20, "low"))
    owner.add_pet(pet_one)
    owner.add_pet(pet_two)

    scheduler = Scheduler(owner)

    filtered_tasks = scheduler.filter_tasks(owner.get_all_tasks(), pet_name="Bean")

    assert len(filtered_tasks) == 1
    assert filtered_tasks[0][0].name == "Bean"


def test_completed_daily_task_creates_next_occurrence() -> None:
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", 30, "high", frequency="daily")
    pet.add_task(task)

    task.mark_complete()
    next_task = task.next_occurrence()
    if next_task is not None:
        pet.add_task(next_task)
    pet.remove_completed_tasks()

    assert len(pet.tasks) == 1
    assert pet.tasks[0].completed is False
    assert pet.tasks[0].description == "Morning walk"


def test_conflict_detection_finds_overlapping_tasks() -> None:
    owner = PetOwner("Jordan")
    pet_one = Pet("Mochi", "dog")
    pet_two = Pet("Bean", "cat")
    pet_one.add_task(Task("Walk", 30, "high", time_of_day="08:00"))
    pet_two.add_task(Task("Feed", 15, "high", time_of_day="08:10"))
    owner.add_pet(pet_one)
    owner.add_pet(pet_two)

    scheduler = Scheduler(owner)

    warnings = scheduler.detect_conflicts(owner.get_all_tasks())

    assert warnings
    assert "overlaps" in warnings[0]


def test_build_daily_schedule_creates_next_occurrence_for_recurring_tasks() -> None:
    owner = PetOwner("Jordan")
    pet = Pet("Mochi", "dog")
    recurring_task = Task("Morning walk", 30, "high", time_of_day="08:00", frequency="daily")
    pet.add_task(recurring_task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner, available_minutes=60, start_time="08:00")

    schedule = scheduler.build_daily_schedule()

    assert len(schedule) == 1
    assert len(pet.tasks) == 1
    assert pet.tasks[0].description == "Morning walk"
    assert pet.tasks[0].completed is False