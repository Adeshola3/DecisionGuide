import json
from pathlib import Path

import streamlit as st


st.set_page_config(page_title="DecisionGuide", layout="centered")


LOGIC_DIR = Path(__file__).parent / "logic"


def load_trees():
    trees = {}
    for path in LOGIC_DIR.glob("*.json"):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            tree_id = data.get("id") or path.stem
            trees[tree_id] = data
        except Exception as e:
            # In production you might log this instead
            print(f"Failed to load {path}: {e}")
    return trees


def traverse_tree(tree, node_id, path_prefix=""):
    """
    Recursively walk a decision tree defined in JSON.
    Returns (decision_code, explanation, path_taken)
    """
    nodes = tree["nodes"]
    node = nodes[node_id]

    node_label = node.get("text", "")
    if path_prefix:
        display_label = f"{path_prefix} → {node_label}"
    else:
        display_label = node_label

    node_type = node.get("type", "choice")

    if node_type == "choice":
        options = list(node["options"].keys())
        choice = st.radio(display_label, options, key=f"{tree['id']}_{node_id}")
        st.write("")  # small spacing

        selected_branch = node["options"][choice]
        path_entry = f"{node_label} → {choice}"

        # If this branch leads directly to a decision
        if "decision" in selected_branch:
            decision = selected_branch["decision"]
            explanation = selected_branch.get("explanation", "")
            return decision, explanation, [path_entry]

        # Otherwise, go to next node
        next_node = selected_branch["next"]
        decision, explanation, sub_path = traverse_tree(tree, next_node, path_prefix="")
        return decision, explanation, [path_entry] + sub_path

    elif node_type == "text":
        st.markdown(display_label)
        return None, None, [node_label]

    else:
        st.warning(f"Unknown node type: {node_type}")
        return None, None, []


def render_jurisdiction_section():
    st.markdown("### Jurisdiction-specific pointers")

    region = st.selectbox(
        "Which jurisdiction are you mainly working under?",
        [
            "Select...",
            "UK / ICO (UK GDPR / DPA 2018)",
            "EU / EDPB (EU GDPR)",
            "US (e.g. HIPAA / State privacy laws)",
            "Nigeria (NDPR)",
            "Other / Mixed",
        ],
        index=0,
        key="dpia_jurisdiction",
    )

    if region == "Select...":
        return

    if region.startswith("UK"):
        st.markdown(
            "- Check UK GDPR Article 35 and ICO guidance on when a DPIA is mandatory.\n"
            "- If CCTV, large-scale monitoring, or profiling is involved, verify against ICO's DPIA checklists.\n"
            "- Ensure documentation follows ICO's recommended DPIA template."
        )
    elif region.startswith("EU"):
        st.markdown(
            "- Refer to EU GDPR Article 35 and EDPB guidelines on DPIAs.\n"
            "- Check your processing activity against your supervisory authority's DPIA 'blacklist' and 'whitelist'.\n"
            "- Ensure you can demonstrate consultation with the DPO where required."
        )
    elif region.startswith("US"):
        st.markdown(
            "- While the term 'DPIA' is EU/UK-driven, similar assessments exist under HIPAA risk analysis and state privacy laws.\n"
            "- Map your DPIA-style assessment to HIPAA Security Rule risk analysis requirements where health data is involved.\n"
            "- Consider state-level requirements (for example CPRA) for high-risk processing and impact assessments."
        )
    elif region.startswith("Nigeria"):
        st.markdown(
            "- Map your assessment against NDPR requirements for high-risk data processing.\n"
            "- Check NITDA guidance and any sector-specific rules for impact assessment expectations.\n"
            "- Ensure cross-border transfer risks are addressed explicitly."
        )
    else:
        st.markdown(
            "- Align your DPIA with any local data protection law or sector regulation.\n"
            "- Where no formal DPIA requirement exists, treat this as a structured privacy and risk assessment.\n"
            "- Document assumptions, risks, and mitigations so they can stand up to regulatory or customer scrutiny."
        )


def main():
    st.title("DecisionGuide")
    st.caption("One smart decision at a time.")

    trees = load_trees()
    if not trees:
        st.error("No decision trees found in the logic/ folder.")
        return

    # Sidebar: tree selection
    tree_options = {
        data.get("title", tree_id): tree_id for tree_id, data in trees.items()
    }
    selected_label = st.sidebar.selectbox(
        "Select a decision guide", list(tree_options.keys())
    )
    selected_tree_id = tree_options[selected_label]
    tree = trees[selected_tree_id]

    st.header(tree.get("title", "Decision Tree"))
    if tree.get("description"):
        st.markdown(tree["description"])

    st.markdown("---")
    st.markdown("### Answer the questions")

    with st.form(key=f"form_{selected_tree_id}"):
        decision, explanation, path = traverse_tree(tree, tree["root"])
        submitted = st.form_submit_button("Run assessment")

    if submitted:
        if decision is None:
            st.warning("No decision reached. Please ensure all questions are answered.")
            return

        st.markdown("### Result")
        st.write(f"**Decision code:** {decision}")
        if explanation:
            st.write(explanation)

        st.markdown("### Path taken")
        for step in path:
            st.write(f"- {step}")

        # If this is the DPIA tree, show jurisdiction guidance after result
        if selected_tree_id.startswith("dpia"):
            render_jurisdiction_section()


if __name__ == "__main__":
    main()