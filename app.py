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

# Lavender Purple Stylish Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Lavender background */
    .stApp {
        background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 50%, #faf5ff 100%);
    }
    
    /* Force text visibility */
    .stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6 {
        color: #4c1d95 !important;
    }
    
    .stRadio label, .stRadio span {
        color: #4c1d95 !important;
        font-weight: 500 !important;
    }
    
    div[data-baseweb="notification"] * {
        color: #6b21a8 !important;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #a78bfa 0%, #c084fc 50%, #e879f9 100%);
        padding: 5rem 2rem;
        border-radius: 30px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(168, 85, 247, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 8s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .hero-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 4px 12px rgba(0,0,0,0.2));
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: white;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        font-weight: 500;
        margin-bottom: 1rem;
        opacity: 0.95;
        color: white;
    }
    
    .hero-description {
        font-size: 1.1rem;
        max-width: 700px;
        margin: 0 auto;
        opacity: 0.9;
        color: white;
        line-height: 1.8;
    }
    
    /* Section Headers */
    .section-header {
        text-align: center;
        margin: 4rem 0 3rem 0;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #6b21a8;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .section-subtitle {
        font-size: 1.1rem;
        color: #9333ea;
        font-weight: 500;
    }
    
    /* Feature Cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        margin: 0 0 4rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2.5rem 2rem;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(167, 139, 250, 0.15);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid transparent;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(167, 139, 250, 0.3);
        border-color: #c084fc;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #7c3aed;
        margin-bottom: 0.75rem;
    }
    
    .feature-text {
        color: #6b7280;
        font-size: 1rem;
        line-height: 1.7;
    }
    
    /* Assessment Cards */
    .assessment-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        margin-bottom: 4rem;
    }
    
    .assessment-card {
        background: linear-gradient(135deg, #a78bfa 0%, #c084fc 100%);
        padding: 2.5rem;
        border-radius: 24px;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        box-shadow: 0 8px 30px rgba(167, 139, 250, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .assessment-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .assessment-card:hover::before {
        opacity: 1;
    }
    
    .assessment-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 16px 50px rgba(167, 139, 250, 0.4);
    }
    
    .assessment-number {
        font-size: 0.9rem;
        font-weight: 700;
        color: rgba(255,255,255,0.8);
        letter-spacing: 3px;
        margin-bottom: 1rem;
    }
    
    .assessment-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: white;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .assessment-description {
        font-size: 1rem;
        color: rgba(255,255,255,0.9);
        line-height: 1.7;
        flex-grow: 1;
        position: relative;
        z-index: 1;
    }
    
    /* Use Case Cards */
    .usecase-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 2rem;
        margin-bottom: 4rem;
    }
    
    .usecase-card {
        background: white;
        padding: 2.5rem;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(167, 139, 250, 0.15);
        border-left: 5px solid #a78bfa;
    }
    
    .usecase-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #7c3aed;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .usecase-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .usecase-list li {
        padding: 0.75rem 0;
        color: #6b7280;
        font-size: 1rem;
        border-bottom: 1px solid #f3f4f6;
        line-height: 1.6;
    }
    
    .usecase-list li:last-child {
        border-bottom: none;
    }
    
    .usecase-list li::before {
        content: '✦';
        margin-right: 1rem;
        color: #c084fc;
        font-weight: bold;
    }
    
    /* CTA Section */
    .cta-section {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #c026d3 100%);
        padding: 4rem 2rem;
        border-radius: 30px;
        text-align: center;
        color: white;
        margin: 4rem 0;
        box-shadow: 0 20px 60px rgba(124, 58, 237, 0.4);
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: white;
    }
    
    .cta-text {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.8;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 2rem;
        background: white;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(167, 139, 250, 0.15);
        margin-top: 4rem;
    }
    
    .footer-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #6b21a8;
        margin-bottom: 0.5rem;
    }
    
    .footer-text {
        color: #9333ea;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .footer-links a {
        color: #a78bfa;
        text-decoration: none;
        margin: 0 1rem;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    .footer-links a:hover {
        color: #7c3aed;
    }
    
    .footer-note {
        margin-top: 1.5rem;
        font-size: 0.9rem;
        color: #9ca3af;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #a78bfa 0%, #c084fc 100%);
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        font-size: 1rem;
        font-weight: 700;
        border-radius: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(167, 139, 250, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(167, 139, 250, 0.5);
        background: linear-gradient(135deg, #c084fc 0%, #e879f9 100%);
    }
    
    /* Download Buttons */
    .stDownloadButton>button {
        background: white;
        color: #7c3aed;
        border: 2px solid #a78bfa;
        padding: 0.75rem 1.5rem;
        font-size: 0.9rem;
        font-weight: 600;
        border-radius: 50px;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        background: #a78bfa;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .feature-grid,
        .assessment-grid,
        .usecase-grid {
            grid-template-columns: 1fr;
        }
        
        .hero-title {
            font-size: 2.2rem;
        }
        
        .section-title {
            font-size: 2rem;
        }
    }
    
    @media (max-width: 480px) {
        .hero-title {
            font-size: 1.8rem;
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
    """Lavender purple stylish landing page"""
    
    # Hero Section
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-content'>
            <div class='hero-icon'>🎯</div>
            <h1 class='hero-title'>DecisionGuide</h1>
            <p class='hero-subtitle'>Open-source assessment framework for GRC professionals</p>
            <p class='hero-description'>
                Make consistent, defensible decisions through structured logic flows. 
                Built with empathy for professionals who need clarity in complex assessments.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Why DecisionGuide
    st.markdown("""
    <div class='section-header'>
        <h2 class='section-title'>Why DecisionGuide?</h2>
        <p class='section-subtitle'>Everything you need for professional GRC assessments</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='feature-grid'>
        <div class='feature-card'>
            <span class='feature-icon'>🔍</span>
            <h3 class='feature-title'>Transparent Logic</h3>
            <p class='feature-text'>
                See exactly how decisions are reached with clear, step-by-step reasoning. 
                Every path is documented and traceable.
            </p>
        </div>
        
        <div class='feature-card'>
            <span class='feature-icon'>🔒</span>
            <h3 class='feature-title'>Privacy First</h3>
            <p class='feature-text'>
                Zero-document approach means no file uploads, no data collection. 
                All processing happens locally in your browser.
            </p>
        </div>
        
        <div class='feature-card'>
            <span class='feature-icon'>📄</span>
            <h3 class='feature-title'>Audit Ready</h3>
            <p class='feature-text'>
                Export professional reports in PDF, JSON, or TXT formats. 
                Complete audit trails for compliance documentation.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Available Assessments
    st.markdown("""
    <div class='section-header'>
        <h2 class='section-title'>Available Assessments</h2>
        <p class='section-subtitle'>Choose an assessment to get started</p>
    </div>
    """, unsafe_allow_html=True)
    
    trees = load_trees()
    assessment_numbers = ["01", "02", "03"]
    
    # Assessment cards
    cards_html = "<div class='assessment-grid'>"
    for idx, (tree_id, tree_data) in enumerate(trees.items()):
        cards_html += f"""
        <div class='assessment-card'>
            <div class='assessment-number'>{assessment_numbers[idx] if idx < len(assessment_numbers) else f"0{idx+1}"}</div>
            <h3 class='assessment-title'>{tree_data.get('title', 'Assessment')}</h3>
            <p class='assessment-description'>{tree_data.get('description', '')}</p>
        </div>
        """
    cards_html += "</div>"
    
    st.markdown(cards_html, unsafe_allow_html=True)
    
    # Buttons
    cols = st.columns(len(trees))
    for idx, (tree_id, tree_data) in enumerate(trees.items()):
        with cols[idx % 3]:
            if st.button(f"Start Assessment", key=f"start_{tree_id}", use_container_width=True):
                st.session_state.selected_tree = tree_id
                st.session_state.show_landing = False
                st.rerun()
    
    # Who Is This For
    st.markdown("""
    <div class='section-header'>
        <h2 class='section-title'>Who Is This For?</h2>
        <p class='section-subtitle'>Built for GRC professionals who demand excellence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='usecase-grid'>
        <div class='usecase-card'>
            <h3 class='usecase-title'>👨‍💼 For Auditors</h3>
            <ul class='usecase-list'>
                <li>Standardize assessment approaches across teams</li>
                <li>Generate consistent, defensible decisions</li>
                <li>Produce audit-ready documentation instantly</li>
            </ul>
        </div>
        
        <div class='usecase-card'>
            <h3 class='usecase-title'>📊 For Risk Managers</h3>
            <ul class='usecase-list'>
                <li>Classify vendors systematically</li>
                <li>Tier risks consistently across organization</li>
                <li>Document decision rationale clearly</li>
            </ul>
        </div>
        
        <div class='usecase-card'>
            <h3 class='usecase-title'>✅ For Compliance Teams</h3>
            <ul class='usecase-list'>
                <li>Determine regulatory requirements quickly</li>
                <li>Apply jurisdiction-specific rules accurately</li>
                <li>Maintain complete audit trails</li>
            </ul>
        </div>
        
        <div class='usecase-card'>
            <h3 class='usecase-title'>🛡️ For Security Teams</h3>
            <ul class='usecase-list'>
                <li>Assess incident severity objectively</li>
                <li>Make reporting decisions confidently</li>
                <li>Document incident response choices</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA
    st.markdown("""
    <div class='cta-section'>
        <h2 class='cta-title'>Ready to Make Better Decisions?</h2>
        <p class='cta-text'>
            Join GRC professionals using DecisionGuide for consistent, defensible assessments 
            backed by structured logic and complete transparency.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class='footer'>
        <p class='footer-title'>DecisionGuide</p>
        <p class='footer-text'>Making structured, smart decisions—one at a time.</p>
        <p class='footer-text'>Built with empathy for professionals who need clarity in complex assessments.</p>
        <div class='footer-links'>
            <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank'>⭐ Star on GitHub</a>
            <a href='https://github.com/Adeshola3/DecisionGuide/issues' target='_blank'>💬 Contribute</a>
        </div>
        <p class='footer-note'>Open source • MIT License • Made with 💜</p>
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
    if st.button("← Back to Home"):
        st.session_state.show_landing = True
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
            st.write(f"- {step}")
        
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
    
    if st.session_state.show_landing:
        show_landing_page()
    else:
        show_assessment_page()


if __name__ == "__main__":
    main()