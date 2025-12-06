"""
Main Streamlit application for DecisionGuide.

This module provides the web interface for DecisionGuide, including:
- Landing page with assessment selection
- Interactive decision tree traversal
- Progress indicators
- Risk scoring integration
- History tracking
- Export functionality
"""
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

import streamlit as st

from utils.export import (
    export_to_pdf, export_to_json, export_to_text, export_to_csv,
    export_history_to_csv, get_filename
)
from utils.validation import (
    validate_json_file, count_tree_nodes, count_answered_questions
)
from utils.history import add_to_history, get_recent_history
from utils.config import Config
from utils.security import sanitize_input, validate_circular_reference
from utils.analytics import get_statistics, search_history, filter_history
from risk_scoring import RiskScorer, display_final_risk_report


st.set_page_config(
    page_title="DecisionGuide",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Simple, clean CSS design
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: #1e1e1e;
        color: #e0e0e0;
    }
    
    .stMarkdown, .stMarkdown p {
        color: #d0d0d0 !important;
        line-height: 1.6;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .assessment-card {
        background: #2a2a2a;
        border: 1px solid #3a3a3a;
        border-radius: 8px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        transition: border-color 0.2s;
    }
    
    .assessment-card:hover {
        border-color: #5a5a5a;
    }
    
    .question-card {
        background: #2a2a2a;
        border: 1px solid #3a3a3a;
        border-radius: 8px;
        padding: 2rem;
        margin-bottom: 1.5rem;
    }
    
    .question-number {
        display: inline-block;
        background: #3a3a3a;
        color: #ffffff;
        padding: 0.4rem 1rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .result-card {
        background: #2a2a2a;
        border: 1px solid #3a3a3a;
        border-radius: 8px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .result-badge {
        display: inline-block;
        background: #3a3a3a;
        color: #ffffff;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .path-step {
        background: #2a2a2a;
        border-left: 3px solid #5a5a5a;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 0 4px 4px 0;
        color: #d0d0d0;
    }
    
    .stButton>button {
        background: #3a3a3a !important;
        color: #ffffff !important;
        border: 1px solid #4a4a4a !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 4px !important;
        transition: background 0.2s !important;
    }
    
    .stButton>button:hover {
        background: #4a4a4a !important;
    }
    
    .stDownloadButton>button {
        background: #2a2a2a !important;
        color: #ffffff !important;
        border: 1px solid #3a3a3a !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 4px !important;
    }
    
    .stDownloadButton>button:hover {
        background: #3a3a3a !important;
    }
    
    .stRadio > div > label {
        background: #2a2a2a !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 4px !important;
        padding: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stRadio > div > label:hover {
        background: #3a3a3a !important;
        border-color: #4a4a4a !important;
    }
</style>
""", unsafe_allow_html=True)


LOGIC_DIR = Path(__file__).parent / "logic"


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_trees() -> Dict[str, Dict[str, Any]]:
    """
    Load and validate all decision tree JSON files with caching.
    
    Returns:
        Dictionary mapping tree IDs to tree data
    """
    trees = {}
    for path in LOGIC_DIR.glob("*.json"):
        is_valid, error, data = validate_json_file(path)
        if is_valid and data:
            # Validate circular references
            is_circular_valid, circular_error = validate_circular_reference(data)
            if not is_circular_valid:
                st.error(f"Circular reference in {path.name}: {circular_error}")
                continue
            
            tree_id = data.get("id") or path.stem
            trees[tree_id] = data
        else:
            st.error(f"Failed to load {path.name}: {error}")
    return trees


def calculate_progress(tree: Dict[str, Any], answers: Dict[str, Any]) -> Tuple[int, int, float]:
    """
    Calculate progress through the assessment.
    
    Args:
        tree: Decision tree data
        answers: Current answers
        
    Returns:
        Tuple of (current_step, total_steps, progress_percentage)
    """
    total_questions = len([n for n in tree.get("nodes", {}).values() if n.get("type") == "choice"])
    answered = count_answered_questions(answers)
    
    if total_questions == 0:
        return 0, 0, 0.0
    
    progress = (answered / total_questions) * 100
    return answered, total_questions, progress


def show_landing_page():
    """
    Display the landing page with assessment selection.
    """
    trees = load_trees()
    
    st.markdown("<div style='max-width: 1200px; margin: 0 auto; padding: 2rem;'>", unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div style='text-align: center; margin-bottom: 4rem;'>
        <h1 style='font-size: 3rem; margin-bottom: 1rem;'>DecisionGuide</h1>
        <p style='font-size: 1.2rem; color: #b0b0b0;'>
            A simple, logic-based assistant for governance and audit decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Select a decision guide to run:")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Assessment cards
    if trees:
        cols = st.columns(3)
        for idx, (tree_id, tree_data) in enumerate(trees.items()):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class='assessment-card'>
                    <h3 style='font-size: 1.5rem; margin-bottom: 0.5rem;'>{tree_data.get('title', 'Assessment')}</h3>
                    <p style='color: #b0b0b0; margin-bottom: 1.5rem;'>{tree_data.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Start Assessment", key=f"start_{tree_id}", use_container_width=True):
                    st.session_state.selected_tree = tree_id
                    st.session_state.show_landing = False
                    st.rerun()
    else:
        st.warning("No assessment trees found. Please add JSON files to the logic/ directory.")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0; border-top: 1px solid #3a3a3a; margin-top: 4rem;'>
        <p style='color: #808080; font-size: 0.9rem;'>
            <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank' style='color: #a0a0a0; text-decoration: none;'>Star on GitHub</a>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <a href='https://github.com/Adeshola3/DecisionGuide/issues' target='_blank' style='color: #a0a0a0; text-decoration: none;'>Contribute</a>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <a href='https://github.com/Adeshola3/DecisionGuide#readme' target='_blank' style='color: #a0a0a0; text-decoration: none;'>Documentation</a>
        </p>
        <p style='color: #606060; font-size: 0.85rem; margin-top: 1rem;'>
            Open source • MIT License • Made by Adeshola
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def show_assessment_page():
    """
    Assessment page with progress indicators and risk scoring.
    """
    trees = load_trees()
    
    st.markdown("<div class='assessment-page-wrapper'>", unsafe_allow_html=True)
    
    # Enhanced Sidebar with history, search, and analytics
    with st.sidebar:
        tab1, tab2, tab3 = st.tabs(["History", "Search", "Analytics"])
        
        with tab1:
            st.subheader("Assessment History")
            history = get_recent_history(limit=50)

            if history:
                # Enhanced filters with date range
                tree_ids = sorted({h.get("tree_id") for h in history if h.get("tree_id")})
                decisions = sorted({h.get("decision") for h in history if h.get("decision")})
                
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    selected_tree = st.selectbox(
                        "Filter by tree",
                        options=["(All)"] + tree_ids,
                        index=0,
                        key="history_filter_tree"
                    )
                with col_f2:
                    selected_decision = st.selectbox(
                        "Filter by decision",
                        options=["(All)"] + decisions,
                        index=0,
                        key="history_filter_decision"
                    )
                
                # Date range filter
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    date_from = st.date_input("From date", value=None, key="history_date_from")
                with col_d2:
                    date_to = st.date_input("To date", value=None, key="history_date_to")

                filtered_history = []
                for entry in history:
                    # Tree filter
                    if selected_tree != "(All)" and entry.get("tree_id") != selected_tree:
                        continue
                    # Decision filter
                    if selected_decision != "(All)" and entry.get("decision") != selected_decision:
                        continue
                    # Date range filter
                    try:
                        entry_date = datetime.fromisoformat(entry.get("timestamp", "")).date()
                        if date_from and entry_date < date_from:
                            continue
                        if date_to and entry_date > date_to:
                            continue
                    except (ValueError, AttributeError):
                        pass
                    filtered_history.append(entry)

                # Table view
                table_rows = [
                    {
                        "Date": e.get("timestamp", "")[:10],
                        "Tree": e.get("tree_title", ""),
                        "Decision": e.get("decision", ""),
                        "Path steps": len(e.get("path", [])),
                    }
                    for e in filtered_history
                ]
                st.dataframe(table_rows, use_container_width=True, hide_index=True)

                # CSV export
                if Config.ENABLE_CSV_EXPORT and filtered_history:
                    csv_data = export_history_to_csv(filtered_history)
                    st.download_button(
                        label="Download history as CSV",
                        data=csv_data,
                        file_name=f"DecisionGuide_History_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )

                # Expanders for details
                for entry in filtered_history[:10]:
                    with st.expander(f"{entry['tree_title']} - {entry['decision'][:40]}"):
                        st.write(f"**Date:** {entry['timestamp'][:19]}")
                        st.write(f"**Decision:** {entry['decision']}")
                        st.write(f"**Path steps:** {len(entry.get('path', []))}")
            else:
                st.caption("No history yet")

            if st.button("Clear history"):
                from utils.history import clear_history
                clear_history()
                st.rerun()
        
        with tab2:
            st.subheader("Search history")
            search_query = st.text_input("Search by tree, decision, or explanation", key="history_search")
            if search_query:
                results = search_history(search_query, limit=10)
                if results:
                    rows = [
                        {
                            "Date": e.get("timestamp", "")[:19],
                            "Tree": e.get("tree_title", ""),
                            "Decision": e.get("decision", ""),
                        }
                        for e in results
                    ]
                    st.dataframe(rows, use_container_width=True, hide_index=True)
                else:
                    st.info("No results found")
        
        with tab3:
            if Config.ENABLE_ANALYTICS:
                st.subheader("Analytics Dashboard")
                stats = get_statistics()
                if stats.get("total_assessments", 0) > 0:
                    # Key metrics in columns
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Assessments", stats["total_assessments"])
                    with col2:
                        st.metric("Recent Activity (7 days)", stats.get("recent_activity_count", 0))
                    with col3:
                        most_used = stats.get("most_used_tree", "N/A")
                        st.metric("Most Used Tree", most_used[:20] + "..." if len(str(most_used)) > 20 else most_used)
                    
                    st.markdown("---")
                    
                    # Tree usage chart
                    if stats.get("tree_usage"):
                        st.subheader("Tree Usage")
                        tree_usage_data = dict(list(stats["tree_usage"].items())[:10])
                        st.bar_chart(tree_usage_data)
                    
                    # Decision distribution
                    if stats.get("decision_distribution"):
                        st.subheader("Decision Distribution")
                        decision_data = dict(list(stats["decision_distribution"].items())[:10])
                        st.bar_chart(decision_data)
                    
                    # Daily activity
                    if stats.get("daily_activity"):
                        st.subheader("Daily Activity")
                        daily_data = stats["daily_activity"]
                        st.line_chart(daily_data)
                else:
                    st.info("No statistics available yet. Complete some assessments to see analytics.")
    
    # Back button - clear all assessment state when going back
    if st.button("Back to Home", key="back_btn"):
        selected_tree_id = st.session_state.get('selected_tree')
        if selected_tree_id:
            # Clear all state for this assessment
            st.session_state.pop(f"answers_{selected_tree_id}", None)
            st.session_state.pop(f"result_{selected_tree_id}", None)
            st.session_state.pop(f"path_{selected_tree_id}", None)
            st.session_state.pop(f"node_history_{selected_tree_id}", None)
        st.session_state.show_landing = True
        st.session_state.pop('selected_tree', None)
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    selected_tree_id = st.session_state.get('selected_tree')
    
    if not selected_tree_id or selected_tree_id not in trees:
        st.error("Assessment not found")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    tree = trees[selected_tree_id]
    
    # Assessment header
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>{tree.get('title', 'Assessment')}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if tree.get("description"):
        st.info(f"{tree['description']}")
    
    st.markdown("<br>", unsafe_allow_html=True)

    answers_key = f"answers_{selected_tree_id}"
    result_key = f"result_{selected_tree_id}"
    path_key = f"path_{selected_tree_id}"
    node_history_key = f"node_history_{selected_tree_id}"
    
    if answers_key not in st.session_state:
        st.session_state[answers_key] = {}
    if result_key not in st.session_state:
        st.session_state[result_key] = None
    if path_key not in st.session_state:
        st.session_state[path_key] = []
    if node_history_key not in st.session_state:
        st.session_state[node_history_key] = []

    answers = st.session_state[answers_key]
    node_history = st.session_state[node_history_key]

    # Clickable breadcrumb navigation (jump back to earlier step)
    if node_history:
        nodes = tree.get("nodes", {})

        def _short_label_for_id(n_id: str) -> str:
            """Get short label for breadcrumb, preferring 'label' field over 'text'."""
            node_data = nodes.get(n_id, {})
            # Prefer 'label' field if available (shorter), otherwise use 'text'
            raw = node_data.get("label") or node_data.get("text") or n_id
            text = sanitize_input(str(raw))
            # If using 'text' field, make it shorter; if 'label', keep as is (assumed short)
            if node_data.get("label"):
                return text[:30]  # Label field, keep short
            else:
                return (text[:25] + "...") if len(text) > 25 else text  # Text field, truncate more

        labels = [
            f"{idx + 1}. {_short_label_for_id(n_id)}"
            for idx, n_id in enumerate(node_history)
        ]

        selected_index = st.selectbox(
            "Breadcrumb",
            options=list(range(len(labels))),
            format_func=lambda i: labels[i],
            index=len(labels) - 1,
            key=f"breadcrumb_{selected_tree_id}",
        )

        # If user picked an earlier step, trim answers and history and clear completion
        if selected_index < len(node_history) - 1:
            keep_ids = set(node_history[: selected_index + 1])
            for nid in list(answers.keys()):
                if nid not in keep_ids:
                    del answers[nid]
            st.session_state[node_history_key] = node_history[: selected_index + 1]
            st.session_state[result_key] = None
            st.session_state[path_key] = []
            st.rerun()

    # Back navigation button (if enabled and we have history)
    if Config.ENABLE_BACK_NAVIGATION and node_history:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Back", key="back_question"):
                # Remove last answer and node from history
                if node_history:
                    last_node = node_history.pop()
                    if last_node in answers:
                        del answers[last_node]
                # Clear completion state as well when stepping back
                st.session_state[result_key] = None
                st.session_state[path_key] = []
                st.rerun()

    decision, explanation, path = traverse_tree_interactive(
        tree, 
        tree["root"], 
        answers, 
        [],
        node_history
    )
    
    st.session_state[path_key] = path

    # Progress indicator (recomputed so it reflects latest state)
    current_step, total_steps, progress = calculate_progress(tree, answers)
    
    # If decision is reached, show 100% progress
    if decision is not None:
        if total_steps > 0:
            progress = 100.0
            current_step = total_steps
        else:
            # If no questions but decision reached, still show complete
            progress = 100.0
            current_step = 1
            total_steps = 1

    if total_steps > 0:
        st.progress(
            progress / 100.0,
            text=f"Progress: Step {current_step} of {total_steps} ({int(progress)}%)",
        )

    if decision is not None:
        st.session_state[result_key] = {
            "decision": decision,
            "explanation": explanation,
            "path": path
        }
        
        # Save to history
        add_to_history(
            selected_tree_id,
            tree.get("title", "Assessment"),
            decision,
            explanation or "",
            path,
            answers
        )

    if st.session_state[result_key] is not None:
        st.success("Assessment Complete!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        result = st.session_state[result_key]
        
        # Optional detailed risk report (separate from summary below)
        if "scoring" in tree and Config.ENABLE_RISK_SCORING:
            try:
                scorer = RiskScorer(tree)
                risk_answers = [
                    {"node_id": k, "choice": v}
                    for k, v in answers.items()
                    if v is not None
                ]
                if risk_answers:
                    display_final_risk_report(scorer, risk_answers)
                    st.markdown("<br>", unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Risk scoring unavailable: {e}")

        # Get risk score if available (for summary + exports)
        risk_score_data = None
        if "scoring" in tree and Config.ENABLE_RISK_SCORING:
            try:
                scorer = RiskScorer(tree)
                risk_answers = [
                    {"node_id": k, "choice": v}
                    for k, v in answers.items()
                    if v is not None
                ]
                if risk_answers:
                    score = scorer.calculate_score(risk_answers)
                    risk_details = scorer.get_risk_details(score)
                    risk_score_data = {
                        "score": score,
                        "level": risk_details["level"],
                    }
            except Exception:
                risk_score_data = None

        # Result Display with Risk Score
        risk_score_html = ""
        if risk_score_data:
            risk_level_color = {
                "Low": "#4caf50",
                "Medium": "#ff9800", 
                "High": "#f44336",
                "Critical": "#d32f2f"
            }.get(risk_score_data['level'], "#ffffff")
            risk_score_html = f"""
            <div style='background: #2a2a2a; border-left: 4px solid {risk_level_color}; padding: 1rem; margin-bottom: 1.5rem; border-radius: 4px;'>
                <strong style='color: #ffffff;'>Risk Score:</strong> 
                <span style='color: {risk_level_color}; font-size: 1.2rem; font-weight: bold;'>{risk_score_data['score']}/100</span>
                <span style='color: #b0b0b0; margin-left: 1rem;'>({risk_score_data['level']} Risk)</span>
            </div>
            """
        
        st.markdown(f"""
        <div class='result-card'>
            <span class='result-badge'>Final Decision</span>
            {risk_score_html}
            <h3 style='font-size: 1.5rem; margin-bottom: 1rem; color: #ffffff;'>{result['decision']}</h3>
            {f"<p style='color: #b0b0b0; font-size: 1rem; line-height: 1.6;'>{result['explanation']}</p>" if result['explanation'] else ""}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Decision Path")
        st.markdown("<div style='background: #2a2a2a; padding: 1.5rem; border-radius: 8px; border: 1px solid #3a3a3a;'>", unsafe_allow_html=True)
        for i, step in enumerate(result['path'], 1):
            st.markdown(f"<div class='path-step'><strong>{i}.</strong> {step}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### Export Your Results")
        
        # Get risk score if available
        risk_score_data = None
        if "scoring" in tree and Config.ENABLE_RISK_SCORING:
            try:
                scorer = RiskScorer(tree)
                risk_answers = [
                    {"node_id": k, "choice": v} 
                    for k, v in answers.items() 
                    if v is not None
                ]
                if risk_answers:
                    score = scorer.calculate_score(risk_answers)
                    risk_details = scorer.get_risk_details(score)
                    risk_score_data = {
                        "score": score,
                        "level": risk_details["level"]
                    }
            except Exception:
                pass
        
        num_cols = 5 if Config.ENABLE_CSV_EXPORT else 4
        cols = st.columns(num_cols)
        
        with cols[0]:
            pdf_buffer = export_to_pdf(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path'],
                risk_score=risk_score_data if Config.INCLUDE_RISK_SCORES else None
            )
            st.download_button(
                label="PDF Report",
                data=pdf_buffer,
                file_name=get_filename(tree.get("title", "Assessment"), "pdf"),
                mime="application/pdf",
                use_container_width=True
            )
        
        with cols[1]:
            json_data = export_to_json(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="JSON Data",
                data=json_data,
                file_name=get_filename(tree.get("title", "Assessment"), "json"),
                mime="application/json",
                use_container_width=True
            )
        
        with cols[2]:
            text_data = export_to_text(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="Text File",
                data=text_data,
                file_name=get_filename(tree.get("title", "Assessment"), "txt"),
                mime="text/plain",
                use_container_width=True
            )
        
        if Config.ENABLE_CSV_EXPORT and len(cols) > 3:
            with cols[3]:
                csv_data = export_to_csv(
                    tree.get("title", "Assessment"),
                    result['decision'],
                    result['explanation'],
                    result['path'],
                    risk_score=risk_score_data
                )
                st.download_button(
                    label="CSV Data",
                    data=csv_data,
                    file_name=get_filename(tree.get("title", "Assessment"), "csv"),
                    mime="text/csv",
                    use_container_width=True
                )
        
        with cols[-1]:
            if st.button("New Assessment", use_container_width=True):
                st.session_state[answers_key] = {}
                st.session_state[result_key] = None
                st.session_state[path_key] = []
                st.session_state[node_history_key] = []
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)


def traverse_tree_interactive(
    tree: Dict[str, Any], 
    node_id: str, 
    answers: Dict[str, Any], 
    path_so_far: List[str],
    node_history: List[str]
) -> Tuple[Optional[str], Optional[str], List[str]]:
    """
    Interactively traverse the decision tree with back navigation support.
    
    Args:
        tree: Decision tree data
        node_id: Current node ID
        answers: Dictionary to store answers
        path_so_far: List of path steps taken so far
        node_history: List of visited node IDs for back navigation
        
    Returns:
        Tuple of (decision, explanation, path) or (None, None, path) if incomplete
    """
    try:
        nodes = tree.get("nodes", {})

        def _short_label(n_id: str) -> str:
            """Helper to derive a concise label for breadcrumbs and path entries."""
            node_data = nodes.get(n_id, {})
            raw = node_data.get("label") or node_data.get("text") or n_id
            text = sanitize_input(str(raw))
            return (text[:40] + "...") if len(text) > 40 else text
        if node_id not in nodes:
            st.error(f"Node '{node_id}' not found in tree")
            return None, None, path_so_far
        
        node = nodes[node_id]
        node_label = sanitize_input(node.get("text", ""))
        node_type = node.get("type", "choice")
        
        if node_type == "choice":
            current_question = count_answered_questions(answers) + 1

            # Breadcrumb navigation (short labels, last few steps only)
            if node_history:
                breadcrumb = " > ".join([_short_label(n) for n in node_history[-3:]])
                st.caption(f"{breadcrumb} > {_short_label(node_id)}")
            
            st.markdown(f"""
            <div class='question-card'>
                <span class='question-number'>Question {current_question}</span>
                <h3 style='font-size: 1.3rem; color: #ffffff; margin-bottom: 1rem;'>{node_label}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            options = list(node.get("options", {}).keys())
            
            if not options:
                st.error(f"No options available for node '{node_id}'")
                return None, None, path_so_far
            
            if node_id in answers:
                selected = answers[node_id]
            else:
                selected = st.radio(
                    "Choose your answer:",
                    options, 
                    key=f"{tree['id']}_{node_id}",
                    index=None,
                    label_visibility="collapsed"
                )
                
                if selected is None:
                    return None, None, path_so_far
                
                # Sanitize input
                selected = sanitize_input(selected)
                answers[node_id] = selected
                
                # Add to node history for back navigation
                if node_id not in node_history:
                    node_history.append(node_id)
            
            path_entry = f"{_short_label(node_id)} > {selected}"
            new_path = path_so_far + [path_entry]
            
            selected_branch = node["options"].get(selected)
            if not selected_branch:
                st.error(f"Invalid option selected: {selected}")
                return None, None, new_path
            
            if "decision" in selected_branch:
                decision = selected_branch["decision"]
                explanation = selected_branch.get("explanation", "")
                return decision, explanation, new_path
            
            if "next" not in selected_branch:
                st.error(f"No 'next' or 'decision' in option '{selected}'")
                return None, None, new_path
            
            next_node = selected_branch["next"]
            return traverse_tree_interactive(tree, next_node, answers, new_path, node_history)
        
        elif node_type == "text":
            st.markdown(f"<p style='color: #d0d0d0;'>{node_label}</p>", unsafe_allow_html=True)
            return None, None, path_so_far + [node_label]
        
        else:
            st.warning(f"Unknown node type: {node_type}")
            return None, None, path_so_far
    
    except Exception as e:
        st.error(f"Error traversing tree: {str(e)}")
        return None, None, path_so_far


def main() -> None:
    """
    Main application entry point with session management.
    """
    # Initialize session state
    if 'show_landing' not in st.session_state:
        st.session_state.show_landing = True
    
    if 'session_start' not in st.session_state:
        st.session_state.session_start = datetime.now()
    
    # Check session timeout
    from utils.security import check_session_timeout
    
    if not check_session_timeout(st.session_state.session_start, Config.SESSION_TIMEOUT):
        st.warning("Your session has expired. Please refresh the page.")
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.show_landing = True
        st.session_state.session_start = datetime.now()
        st.rerun()
    
    if st.session_state.show_landing:
        show_landing_page()
    else:
        show_assessment_page()


if __name__ == "__main__":
    # Health check endpoint (for monitoring)
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--health-check":
        from health_check import health_check
        import json
        result = health_check()
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["status"] == "healthy" else 1)
    
    main()
