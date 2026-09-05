import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Heat Pump Diagnostic Tool",
    page_icon="🔧",
    layout="centered",
)

st.title("🔧 Heat Pump Diagnostic Tool")
st.markdown(
    "Please complete the initial details below to begin the sequential diagnostic process."
)

# --- SECTION 1: Customer & System Details ---
st.header("1. Customer & System Information")

col1, col2 = st.columns(2)
with col1:
    customer_name = st.text_input("Customer Name")
    postcode = st.text_input("Postcode")
address = st.text_area("Address")

col3, col4 = st.columns(2)
with col3:
    hp_make = st.text_input("Heat Pump Make (e.g., Samsung, Daikin, Mitsubishi)")
with col4:
    hp_model = st.text_input("Heat Pump Model (e.g., EHS Mono Gen6)")

hp_kw = st.number_input(
    "Heat Pump Size (kW)", min_value=1.0, max_value=50.0, step=0.5, value=8.0
)

st.divider()

# --- SECTION 2: Reported Issues (Multi-Select) ---
st.header("2. Reported Issues")
st.markdown(
    "Select all symptoms or fault codes reported by the customer or controller:"
)

issue_options = [
    "E199 / E153 (Flow Rate / Circulation Error)",
    "Low Delta T at full load",
    "Compressor failing to start / Inverter Fault",
    "Frequent defrost cycles / Ice buildup",
    "Communication error between indoor and outdoor unit",
    "Other / Custom Issue",
]

selected_issues = st.multiselect("Active Faults / Symptoms", issue_options)

custom_issue = ""
if "Other / Custom Issue" in selected_issues:
    custom_issue = st.text_input(
        "Please describe the custom issue reported by the customer:"
    )

st.divider()

# --- SECTION 3: Sequential Diagnostic Questionnaire ---
st.header("3. Sequential Diagnostic Questionnaire")
st.markdown(
    "Work through the relevant active phases below in sequence to isolate root causes."
)

# Track answers across sections
e_q1, e_q2 = "Select", "Select"
h_q1, h_q2, h_q3 = "Select", "Select", "Select"
c_q1, c_q2 = "Select", "Select"

# Determine which sequence blocks to display based on selected issues
has_electrical = any(
    "Compressor" in issue or "Communication" in issue for issue in selected_issues
)
has_hydraulic = any(
    "Flow Rate" in issue or "Low Delta T" in issue or "Defrost" in issue
    for issue in selected_issues
)

# --- Phase 1: Electrical & Safety Checks (Always first if electrical/comm selected, or general fallback) ---
if has_electrical or not selected_issues:
    st.markdown("### Phase 1: Electrical & Power Diagnostics")
    st.image(
        "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=600&auto=format&fit=crop&q=80",
        caption="Step 1: Electrical Safety & Supply",
        width=300,
    )
    e_q1 = st.radio(
        "1.1 Is there a stable mains voltage supply at the outdoor unit terminals?",
        ("Select", "Yes", "No"),
        key="eq1",
    )
    e_q2 = st.radio(
        "1.2 Are communication wiring and inverter fuses intact and secure?",
        ("Select", "Yes", "No"),
        key="eq2",
    )
    st.divider()

# --- Phase 2: Hydraulic & Flow Checks ---
if has_hydraulic or not selected_issues:
    st.markdown("### Phase 2: Hydraulic & Circulation Diagnostics")
    st.image(
        "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=600&auto=format&fit=crop&q=80",
        caption="Step 2: Hydronic Balancing & Flow",
        width=300,
    )
    h_q1 = st.radio(
        "2.1 Are all system isolation and lockshield valves fully open?",
        ("Select", "Yes", "No"),
        key="hq1",
    )
    h_q2 = st.radio(
        "2.2 Is the primary magnetic inline filter/strainer clear of debris?",
        ("Select", "Yes", "No"),
        key="hq2",
    )
    h_q3 = st.radio(
        "2.3 Is system pressure stable (1.0 - 1.5 bar) and free of trapped air?",
        ("Select", "Yes", "No"),
        key="hq3",
    )
    st.divider()

# --- Phase 3: General System & Controller Checks ---
st.markdown("### Phase 3: Controller & Operational Reset")
st.image(
    "https://images.unsplash.com/photo-1544717305-2782549b5136?w=600&auto=format&fit=crop&q=80",
    caption="Step 3: System State & Hard Reboot",
    width=300,
)
c_q1 = st.radio(
    "3.1 Is the controller displaying active hard lockout logs?",
    ("Select", "Yes", "No"),
    key="cq1",
)
c_q2 = st.radio(
    "3.2 Have you performed a complete hard power cycle (reboot) of the system?",
    ("Select", "Yes", "No"),
    key="cq2",
)

st.divider()

# --- SECTION 4: Remediation Plan Generation ---
if st.button("Generate Final Diagnostic Summary", type="primary"):
    if not customer_name or not hp_make or not selected_issues:
        st.error(
            "Please ensure Customer Name, Heat Pump Make, and at least one Reported Issue are provided."
        )
    else:
        st.success("Sequential analysis complete based on technician inputs:")

        st.subheader("Job Summary")
        st.markdown(f"**Customer:** {customer_name}")
        st.markdown(f"**Address:** {address if address else 'N/A'}, {postcode}")
        st.markdown(
            f"**Target System:** {hp_make} - {hp_model} ({hp_kw} kW)"
        )
        st.markdown(
            f"**Reported Issues:** {', '.join(selected_issue for selected_issue in selected_issues)}"
        )
        if custom_issue:
            st.markdown(f"**Custom Details:** {custom_issue}")

        st.subheader("Prioritised Actionable Next Steps:")

        # Phase 1 Remediation
        if e_q1 == "No":
            st.warning(
                "• **[Phase 1] Power Supply:** Check incoming isolator, circuit breakers, and supply voltage at the unit."
            )
        if e_q2 == "No":
            st.warning(
                "• **[Phase 1] Wiring/Fuses:** Inspect data cable screening, terminal tightness, and inverter board fuses."
            )

        # Phase 2 Remediation
        if h_q1 == "No":
            st.warning(
                "• **[Phase 2] Isolation Valves:** Open all primary circuit and radiator lockshield valves fully."
            )
        if h_q2 == "No":
            st.warning(
                "• **[Phase 2] Strainer Maintenance:** Isolate, drain locally, and clean the magnetic filter."
            )
        if h_q3 == "No":
            st.warning(
                "• **[Phase 2] System Pressure:** Recharge system pressure to target operating limits and bleed air vents."
            )

        # Phase 3 Remediation
        if c_q2 == "No":
            st.warning(
                "• **[Phase 3] Hard Reset:** Kill mains power for 5 minutes to clear transient controller latches."
            )

        all_answers = [e_q1, e_q2, h_q1, h_q2, h_q3, c_q1, c_q2]
        if all(
            ans in ("Yes", "Select") for ans in all_answers
        ):  # Adjust if unselected fields remain
            st.info(
                "• All sequential checks completed. Escalate to manufacturer technical support if faults persist."
            )
