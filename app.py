import json
from pathlib import Path

import streamlit as st

from utils.export import export_to_pdf, export_to_json, export_to_text, get_filename


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
            print(f"Failed to load {path}: {e}")
    return trees


def count_max_depth(tree, node_id, visited=None):
    """
    Count maximum depth (number of questions) from current node to any outcome.
    """
    if visited is None:
        visited = set()
    
    if node_id in visited:
        return 0
    
    visited.add(node_id)
    nodes = tree.get("nodes", {})
    
    if node_id not in nodes:
        return 0
    
    node = nodes[node_id]
    node_type = node.get("type", "choice")
    
    if node_type != "choice":
        return 0
    
    # This is a question, count it
    max_depth = 0
    
    # Check all possible branches
    for option_key, option_data in node.get("options", {}).items():
        if "next" in option_data:
            # This leads to another question
            branch_depth = count_max_depth(tree, option_data["next"], visited.copy())
            max_depth = max(max_depth, branch_depth)
        # else: this leads directly to an outcome (terminal node)
    
    return 1 + max_depth


def traverse_tree_interactive(tree, node_id, answers, path_so_far):
    """
    Interactively traverse the tree.
    Shows one question at a time with progress indicator.
    Returns (decision_code, explanation, full_path) when complete, or (None, None, path) if still in progress.
    """
    nodes = tree["nodes"]
    node = nodes[node_id]
    
    node_label = node.get("text", "")
    node_type = node.get("type", "choice")
    
    if node_type == "choice":
        # Calculate progress
        current_question = len(answers) + 1
        # Estimate remaining questions from current position
        remaining = count_max_depth(tree, node_id)
        estimated_total = current_question + remaining - 1  # -1 because current is counted in remaining
        
        # Show progress (ALWAYS, no conditions)
        if estimated_total >= current_question:
            progress_percentage = (current_question / estimated_total) * 100
        else:
            progress_percentage = 100
        
        # Progress display
        st.info(f"📊 Question {current_question} of ~{estimated_total}")
        st.progress(min(progress_percentage / 100, 1.0))
        st.caption(f"{int(min(progress_percentage, 100))}% complete")
        st.markdown("---")
        
        options = list(node["options"].keys())
        
        # Check if this question was already answered
        if node_id in answers:
            selected = answers[node_id]
        else:
            # Show the question
            selected = st.radio(
                node_label, 
                options, 
                key=f"{tree['id']}_{node_id}",
                index=None  # No default selection
            )
            
            if selected is None:
                # User hasn't answered yet, stop here
                return None, None, path_so_far
            
            # Save the answer
            answers[node_id] = selected
        
        # Add to path
        path_entry = f"{node_label} → {selected}"
        new_path = path_so_far + [path_entry]
        
        selected_branch = node["options"][selected]
        
        # Check if this leads to a decision
        if "decision" in selected_branch:
            decision = selected_branch["decision"]
            explanation = selected_branch.get("explanation", "")
            return decision, explanation, new_path
        
        # Otherwise, continue to next node
        next_node = selected_branch["next"]
        return traverse_tree_interactive(tree, next_node, answers, new_path)
    
    elif node_type == "text":
        st.markdown(node_label)
        return None, None, path_so_far + [node_label]
    
    else:
        st.warning(f"Unknown node type: {node_type}")
        return None, None, path_so_far


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

    # Initialize session state for this tree
    answers_key = f"answers_{selected_tree_id}"
    result_key = f"result_{selected_tree_id}"
    
    if answers_key not in st.session_state:
        st.session_state[answers_key] = {}
    
    if result_key not in st.session_state:
        st.session_state[result_key] = None

    # Traverse the tree
    answers = st.session_state[answers_key]
    decision, explanation, path = traverse_tree_interactive(
        tree, 
        tree["root"], 
        answers, 
        []
    )

    # If we have a decision, show it
    if decision is not None:
        st.session_state[result_key] = {
            "decision": decision,
            "explanation": explanation,
            "path": path
        }

    # Display result if available
    if st.session_state[result_key] is not None:
        # Show 100% completion
        st.success("✅ Assessment Complete!")
        st.progress(1.0)
        
        st.markdown("---")
        
        result = st.session_state[result_key]
        
        st.markdown("### Result")
        st.write(f"**Decision code:** {result['decision']}")
        if result['explanation']:
            st.write(result['explanation'])

        st.markdown("### Path taken")
        for step in result['path']:
            st.write(f"- {step}")
        
        # Export options
        st.markdown("---")
        st.markdown("### Export Options")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # PDF Export
            pdf_buffer = export_to_pdf(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📄 Download PDF",
                data=pdf_buffer,
                file_name=get_filename(tree.get("title", "Assessment"), "pdf"),
                mime="application/pdf"
            )
        
        with col2:
            # JSON Export
            json_data = export_to_json(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📋 Download JSON",
                data=json_data,
                file_name=get_filename(tree.get("title", "Assessment"), "json"),
                mime="application/json"
            )
        
        with col3:
            # Text Export
            text_data = export_to_text(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📝 Download TXT",
                data=text_data,
                file_name=get_filename(tree.get("title", "Assessment"), "txt"),
                mime="text/plain"
            )
        
        with col4:
            # Reset button
            if st.button("🔄 Start over"):
                st.session_state[answers_key] = {}
                st.session_state[result_key] = None
                st.rerun()


if __name__ == "__main__":
    main()