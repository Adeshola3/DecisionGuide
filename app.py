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

    # Initialize session state for this tree
    state_key = f"result_{selected_tree_id}"
    if state_key not in st.session_state:
        st.session_state[state_key] = None

    with st.form(key=f"form_{selected_tree_id}"):
        decision, explanation, path = traverse_tree(tree, tree["root"])
        submitted = st.form_submit_button("Run assessment")

    if submitted:
        if decision is None:
            st.warning("No decision reached. Please ensure all questions are answered.")
            return
        
        # Store result in session state
        st.session_state[state_key] = {
            "decision": decision,
            "explanation": explanation,
            "path": path
        }

    # Display result if it exists in session state
    if st.session_state[state_key] is not None:
        result = st.session_state[state_key]
        
        st.markdown("### Result")
        st.write(f"**Decision code:** {result['decision']}")
        if result['explanation']:
            st.write(result['explanation'])

        st.markdown("### Path taken")
        for step in result['path']:
            st.write(f"- {step}")

        # If this is the DPIA tree, show jurisdiction guidance after result
        if selected_tree_id.startswith("dpia"):
            render_jurisdiction_section()
