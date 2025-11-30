import streamlit as st

# ----------------------------
# BASIC PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="DecisionGuide", layout="centered")

st.title("DecisionGuide")
st.write("A simple, logic-based assistant for governance and audit decisions.")


# ----------------------------
# TREE 1: INCIDENT REPORTING
# ----------------------------
def tree_incident_reporting():
    st.subheader("Tree 1 – Vendor Incident Reporting")

    path = []

    q1 = st.radio(
        "1. Does this vendor process personal or sensitive data on your behalf?",
        ["Select...", "Yes", "No"],
        index=0,
        key="ir_q1",
    )
    path.append(f"Q1 → {q1}")

    if q1 == "Select...":
        return None, None, path

    if q1 == "No":
        decision = "ACCEPT"
        explanation = (
            "The vendor does not process personal or sensitive data on your behalf. "
            "Strict incident notification requirements are not triggered. You can still "
            "include a generic incident notification clause as good practice."
        )
        return decision, explanation, path

    # If Yes:
    q2 = st.radio(
        "2. Is there a regulatory or contractual incident/breach reporting requirement "
        "(for example GDPR/UK GDPR, sector rules, or customer contracts)?",
        ["Select...", "Yes", "No"],
        index=0,
        key="ir_q2",
    )
    path.append(f"Q2 → {q2}")

    if q2 == "Select...":
        return None, None, path

    if q2 == "No":
        decision = "ACCEPT_WITH_MITIGATION"
        explanation = (
            "There is no explicit regulatory or upstream contractual incident notification "
            "timeframe, but the vendor processes personal or sensitive data. You should "
            "define a reasonable notification time window in the contract for governance "
            "and monitoring purposes."
        )
        return decision, explanation, path

    # If Yes:
    q3 = st.radio(
        "3. What is your required maximum incident notification timeframe?",
        ["Select...", "24 hours", "48 hours", "72 hours"],
        index=0,
        key="ir_q3",
    )
    path.append(f"Q3 → {q3}")

    if q3 == "Select...":
        return None, None, path

    # Map to numeric
    required_hours = int(q3.split()[0])

    q4 = st.radio(
        f"4. Can the vendor contractually commit to notify you within {required_hours} hours?",
        ["Select...", "Yes", "No"],
        index=0,
        key="ir_q4",
    )
    path.append(f"Q4 → {q4}")

    if q4 == "Select...":
        return None, None, path

    if q4 == "Yes":
        decision = "ACCEPT"
        explanation = (
            f"The vendor agrees to a {required_hours}-hour notification window, which "
            "aligns with your internal standard and regulatory expectations. This supports "
            "timely internal escalation and external reporting where required."
        )
        return decision, explanation, path

    # If vendor cannot meet required window:
    q5 = st.radio(
        "5. Can you introduce compensating controls (for example enhanced monitoring, "
        "stricter SLAs, high-priority incident routing)?",
        ["Select...", "Yes", "No"],
        index=0,
        key="ir_q5",
    )
    path.append(f"Q5 → {q5}")

    if q5 == "Select...":
        return None, None, path

    if q5 == "Yes":
        decision = "ACCEPT_WITH_MITIGATION"
        explanation = (
            "The vendor cannot meet your preferred incident notification timeframe, but "
            "you can introduce compensating controls such as enhanced monitoring and "
            "prioritised escalation. The risk is reduced but should be documented and "
            "periodically reviewed."
        )
        return decision, explanation, path

    decision = "REJECT"
    explanation = (
        "The vendor cannot meet your required notification timeframe and you cannot put "
        "effective compensating controls in place. The residual risk remains too high, "
        "so you should consider alternative vendors or a different solution."
    )
    return decision, explanation, path


