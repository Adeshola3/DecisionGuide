import json
from pathlib import Path

import streamlit as st

from utils.export import export_to_pdf, export_to_json, export_to_text, get_filename


# Page config
st.set_page_config(
    page_title="DecisionGuide",
    page_icon="🎯",
    layout="wide",
)


# Modern, calm styling
st.markdown(
    """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background: radial-gradient(circle at top, #eef2ff 0, #f9fafb 40%, #f5f5f7 100%);
    }

    .dg-shell {
        max-width: 1100px;
        margin: 2rem auto 3rem auto;
        padding: 2.5rem 2.25rem;
        background: rgba(255,255,255,0.96);
        border-radius: 24px;
        box-shadow:
            0 18px 45px rgba(15, 23, 42, 0.08),
            0 0 0 1px rgba(148, 163, 184, 0.08);
    }

    .dg-header-row {
        display: flex;
        gap: 2.25rem;
        align-items: center;
        margin-bottom: 2.25rem;
        flex-wrap: wrap;
    }

    .dg-hero-icon {
        width: 70px;
        height: 70px;
        border-radius: 24px;
        background: conic-gradient(from 160deg, #4f46e5, #6366f1, #a855f7, #4f46e5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.1rem;
        color: white;
        box-shadow: 0 12px 30px rgba(79,70,229,0.4);
    }

    .dg-header-main {
        flex: 1;
        min-width: 240px;
    }

    .dg-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        background: rgba(79,70,229,0.08);
        color: #4338ca;
        margin-bottom: 0.7rem;
    }

    .dg-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #22c55e;
    }

    .dg-header-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #020617;
        margin-bottom: 0.15rem;
    }

    .dg-header-tagline {
        font-size: 0.98rem;
        color: #6b7280;
        max-width: 520px;
    }

    .dg-header-subnote {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 0.4rem;
    }

    .dg-header-side {
        min-width: 220px;
    }

    .dg-stat-card {
        background: #0f172a;
        color: #e5e7eb;
        border-radius: 18px;
        padding: 1rem 1.1rem;
        font-size: 0.85rem;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.35);
    }

    .dg-stat-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #9ca3af;
        margin-bottom: 0.35rem;
    }

    .dg-stat-main {
        font-size: 0.95rem;
        margin-bottom: 0.35rem;
    }

    .dg-stat-pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
        margin-top: 0.2rem;
    }

    .dg-stat-pill {
        padding: 0.1rem 0.5rem;
        border-radius: 999px;
        font-size: 0.68rem;
        background: rgba(148,163,184,0.2);
        color: #e5e7eb;
    }

    .dg-section-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.35rem;
    }

    .dg-section-text {
        font-size: 0.9rem;
        color: #6b7280;
        line-height: 1.6;
        margin-bottom: 0.75rem;
    }

    .dg-assessment-card {
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        padding: 0.9rem 1rem;
        margin-bottom: 0.7rem;
        background: #f9fafb;
        transition: border-color 0.2s ease, background 0.2s ease, transform 0.15s ease;
        cursor: pointer;
    }

    .dg-assessment-card:hover {
        background: #eef2ff;
        border-color: #4f46e5;
        transform: translateY(-1px);
    }

    .dg-assessment-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.1rem;
    }

    .dg-assessment-desc {
        font-size: 0.83rem;
        color: #6b7280;
    }

    .dg-assessment-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-top: 0.4rem;
        font-size: 0.72rem;
        color: #9ca3af;
    }

    .dg-chip {
        padding: 0.12rem 0.55rem;
        border-radius: 999px;
        background: #eef2ff;
        color: #4f46e5;
        font-size: 0.72rem;
    }

    .dg-side-box {
        border-radius: 16px;
        background: #0b1120;
        color: #e5e7eb;
        padding: 1.3rem 1.4rem;
        font-size: 0.86rem;
    }

    .dg-side-title {
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
        color: #e5e7eb;
    }

    .dg-side-list {
        padding-left: 1.1rem;
        margin: 0.1rem 0 0.6rem 0;
        font-size: 0.83rem;
    }

    .dg-side-list li {
        margin-bottom: 0.25rem;
        color: #9ca3af;
    }

    .dg-footer {
        margin-top: 1.75rem;
        font-size: 0.8rem;
        color: #9ca3af;
        text-align: center;
    }

    .dg-footer a {
        color: #4f46e5;
        text-decoration: none;
        font-weight: 500;
    }
    .dg-footer a:hover {
        color: #312e81;
    }

    .stButton>button {
        border-radius: 999px;
        padding: 0.4rem 1.2rem;
        font-size: 0.88rem;
        font-weight: 500;
        border: 1px solid #4f46e5;
        color: #ffffff;
        background: linear-gradient(135deg, #4f46e5, #6366f1);
    }
    .stButton>button:hover {
        filter: brightness(1.04);
    }

    .stDownloadButton>button {
        border-radius: 999px;
        padding: 0.4rem 0.9rem;
        font-size: 0.82rem;
        font-weight: 500;
        border: 1px solid #4f46e5;
        color: #ffffff;
        background: linear-gradient(135deg, #4f46e5, #6366f1);
    }

    @media (max-width: 800px) {
        .dg-shell {
            margin: 0;
            border-radius: 0;
            box-shadow: none;
        }
        .dg-header-row {
            flex-direction: column;
            align-items: flex-start;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)


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


def traverse_tree_interactive(tree, node_id, answers, path_so_far):
    nodes = tree["nodes"]
    node = nodes[node_id]

    node_label = node.get("text", "")
    node_type = node.get("type", "choice")

    if node_type == "choice":
        question_index = len(path_so_far) + 1
        st.markdown(f"**Question {question_index}**")
        st.write(node_label)

        options = list(node["options"].keys())

        if node_id in answers:
            selected = answers[node_id]
        else:
            selected = st.radio(
                "Select an option:",
                options,
                index=None,
                key=f"{tree['id']}_{node_id}",
            )
            if selected is None:
                st.write("")
                return None, None, path_so_far
            answers[node_id] = selected

        path_entry = f"{node_label} → {selected}"
        new_path = path_so_far + [path_entry]

        selected_branch = node["options"][selected]

        if "decision" in selected_branch:
            decision = selected_branch["decision"]
            explanation = selected_branch.get("explanation", "")
            return decision, explanation, new_path

        next_node = selected_branch["next"]
        st.write("")
        return traverse_tree_interactive(tree, next_node, answers, new_path)

    elif node_type == "text":
        st.markdown(node_label)
        return None, None, path_so_far + [node_label]

    else:
        st.warning(f"Unknown node type: {node_type}")
        return None, None, path_so_far


def render_dpia_jurisdiction_block():
    st.markdown("---")
    st.markdown("#### Jurisdiction-specific pointers")

    region = st.selectbox(
        "Which jurisdiction are you mainly working under?",
        [
            "Select...",
            "UK / ICO (UK GDPR / DPA 2018)",
            "EU / EDPB (EU GDPR)",
            "US (HIPAA / state privacy laws)",
            "Nigeria (NDPR)",
            "Other / mixed",
        ],
        index=0,
        key="dpia_jurisdiction",
    )

    if region == "Select...":
        return

    if region.startswith("UK"):
        st.markdown(
            "- Check UK GDPR Article 35 and ICO guidance on when a DPIA is mandatory.\n"
            "- If CCTV, large-scale monitoring, or profiling is involved, verify against ICO DPIA examples.\n"
            "- Use ICO DPIA templates to structure documentation."
        )
    elif region.startswith("EU"):
        st.markdown(
            "- Refer to EU GDPR Article 35 and EDPB guidelines on DPIA.\n"
            "- Check your activity against your authority’s DPIA 'blacklist' and 'whitelist'.\n"
            "- Evidence DPO consultation where required."
        )
    elif region.startswith("US"):
        st.markdown(
            "- Map your DPIA-style assessment to HIPAA Security Rule risk analysis if health data is involved.\n"
            "- Consider state privacy laws (for example CPRA) where profiling or high-risk processing is in scope.\n"
            "- Treat this as a structured impact assessment even if the term 'DPIA' is not used."
        )
    elif region.startswith("Nigeria"):
        st.markdown(
            "- Align to NDPR requirements for high-risk processing.\n"
            "- Check any NITDA guidance for your sector.\n"
            "- Pay attention to cross-border transfers and hosting expectations."
        )
    else:
        st.markdown(
            "- Align your assessment with any applicable local privacy or sector law.\n"
            "- Where no formal DPIA requirement exists, treat this as evidence of responsible risk analysis.\n"
            "- Make sure your reasoning and mitigations are clearly documented."
        )


def show_landing_page():
    trees = load_trees()

    st.markdown("<div class='dg-shell'>", unsafe_allow_html=True)

    # Header / hero row
    st.markdown("<div class='dg-header-row'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='dg-hero-icon'>🎯</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='dg-header-main'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='dg-badge'><span class='dg-dot'></span> Open source · GRC-focused</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='dg-header-title'>DecisionGuide</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='dg-header-tagline'>A lightweight, logic-based assistant that helps you make consistent, defensible governance and audit decisions.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='dg-header-subnote'>No uploads · No personal data · Everything stays in the browser.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)  # close header-main

    st.markdown("<div class='dg-header-side'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='dg-stat-card'>
            <div class='dg-stat-label'>Built for</div>
            <div class='dg-stat-main'>Analysts, auditors, and students who hate guesswork.</div>
            <div class='dg-stat-pill-row'>
                <span class='dg-stat-pill'>Vendor risk</span>
                <span class='dg-stat-pill'>DPIA checks</span>
                <span class='dg-stat-pill'>Incident logic</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)  # header-side

    st.markdown("</div>", unsafe_allow_html=True)  # header-row

    st.markdown("---")

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown("<div class='dg-section-title'>Available guides</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='dg-section-text'>Start with any assessment below. You’ll be guided through a series of simple questions until a clear outcome is reached.</div>",
            unsafe_allow_html=True,
        )

        for tree_id, tree in trees.items():
            title = tree.get("title", "Assessment")
            desc = tree.get("description", "")

            # Card
            st.markdown("<div class='dg-assessment-card'>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='dg-assessment-title'>{title}</div>",
                unsafe_allow_html=True,
            )
            if desc:
                st.markdown(
                    f"<div class='dg-assessment-desc'>{desc}</div>",
                    unsafe_allow_html=True,
                )
            st.markdown(
                """
                <div class='dg-assessment-meta'>
                    <span>Logic-based · No code required</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # Button
            if st.button(f"Start “{title}”", key=f"start_{tree_id}"):
                st.session_state.selected_tree = tree_id
                st.session_state.show_landing = False
                st.session_state.pop(f"answers_{tree_id}", None)
                st.session_state.pop(f"result_{tree_id}", None)
                st.experimental_rerun()

    with col_right:
        st.markdown("<div class='dg-section-title'>What DecisionGuide is for</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='dg-side-box'>
              <div class='dg-side-title'>Use it when you need:</div>
              <ul class='dg-side-list'>
                <li>A quick, structured DPIA requirement check.</li>
                <li>Simple vendor risk tiering without spreadsheets.</li>
                <li>Transparent logic you can show to auditors or managers.</li>
                <li>A repeatable way to explain why a decision was made.</li>
              </ul>
              <div style='font-size:0.8rem; color:#9ca3af;'>
                The tool guides judgement, it does not replace it.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class='dg-footer'>
            Open source · MIT Licence · 
            <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank'>View on GitHub</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)  # close shell


def show_assessment_page():
    trees = load_trees()

    if st.button("← Back to home"):
        st.session_state.show_landing = True
        st.session_state.pop("selected_tree", None)
        st.experimental_rerun()

    st.markdown("<div class='dg-shell'>", unsafe_allow_html=True)

    selected_tree_id = st.session_state.get("selected_tree")
    if not selected_tree_id or selected_tree_id not in trees:
        st.error("Assessment not found.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    tree = trees[selected_tree_id]

    st.markdown("<div class='dg-badge'><span class='dg-dot'></span> Assessment</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='dg-header-title'>{tree.get('title', 'Assessment')}</div>",
        unsafe_allow_html=True,
    )
    if tree.get("description"):
        st.markdown(
            f"<div class='dg-header-tagline'>{tree['description']}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    answers_key = f"answers_{selected_tree_id}"
    result_key = f"result_{selected_tree_id}"

    if answers_key not in st.session_state:
        st.session_state[answers_key] = {}

    if result_key not in st.session_state:
        st.session_state[result_key] = None

    answers = st.session_state[answers_key]

    decision, explanation, path = traverse_tree_interactive(
        tree,
        tree["root"],
        answers,
        [],
    )

    if decision is not None:
        st.session_state[result_key] = {
            "decision": decision,
            "explanation": explanation,
            "path": path,
        }

    result = st.session_state[result_key]

    if result is not None:
        st.markdown("---")
        st.success("Assessment complete.")

        st.markdown("#### Result")
        st.write(f"**Decision code:** {result['decision']}")
        if result["explanation"]:
            st.write(result["explanation"])

        st.markdown("#### Path taken")
        for step in result["path"]:
            st.write(f"- {step}")

        if selected_tree_id.startswith("dpia"):
            render_dpia_jurisdiction_block()

        st.markdown("---")
        st.markdown("#### Export")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            pdf_buffer = export_to_pdf(
                tree.get("title", "Assessment"),
                result["decision"],
                result["explanation"],
                result["path"],
            )
            st.download_button(
                label="📄 PDF",
                data=pdf_buffer,
                file_name=get_filename(tree.get("title", "Assessment"), "pdf"),
                mime="application/pdf",
            )

        with col2:
            json_data = export_to_json(
                tree.get("title", "Assessment"),
                result["decision"],
                result["explanation"],
                result["path"],
            )
            st.download_button(
                label="📋 JSON",
                data=json_data,
                file_name=get_filename(tree.get("title", "Assessment"), "json"),
                mime="application/json",
            )

        with col3:
            text_data = export_to_text(
                tree.get("title", "Assessment"),
                result["decision"],
                result["explanation"],
                result["path"],
            )
            st.download_button(
                label="📝 TXT",
                data=text_data,
                file_name=get_filename(tree.get("title", "Assessment"), "txt"),
                mime="text/plain",
            )

        with col4:
            if st.button("🔄 Start over"):
                st.session_state[answers_key] = {}
                st.session_state[result_key] = None
                st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    if "show_landing" not in st.session_state:
        st.session_state.show_landing = True

    if st.session_state.show_landing:
        show_landing_page()
    else:
        show_assessment_page()


if __name__ == "__main__":
    main()