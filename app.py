import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
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


st.subheader("Owner & Pet Info")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Available minutes per day", min_value=10, max_value=600, value=90)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Persist Owner/Pet objects across reruns using session_state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_minutes_per_day=int(available_minutes))
    st.session_state.pet = Pet(name=pet_name, species=species)
    st.session_state.owner.add_pet(st.session_state.pet)

# Keep owner/pet in sync with any edits to the inputs above
st.session_state.owner.name = owner_name
st.session_state.owner.available_minutes_per_day = int(available_minutes)
st.session_state.pet.name = pet_name
st.session_state.pet.species = species

st.markdown("### Tasks")
st.caption("Add a few tasks. These feed directly into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.pet.add_task(
        Task(title=task_title, duration_minutes=int(duration), priority=priority)
    )

current_tasks = st.session_state.pet.get_tasks()
if current_tasks:
    st.write("Current tasks:")
    st.table([
        {"title": t.title, "duration_minutes": t.duration_minutes, "priority": t.priority}
        for t in current_tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    plan = scheduler.build_daily_plan()
    explanations = scheduler.explain_plan(plan)
    conflicts = scheduler.detect_conflicts(plan)

    if plan:
        st.success(f"Today's plan for {st.session_state.owner.name}:")
        for line in explanations:
            st.write(f"- {line}")
        total = sum(t.duration_minutes for t in plan)
        st.caption(f"Total time scheduled: {total} / {st.session_state.owner.available_minutes_per_day} minutes")
    else:
        st.warning("No tasks fit in the available time. Add shorter or fewer tasks.")

    if conflicts:
        for warning in conflicts:
            st.warning(warning)