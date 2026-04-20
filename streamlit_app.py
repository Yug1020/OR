import streamlit as st
import simpy       
import random
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Verve Tech Fest System", layout="wide")

st.title("🎉 Verve Tech Fest (VIT) Queue Management System")
st.markdown("### Optimize event participation using simulation and queuing theory")

# 🔧 SIDEBAR INPUTS
st.sidebar.header("⚙️ Simulation Controls")

num_reg = st.sidebar.slider("Registration Counters", 1, 5, 2)
num_tech = st.sidebar.slider("No. of Tech Events", 1, 5, 3)
num_nontech = st.sidebar.slider("No. of Non-Tech Events", 1, 5, 2)

arrival_rate = st.sidebar.slider("Arrival Rate (participants/min)", 1, 10, 2)
sim_time = st.sidebar.slider("Simulation Time (minutes)", 100, 1000, 480)

# ⏱️ Service time constants (in minutes)
REG_TIME = 3
TECH_TIME = 10
NONTECH_TIME = 5

# 📊 Storage
wait_times = {
    "Registration": [],
    "Tech Events": [],
    "Non-Tech Events": []
}

total_time = []

# 🧠 SIMULATION LOGIC
def participant(env, reg, tech, nontech):
    arrival = env.now

    # Registration
    with reg.request() as req:
        start = env.now
        yield req
        wait_times["Registration"].append(env.now - start)
        yield env.timeout(random.expovariate(1 / REG_TIME))

    # Tech Event
    with tech.request() as req:
        start = env.now
        yield req
        wait_times["Tech Events"].append(env.now - start)
        yield env.timeout(random.expovariate(1 / TECH_TIME))

    # Non-Tech Event
    with nontech.request() as req:
        start = env.now
        yield req
        wait_times["Non-Tech Events"].append(env.now - start)
        yield env.timeout(random.expovariate(1 / NONTECH_TIME))

    total_time.append(env.now - arrival)


def arrival(env, reg, tech, nontech):
    while True:
        yield env.timeout(random.expovariate(arrival_rate))
        env.process(participant(env, reg, tech, nontech))


def run_simulation():
    random.seed(42)
    env = simpy.Environment()

    reg = simpy.Resource(env, capacity=num_reg)
    tech = simpy.Resource(env, capacity=num_tech)
    nontech = simpy.Resource(env, capacity=num_nontech)

    env.process(arrival(env, reg, tech, nontech))
    env.run(until=sim_time)


# ▶️ RUN BUTTON
if st.button("🚀 Run Simulation"):

    # Reset data
    for k in wait_times:
        wait_times[k] = []
    total_time.clear()

    run_simulation()

    st.subheader("📊 Key Results")

    col1, col2, col3 = st.columns(3)

    avg_tech = np.mean(wait_times["Tech Events"])
    avg_total = np.mean(total_time)
    participants = len(total_time)

    col1.metric("💻 Avg Tech Event Wait", f"{avg_tech:.2f} min")
    col2.metric("👥 Participants Served", participants)
    col3.metric("⏱ Avg Total Time", f"{avg_total:.2f} min")

    # 📈 GRAPH
    st.subheader("📈 Waiting Time at Each Stage")

    stages = list(wait_times.keys())
    values = [np.mean(wait_times[s]) for s in stages]

    fig, ax = plt.subplots()
    ax.bar(stages, values)
    ax.set_ylabel("Avg Waiting Time (min)")
    ax.set_title("Event Queue Performance")

    st.pyplot(fig)

    # 🚨 BOTTLENECK DETECTION
    max_stage = stages[np.argmax(values)]
    st.warning(f"🚨 Bottleneck detected at: {max_stage}")

    # 💰 COST ANALYSIS
    st.subheader("💰 Cost Analysis")

    cost = (
        num_tech * 3000 +
        num_reg * 1000 +
        num_nontech * 1000
    )

    st.write(f"Estimated Event Cost: ₹{cost}")

    st.info("💡 Recommendation: Increase capacity at bottleneck stage to reduce waiting time.")

# import streamlit as st
# import simpy
# import random
# import numpy as np
# import matplotlib.pyplot as plt

# st.set_page_config(page_title="Hospital Queue System", layout="wide")

# st.title("🏥 Hospital Queue Management System")
# st.markdown("### Optimize hospital resources using simulation and queuing theory")

