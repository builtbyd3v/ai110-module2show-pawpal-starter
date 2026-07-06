import streamlit as st

from pawpal_system import Pet, PetOwner, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def initialize_state() -> None:
    """Create the session state objects the app needs."""

    if "owner" not in st.session_state:
        st.session_state.owner = PetOwner(name="Jordan")
    if "schedule" not in st.session_state:
        st.session_state.schedule = []
    if "schedule_explanations" not in st.session_state:
        st.session_state.schedule_explanations = []


def get_selected_pet() -> Pet | None:
    """Return the currently selected pet, if one exists."""

    owner: PetOwner = st.session_state.owner
    if not owner.pets:
        return None

    selected_name = st.session_state.get("selected_pet_name")
    for pet in owner.pets:
        if pet.name == selected_name:
            return pet
    return owner.pets[0]


def refresh_selected_pet_name() -> None:
    """Keep the selected pet aligned with the first available pet."""

    owner: PetOwner = st.session_state.owner
    if owner.pets:
        st.session_state.selected_pet_name = owner.pets[0].name


initialize_state()

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ helps a pet owner organize care tasks, keep the current plan in memory, and generate a daily schedule based on priorities and time.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Step 1: Establish the Connection")
st.caption("This app imports the classes from pawpal_system.py so the UI can create real objects.")

owner = st.session_state.owner

with st.form("owner_form", border=True):
    owner_name = st.text_input("Owner name", value=owner.name)
    preferences_text = st.text_input(
        "Owner preferences",
        value=", ".join(owner.preferences),
        help="Separate preferences with commas.",
    )
    save_owner = st.form_submit_button("Save owner")

if save_owner:
    owner.name = owner_name.strip() or owner.name
    preferences = [item.strip() for item in preferences_text.split(",") if item.strip()]
    owner.update_preferences(preferences)
    st.session_state.owner = owner
    st.success("Owner saved to session state.")

st.divider()

st.subheader('Step 2: Manage the Application "Memory"')
st.caption("Session state keeps the owner, pets, and tasks available while you use the app.")

with st.form("pet_form", border=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=40, value=5)
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    pet = Pet(name=pet_name.strip() or "Unnamed pet", species=species, age=int(age))
    owner.add_pet(pet)
    st.session_state.owner = owner
    refresh_selected_pet_name()
    st.success(f"Added {pet.name} to memory.")

if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    if "selected_pet_name" not in st.session_state or st.session_state.selected_pet_name not in pet_names:
        st.session_state.selected_pet_name = pet_names[0]

    st.selectbox(
        "Choose a pet",
        pet_names,
        key="selected_pet_name",
        help="Pick which pet receives the next task.",
    )
else:
    st.info("Add at least one pet before creating tasks.")

selected_pet = get_selected_pet()

with st.form("task_form", border=True):
    task_description = st.text_input("Task description", value="Morning walk")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    time_of_day = st.text_input("Preferred time", value="08:00")
    category = st.text_input("Category", value="care")
    frequency = st.selectbox("Frequency", ["daily", "weekly", "one-time"], index=0)
    add_task = st.form_submit_button("Add task")

if add_task:
    if selected_pet is None:
        st.error("Add a pet first so the task has somewhere to go.")
    else:
        selected_pet.add_task(
            Task(
                description=task_description.strip() or "Untitled task",
                duration_minutes=int(duration),
                priority=priority,
                time_of_day=time_of_day.strip() or None,
                category=category.strip() or "general",
                frequency=frequency,
            )
        )
        st.session_state.owner = owner
        st.success(f"Added a task for {selected_pet.name}.")

if owner.pets:
    st.markdown("### Current pets and tasks")
    for pet in owner.pets:
        st.write(f"**{pet.name}** ({pet.species})")
        if pet.tasks:
            st.table(
                [
                    {
                        "description": task.description,
                        "duration_minutes": task.duration_minutes,
                        "priority": task.priority,
                        "time_of_day": task.time_of_day or "-",
                        "category": task.category,
                        "frequency": task.frequency,
                        "completed": task.completed,
                    }
                    for task in pet.tasks
                ]
            )
        else:
            st.caption("No tasks yet.")

st.divider()

st.subheader("Step 3: Wiring UI Actions to Logic")
st.caption("Generate a schedule from the owner and all of their pets' tasks.")

available_minutes = st.slider("Available minutes", min_value=30, max_value=480, value=180, step=15)
start_time = st.text_input("Start time", value="08:00")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=owner, available_minutes=available_minutes, start_time=start_time)
    schedule = scheduler.build_daily_schedule()
    explanations = scheduler.explain_plan(schedule)
    st.session_state.schedule = schedule
    st.session_state.schedule_explanations = explanations

if st.session_state.schedule:
    st.markdown("### Today's Schedule")
    st.table(st.session_state.schedule)

if st.session_state.schedule_explanations:
    st.markdown("### Why this plan was chosen")
    for explanation in st.session_state.schedule_explanations:
        st.write(f"- {explanation}")

st.divider()

st.markdown(
    """
**Checkpoint:** `app.py` now imports the logic layer, stores the owner in session state, adds pets and tasks into that memory, and generates a schedule from the stored data.
"""
)
