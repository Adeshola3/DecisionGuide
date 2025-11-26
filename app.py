import json
from pathlib import Path

import streamlit as st

from utils.export import export_to_pdf, export_to_json, export_to_text, get_filename


st.set_page_config(
    page_title="DecisionGuide",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark Elegant Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Dark background */
    .stApp {
        background: #1a2332;
    }
    
    /* Force white text for assessment page */
    .stMarkdown, .stMarkdown p {
        color: #e8eaed !important;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
    }
    
    .stRadio label, .stRadio span {
        color: #e8eaed !important;
        font-weight: 500 !important;
    }
    
    div[data-baseweb="notification"] * {
        color: #1a2332 !important;
        font-weight: 500 !important;
    }
    
    /* Hero Section - Dark Elegant */
    .hero-container {
        background: linear-gradient(135deg, #1e3a5f 0%, #1a2332 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 3rem 2rem;
    }
    
    .hero-content {
        max-width: 700px;
        text-align: center;
    }
    
    .hero-logo {
        width: 120px;
        height: 120px;
        margin: 0 auto 2rem auto;
        background: transparent;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 5rem;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1.5rem;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #d4af76;
        font-weight: 500;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 3rem;
    }
    
    /* Feature Badges */
    .feature-badges {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 3rem;
    }
    
    .feature-badge {
        background: rgba(212, 175, 118, 0.15);
        border: 2px solid rgba(212, 175, 118, 0.3);
        border-radius: 50px;
        padding: 1.2rem 2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .feature-badge:hover {
        background: rgba(212, 175, 118, 0.25);
        border-color: rgba(212, 175, 118, 0.5);
        transform: translateX(10px);
    }
    
    .feature-icon {
        width: 50px;
        height: 50px;
        background: #d4af76;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        flex-shrink: 0;
    }
    
    .feature-text {
        font-size: 1.2rem;
        font-weight: 600;
        color: #ffffff;
        text-align: left;
    }
    
    /* Description */
    .hero-description {
        font-size: 1.1rem;
        color: #b8c4d6;
        line-height: 1.8;
        margin-bottom: 3rem;
    }
    
    /* Buttons */
    .stButton>button {
        background: #d4af76;
        color: #1a2332;
        border: none;
        padding: 1.2rem 3rem;
        font-size: 1.1rem;
        font-weight: 700;
        border-radius: 50px;
        transition: all 0.3s ease;
        width: 100%;
        max-width: 400px;
        text-transform: capitalize;
    }
    
    .stButton>button:hover {
        background: #e8c589;
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(212, 175, 118, 0.4);
    }
    
    /* Assessment Grid */
    .assessment-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        max-width: 1200px;
        margin: 3rem auto;
        padding: 0 2rem;
    }
    
    .assessment-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #1a2332 100%);
        border: 2px solid rgba(212, 175, 118, 0.2);
        border-radius: 20px;
        padding: 2.5rem;
        min-height: 280px;
        transition: all 0.3s ease;
    }
    
    .assessment-card:hover {
        border-color: rgba(212, 175, 118, 0.5);
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
    }
    
    .assessment-number {
        font-size: 0.85rem;
        font-weight: 600;
        color: #d4af76;
        letter-spacing: 2px;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }
    
    .assessment-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    .assessment-description {
        font-size: 0.95rem;
        color: #b8c4d6;
        line-height: 1.7;
    }
    
    /* Section Headers */
    .section-header {
        text-align: center;
        margin: 4rem 0 3rem 0;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    .section-subtitle {
        font-size: 1.1rem;
        color: #d4af76;
        font-weight: 500;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 4rem 2rem;
        color: #b8c4d6;
        max-width: 800px;
        margin: 4rem auto 0 auto;
        border-top: 1px solid rgba(212, 175, 118, 0.2);
    }
    
    .footer-links a {
        color: #d4af76;
        text-decoration: none;
        margin: 0 1.5rem;
        font-weight: 600;
        transition: color 0.2s ease;
    }
    
    .footer-links a:hover {
        color: #e8c589;
    }
    
    /* Download Buttons */
    .stDownloadButton>button {
        background: rgba(212, 175, 118, 0.15);
        color: #d4af76;
        border: 2px solid rgba(212, 175, 118, 0.3);
        padding: 0.75rem 1.5rem;
        font-size: 0.9rem;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        background: rgba(212, 175, 118, 0.25);
        border-color: #d4af76;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .feature-badge {
            padding: 1rem 1.5rem;
        }
        
        .feature-text {
            font-size: 1rem;
        }
        
        .assessment-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)


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


def show_landing_page():
    """Dark elegant landing page"""
    
    # Use columns to center the button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class='hero-container'>
            <div class='hero-content'>
                <div class='hero-logo'>🎯</div>
                
                <h1 class='hero-title'>DecisionGuide</h1>
                
                <p class='hero-subtitle'>Open-Source Assessment For GRC Professionals</p>
                
                <div class='feature-badges'>
                    <div class='feature-badge'>
                        <div class='feature-icon'>🌳</div>
                        <div class='feature-text'>Structured Assessment Logic</div>
                    </div>
                    
                    <div class='feature-badge'>
                        <div class='feature-icon'>📋</div>
                        <div class='feature-text'>Research-Backed Frameworks</div>
                    </div>
                    
                    <div class='feature-badge'>
                        <div class='feature-icon'>🛡️</div>
                        <div class='feature-text'>Consistent, Defensible Decisions</div>
                    </div>
                </div>
                
                <p class='hero-description'>
                    Make clearer GRC judgments with guided assessment flows 
                    (ISO 27001, GDPR, NIST CSF) based on industry research.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Button below the hero content
        if st.button("Start an Assessment", key="main_cta", use_container_width=True):
            st.session_state.show_selection = True
            st.rerun()


def show_assessment_selection():
    """Show assessment selection page"""
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.show_selection = False
        st.rerun()
    
    st.markdown("""
    <div class='section-header'>
        <h2 class='section-title'>Choose an Assessment</h2>
        <p class='section-subtitle'>Select a framework to begin</p>
    </div>
    """, unsafe_allow_html=True)
    
    trees = load_trees()
    
    # Use Streamlit columns with HTML cards
    cols = st.columns(3)
    assessment_numbers = ["Assessment 01", "Assessment 02", "Assessment 03"]
    
    for idx, (tree_id, tree_data) in enumerate(trees.items()):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='assessment-card'>
                <div class='assessment-number'>{assessment_numbers[idx]}</div>
                <h3 class='assessment-title'>{tree_data.get('title', 'Assessment')}</h3>
                <p class='assessment-description'>{tree_data.get('description', '')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Begin Assessment", key=f"start_{tree_id}", use_container_width=True):
                st.session_state.selected_tree = tree_id
                st.session_state.show_landing = False
                st.session_state.show_selection = False
                st.rerun()
    
    # Footer
    st.markdown("""
    <div class='footer'>
        <p style='font-size: 1.1rem; margin-bottom: 1.5rem;'>
            <strong style='color: #ffffff;'>DecisionGuide</strong> — Making structured, smart decisions, one at a time.
        </p>
        <div class='footer-links'>
            <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank'>⭐ GitHub</a>
            <a href='https://github.com/Adeshola3/DecisionGuide/issues' target='_blank'>💬 Contribute</a>
        </div>
        <p style='margin-top: 1.5rem; font-size: 0.9rem; color: #6b7280;'>
            Open Source • MIT License
        </p>
    </div>
    """, unsafe_allow_html=True)


def traverse_tree_interactive(tree, node_id, answers, path_so_far):
    """Interactively traverse the tree"""
    nodes = tree["nodes"]
    node = nodes[node_id]
    
    node_label = node.get("text", "")
    node_type = node.get("type", "choice")
    
    if node_type == "choice":
        current_question = len(answers) + 1
        st.info(f"📊 Question {current_question}")
        st.markdown("---")
        
        options = list(node["options"].keys())
        
        if node_id in answers:
            selected = answers[node_id]
        else:
            selected = st.radio(
                node_label, 
                options, 
                key=f"{tree['id']}_{node_id}",
                index=None
            )
            
            if selected is None:
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
        return traverse_tree_interactive(tree, next_node, answers, new_path)
    
    elif node_type == "text":
        st.markdown(node_label)
        return None, None, path_so_far + [node_label]
    
    else:
        st.warning(f"Unknown node type: {node_type}")
        return None, None, path_so_far


def show_assessment_page():
    """Display the assessment page"""
    trees = load_trees()
    
    # Back button
    if st.button("← Back to Selection"):
        st.session_state.show_selection = True
        st.session_state.pop('selected_tree', None)
        st.rerun()
    
    st.markdown("---")
    
    selected_tree_id = st.session_state.get('selected_tree')
    
    if not selected_tree_id or selected_tree_id not in trees:
        st.error("Assessment not found")
        return
    
    tree = trees[selected_tree_id]
    
    st.title(tree.get("title", "Assessment"))
    if tree.get("description"):
        st.info(tree["description"])
    
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
        []
    )

    if decision is not None:
        st.session_state[result_key] = {
            "decision": decision,
            "explanation": explanation,
            "path": path
        }

    if st.session_state[result_key] is not None:
        st.success("✅ Assessment Complete!")
        
        st.markdown("---")
        
        result = st.session_state[result_key]
        
        st.markdown("### Result")
        st.write(f"**Decision:** {result['decision']}")
        if result['explanation']:
            st.write(result['explanation'])

        st.markdown("### Decision Path")
        for step in result['path']:
            st.write(f"→ {step}")
        
        st.markdown("---")
        st.markdown("### Export Options")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pdf_buffer = export_to_pdf(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📄 PDF",
                data=pdf_buffer,
                file_name=get_filename(tree.get("title", "Assessment"), "pdf"),
                mime="application/pdf"
            )
        
        with col2:
            json_data = export_to_json(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📋 JSON",
                data=json_data,
                file_name=get_filename(tree.get("title", "Assessment"), "json"),
                mime="application/json"
            )
        
        with col3:
            text_data = export_to_text(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📝 TXT",
                data=text_data,
                file_name=get_filename(tree.get("title", "Assessment"), "txt"),
                mime="text/plain"
            )
        
        with col4:
            if st.button("🔄 Restart"):
                st.session_state[answers_key] = {}
                st.session_state[result_key] = None
                st.rerun()


def main():
    if 'show_landing' not in st.session_state:
        st.session_state.show_landing = True
    
    if 'show_selection' not in st.session_state:
        st.session_state.show_selection = False
    
    if st.session_state.show_landing and not st.session_state.show_selection:
        show_landing_page()
    elif st.session_state.show_selection:
        show_assessment_selection()
    else:
        show_assessment_page()


if __name__ == "__main__":
    main()
