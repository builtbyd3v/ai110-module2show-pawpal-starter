from pawpal_system import Pet, Task


def test_mark_complete_changes_status() -> None:
    task = Task("Morning walk", 30, "high")

    task.mark_complete()

    assert task.completed is True


def test_adding_a_task_increases_task_count() -> None:
    pet = Pet("Mochi", "dog")

    pet.add_task(Task("Breakfast", 10, "high"))
    pet.add_task(Task("Playtime", 20, "low"))

    assert len(pet.get_tasks()) == 2