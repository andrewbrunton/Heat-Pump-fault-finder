import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Heat Pump Field Diagnostic Assistant",
    page_icon="🔧",
    layout="centered",
)

# Application Header
st.title("Heat Pump Diagnostic Assistant")
st.markdown(
    "Field-side troubleshooting tool for heating engineers and technicians."
)
st.markdown("---")

# 1. Make and Model Selection Database
heat_pump_database = {
    "Samsung": {
        "models": [
            "Samsung EHS Mono Gen6 (R32)",
            "Samsung EHS Split",
            "Samsung EHS TDM Plus",
        ],
        "common_errors": [
            "E199 / E153 (Flow Rate / Circulation Error)",
            "E425 / E458 (Fan Motor / Communication Fault)",
            "E202 (Indoor/Outdoor Unit Communication Loss)",
            "Low COP / High Electrical Consumption",
        ],
    },
    "Mitsubishi Electric": {
        "models": [
            "Mitsubishi Ecodan FTC5 (Monobloc/Split)",
            "Mitsubishi Ecodan FTC6 (Monobloc/Split)",
        ],
        "common_errors": [
            "Error Code P8 / E6 (Sensor / Communication Fault)",
            "Error Code U4 / U5 (Phase / Power Supply Fault)",
            "Rapid Cycling / Short Run Times",
            "Inadequate Domestic Hot Water Recovery",
        ],
    },
    "Vaillant": {
        "models": [
            "Vaillant aroTHERM Plus (R290)",
            "Vaillant aroTHERM Split",
        ],
        "common_errors": [
            "F.32 / F.73 (Flow Sensor / Pressure Sensor Fault)",
            "F.530 (Low Glycol / Flow Deficit)",
            "Compressor Lockout / High Discharge Temp",
        ],
    },
}

# Sidebar Selection
st.sidebar.header("1. System Identification")
selected_manufacturer = st.sidebar.selectbox(
    "Select Manufacturer", list(heat_pump_database.keys())
)
selected_model = st.sidebar.selectbox(
    "Select Model Series", heat_pump_database[selected_manufacturer]["models"]
)
selected_fault = st.sidebar.selectbox(
    "Select Primary Symptom / Error Code",
    heat_pump_database[selected_manufacturer]["common_errors"],
)

st.sidebar.markdown("---")
st.sidebar.info(
    f"**Active Profile:** {selected_manufacturer} - {selected_model}"
)

# Main Diagnostic Interface
st.subheader(f"Diagnostic Workflow: {selected_fault}")
st.markdown(
    "Work through the key checks below. Expand the **Guidance & How-To** section for step-by-step testing instructions and expected field benchmarks."
)

# Diagnostic Steps with Integrated Guidance
tabs = st.tabs(
    ["1. Flow & Hydraulics", "2. Sensors & Electronics", "3. System Settings"]
)

with tabs[0]:
    st.markdown("### Volumetric Flow & Delta T Verification")

    col1, col2 = st.columns(2)
    with col1:
        flow_status = st.radio(
            "Is flow rate within manufacturer specification?",
            ["Unknown / Not Tested", "Yes, verified stable", "No / Flow error active"],
            key="flow_check",
        )
    with col2:
        delta_t_val = st.number_input(
            "Measured Primary Delta T (°C) at full load:",
            min_value=0.0,
            max_value=20.0,
            value=5.0,
            step=0.5,
        )

    # Contextual Guidance Expander
    with st.expander("📖 Guidance: How to test Flow Rate and Delta T"):
        st.markdown("""
        * **Tools Required:** Calibrated twin-probe digital contact thermometer with thermal paste/insulation wrap, and differential pressure manometer if checking pump head.
        * **Procedure:**
          1. Force the unit into continuous space-heating mode at full design capacity.
          2. Attach sensors directly to the main primary flow and return pipes close to the unit, stripping away old pipe insulation at the contact point.
          3. Wrap probes securely with thermal insulation tape to prevent ambient air cooling interference.
          4. Allow readings to stabilise for 3 to 5 minutes before noting the differential.
        * **Field Benchmarks:** 
          * **Delta T > 8°C to 10°C:** Indicates restricted flow, blocked Y-strainer mesh, or severe hydronic resistance.
          * **Delta T < 3°C:** Indicates excessive pump speed, volumetric short-circuiting, or hydraulic bypass issues.
        """)

    if delta_t_val > 8.0:
        st.warning(
            "⚠️ High Delta T detected. Inspect primary Y-strainer, check for trapped air in the plate heat exchanger, and verify circulator pump duty settings."
        )
    elif delta_t_val < 3.0 and delta_t_val > 0:
        st.info(
            "ℹ️ Low Delta T detected. Check for hydraulic short-circuiting across a buffer vessel or low-loss header."
        )

with tabs[1]:
    st.markdown("### Sensor Calibration & Resistance Check")

    sensor_checked = st.checkbox(
        "I have checked flow and return thermistor resistance values against manufacturer tables."
    )

    with st.expander("📖 Guidance: How to check NTC Thermistors"):
        st.markdown("""
        * **Tools Required:** Digital multimeter set to ohms (Ω).
        * **Procedure:**
          1. Isolate all electrical power to the heat pump completely.
          2. Disconnect the sensor plug from the main controller board.
          3. Measure resistance across the sensor terminals.
          4. Measure current water or ambient temperature using a digital probe.
          5. Cross-reference your ohm reading against the manufacturer's NTC resistance temperature chart.
        * **Field Benchmarks:** A drifting sensor (e.g., showing 10°C when pipe is at 35°C) will cause premature cycling or incorrect modulation. Replace any thermistor showing erratic resistance swings.
        """)

with tabs[2]:
    st.markdown("### Controller Configuration & Weather Compensation")

    curve_status = st.selectbox(
        "Weather compensation curve setting:",
        [
            "Select status...",
            "Correctly mapped to building heat loss",
            "Too aggressive (high flow temps at moderate outdoor temps)",
            "Unaligned / Factory default",
        ],
    )

    with st.expander("📖 Guidance: How to configure Weather Compensation"):
        st.markdown("""
        * **Procedure:**
          1. Check design outdoor temperature for your geographic region (e.g., -4°C to -6°C for many UK locations).
          2. Verify that maximum design flow temperature aligns with emitter sizing (e.g., strictly capped at 50°C to 55°C for heat pump compatibility).
          3. Ensure parallel shift is adjusted so the property maintains comfort without over-shooting during mild shoulder seasons.
        """)

st.markdown("---")

# Summary & Remediation Action Plan Generator
st.subheader("💡 Recommended Remediation Action Plan")

if st.button("Generate Final Diagnostic Summary"):
    st.success("Analysis complete based on technician inputs:")
    st.markdown(f"""
    * **Target System:** {selected_manufacturer} - {selected_model}
    * **Reported Issue:** {selected_fault}
    * **Actionable Next Steps:**
      1. Inspect the primary circuit Y-strainer and magnetic filter for particulate accumulation.
      2. Verify that minimum system water volume thresholds are met (check buffer vessel integration).
      3. Confirm that circulator pump residual head matches system hydraulic resistance curves.
    """)
else:
    st.info(
        "Complete the diagnostic tabs above and click the button to compile the custom action plan."
    )