# ----------------------------
# TREE 2: VENDOR DATA RISK CLASSIFICATION
# ----------------------------
def tree_vendor_classification():
    st.subheader("Tree 2 – Vendor Data Risk Classification")

    path = []

    q1 = st.radio(
        "1. Does the vendor handle personal data?",
        ["Select...", "No data", "Personal data", "Special category / highly sensitive data"],
        index=0,
        key="vc_q1",
    )
    path.append(f"Q1 → {q1}")

    if q1 == "Select...":
        return None, None, path

    q2 = st.radio(
        "2. What is the scale of processing?",
        ["Select...", "Small (few records, low volume)", "Medium", "Large (high volume / continuous)"],
        index=0,
        key="vc_q2",
    )
    path.append(f"Q2 → {q2}")

    if q2 == "Select...":
        return None, None, path

    q3 = st.radio(
        "3. Does the vendor connect to your core systems or internal network?",
        ["Select...", "Yes", "No"],
        index=0,
        key="vc_q3",
    )
    path.append(f"Q3 → {q3}")

    if q3 == "Select...":
        return None, None, path

    # Simple scoring
    score = 0

    if q1 == "No data":
        score += 0
    elif q1 == "Personal data":
        score += 2
    elif q1 == "Special category / highly sensitive data":
        score += 4

    if q2 == "Small (few records, low volume)":
        score += 1
    elif q2 == "Medium":
        score += 2
    elif q2 == "Large (high volume / continuous)":
        score += 3

    if q3 == "Yes":
        score += 2
    elif q3 == "No":
        score += 0

    # Map score to risk level
    if score <= 2:
        level = "LOW"
        explanation = (
            "The vendor has limited exposure to personal or sensitive data and does not "
            "present significant integration risk. Standard due diligence and basic "
            "controls should be sufficient."
        )
    elif 3 <= score <= 5:
        level = "MEDIUM"
        explanation = (
            "The vendor processes personal data or has moderate integration with your "
            "environment. A more detailed security and privacy review is appropriate, and "
            "contractual controls should be clearly defined."
        )
    elif 6 <= score <= 7:
        level = "HIGH"
        explanation = (
            "The vendor processes a meaningful volume of personal or sensitive data and/or "
            "connects to core systems. Enhanced due diligence, stronger controls, and "
            "ongoing monitoring are recommended."
        )
    else:
        level = "CRITICAL"
        explanation = (
            "The vendor processes highly sensitive or special category data at scale and/or "
            "is tightly integrated with critical systems. Treat this as a critical vendor: "
            "require comprehensive assessment, senior sign-off, and continuous monitoring."
        )

    decision = f"RISK TIER: {level}"
    return decision, explanation, path


# ----------------------------
# TREE 3: DPIA (DATA PROTECTION IMPACT ASSESSMENT) REQUIREMENT
# ----------------------------
def tree_dpia():
    st.subheader("Tree 3 – DPIA Requirement Check")

    path = []

    q1 = st.radio(
        "1. Does the processing involve systematic and extensive profiling or automated decisions about individuals?",
        ["Select...", "Yes", "No"],
        index=0,
        key="dp_q1",
    )
    path.append(f"Q1 → {q1}")

    if q1 == "Select...":
        return None, None, path

    q2 = st.radio(
        "2. Will the processing involve large-scale use of special category data "
        "(for example health, biometrics, ethnicity)?",
        ["Select...", "Yes", "No"],
        index=0,
        key="dp_q2",
    )
    path.append(f"Q2 → {q2}")

    if q2 == "Select...":
        return None, None, path

    q3 = st.radio(
        "3. Will the processing involve systematic monitoring of publicly accessible areas "
        "or behaviour (for example CCTV, online tracking)?",
        ["Select...", "Yes", "No"],
        index=0,
        key="dp_q3",
    )
    path.append(f"Q3 → {q3}")

    if q3 == "Select...":
        return None, None, path

    yes_count = sum(1 for ans in [q1, q2, q3] if ans == "Yes")

    if yes_count == 0:
        decision = "DPIA NOT REQUIRED (LIKELY)"
        explanation = (
            "None of the high-risk indicators are triggered. A full DPIA is unlikely to be "
            "mandatory, but you should document this assessment and keep it under review "
            "if the scope changes."
        )
    elif yes_count == 1:
        decision = "DPIA RECOMMENDED"
        explanation = (
            "At least one high-risk characteristic is present. A DPIA may not be strictly "
            "mandatory in all jurisdictions, but completing one is recommended to document "
            "risk analysis and controls."
        )
    else:
        decision = "DPIA REQUIRED"
        explanation = (
            "Multiple high-risk characteristics are present. A DPIA should be treated as "
            "mandatory to assess and document privacy risks and mitigating controls before "
            "proceeding."
        )

    return decision, explanation, path


# ----------------------------
# MAIN APP: TREE SELECTION
# ----------------------------

tree_choice = st.selectbox(
    "Select a decision guide to run:",
    ["Select...", "Incident Reporting", "Vendor Risk Tiering", "DPIA Requirement"],
)

decision = None
explanation = None
path = []

if tree_choice == "Incident Reporting":
    decision, explanation, path = tree_incident_reporting()
elif tree_choice == "Vendor Risk Tiering":
    decision, explanation, path = tree_vendor_classification()
elif tree_choice == "DPIA Requirement":
    decision, explanation, path = tree_dpia()

st.markdown("---")

if decision:
    st.subheader("Decision")
    st.write(decision)

if explanation:
    st.subheader("Explanation")
    st.write(explanation)
if path and st.checkbox("Show decision path"):
    st.subheader("Path taken")
    for step in path:
        st.write("•", step)