# # 🔧 SIDEBAR INPUTS
# st.sidebar.header("⚙️ Simulation Controls")

# num_reg = st.sidebar.slider("Registration Counters", 1, 5, 2)
# num_doc = st.sidebar.slider("Doctors", 1, 5, 3)
# num_pharm = st.sidebar.slider("Pharmacy Counters", 1, 5, 2)
# num_bill = st.sidebar.slider("Billing Counters", 1, 3, 1)

# arrival_rate = st.sidebar.slider("Arrival Rate (patients/min)", 0.1, 1.0, 0.2)
# sim_time = st.sidebar.slider("Simulation Time (minutes)", 100, 1000, 480)

# # Service time constants
# REG_TIME = 3
# DOC_TIME = 10
# PHARM_TIME = 5
# BILL_TIME = 2

# # Storage
# wait_times = {
#     "Registration": [],
#     "Doctor": [],
#     "Pharmacy": [],
#     "Billing": []
# }

# total_time = []

# # 🧠 SIMULATION LOGIC
# def patient(env, reg, doc, pharm, bill):
#     arrival = env.now

#     with reg.request() as req:
#         start = env.now
#         yield req
#         wait_times["Registration"].append(env.now - start)
#         yield env.timeout(random.expovariate(1/REG_TIME))

#     with doc.request() as req:
#         start = env.now
#         yield req
#         wait_times["Doctor"].append(env.now - start)
#         yield env.timeout(random.expovariate(1/DOC_TIME))

#     with pharm.request() as req:
#         start = env.now
#         yield req
#         wait_times["Pharmacy"].append(env.now - start)
#         yield env.timeout(random.expovariate(1/PHARM_TIME))

#     with bill.request() as req:
#         start = env.now
#         yield req
#         wait_times["Billing"].append(env.now - start)
#         yield env.timeout(random.expovariate(1/BILL_TIME))

#     total_time.append(env.now - arrival)


# def arrival(env, reg, doc, pharm, bill):
#     while True:
#         yield env.timeout(random.expovariate(arrival_rate))
#         env.process(patient(env, reg, doc, pharm, bill))


# def run_simulation():
#     random.seed(42)
#     env = simpy.Environment()

#     reg = simpy.Resource(env, capacity=num_reg)
#     doc = simpy.Resource(env, capacity=num_doc)
#     pharm = simpy.Resource(env, capacity=num_pharm)
#     bill = simpy.Resource(env, capacity=num_bill)

#     env.process(arrival(env, reg, doc, pharm, bill))
#     env.run(until=sim_time)


# # ▶️ RUN BUTTON
# if st.button("🚀 Run Simulation"):

#     # Reset data
#     for k in wait_times:
#         wait_times[k] = []
#     total_time.clear()

#     run_simulation()

#     st.subheader("📊 Key Results")

#     col1, col2, col3 = st.columns(3)

#     avg_doc = np.mean(wait_times["Doctor"])
#     avg_total = np.mean(total_time)
#     patients = len(total_time)

#     col1.metric("👨‍⚕️ Avg Doctor Wait", f"{avg_doc:.2f} min")
#     col2.metric("👥 Patients Served", patients)
#     col3.metric("⏱ Avg Total Time", f"{avg_total:.2f} min")

#     # 📈 GRAPH
#     st.subheader("📈 Waiting Time at Each Stage")

#     stages = list(wait_times.keys())
#     values = [np.mean(wait_times[s]) for s in stages]

#     fig, ax = plt.subplots()
#     ax.bar(stages, values)
#     ax.set_ylabel("Avg Waiting Time (min)")
#     ax.set_title("Queue Performance")

#     st.pyplot(fig)

#     # 🚨 BOTTLENECK
#     max_stage = stages[np.argmax(values)]
#     st.warning(f"🚨 Bottleneck detected at: {max_stage}")

#     # 💰 COST ANALYSIS
#     st.subheader("💰 Cost Analysis")

#     cost = (
#         num_doc * 3000 +
#         num_reg * 1000 +
#         num_pharm * 1000 +
#         num_bill * 1000
#     )

#     st.write(f"Estimated Daily Cost: ₹{cost}")

#     st.info("💡 Recommendation: Increase servers at bottleneck stage to reduce waiting time.")
