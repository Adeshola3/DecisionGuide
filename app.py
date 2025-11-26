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

# Custom CSS for the NEW "Midnight Compliance" styling
# Color Palette:
# Background: #1a1d2d (Deep Charcoal/Navy)
# Primary Text: #f0f2f6 (Light Gray/White)
# Accent Color (Teal): #00cc99
# Secondary Accent (Lighter Teal): #00ffc6
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Dark background for the main app */
    .stApp {
        background: #1a1d2d;
    }
    
    /* Ensure all text is visible on the dark background */
    .stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6 {
        color: #f0f2f6 !important; /* Light text for readability */
    }
    
    /* Input elements and labels */
    .stRadio label, .stRadio span, .stTextInput label, .stSelectbox label {
        color: #f0f2f6 !important;
        font-weight: 500 !important;
    }
    
    /* Notification/Info boxes */
    div[data-baseweb="notification"] * {
        color: #00cc99 !important; /* Teal accent */
    }
    
    /* Hero section styling - Clean and sharp */
    .hero-section {
        background: #232738; /* Slightly lighter dark background */
        padding: 6rem 2rem;
        border-radius: 15px;
        text-align: center;
        color: #f0f2f6;
        margin-bottom: 3rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.4);
        min-height: 80vh;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #00cc9933; /* Subtle accent border */
    }
    
    .hero-content {
        max-width: 900px;
        margin: 0 auto;
    }
    
    .hero-logo {
        font-size: 8rem;
        margin-bottom: 2rem;
        color: #00cc99; /* Teal logo */
        filter: drop-shadow(0 0 10px rgba(0,204,153,0.5));
    }
    
    .hero-title {
        font-size: 5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #f0f2f6;
        letter-spacing: -3px;
    }
    
    .hero-subtitle {
        font-size: 1.6rem;
        margin-bottom: 2rem;
        color: #00ffc6; /* Lighter teal for sub-header */
        line-height: 1.6;
    }
    
    .hero-description {
        font-size: 1.15rem;
        max-width: 800px;
        margin: 0 auto;
        opacity: 0.8;
        color: #cccccc;
        line-height: 1.8;
    }
    
    /* Feature cards */
    .feature-card {
        background: #232738;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.4);
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 5px solid #00cc99; /* Strong accent line */
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #00ffc6;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f0f2f6;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #cccccc;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Assessment cards */
    .assessment-card {
        /* Using gradients for variety but keeping the dark tone */
        background: linear-gradient(135deg, #232738 0%, #1a1d2d 100%); 
        padding: 2rem;
        border-radius: 10px;
        color: #f0f2f6;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4);
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
        border: 1px solid #00cc99;
    }
    
    .assessment-card:hover {
        transform: translateY(-5px);
        background: #2a3148;
    }
    
    .assessment-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #00ffc6; /* Teal accent title */
    }
    
    .assessment-description {
        font-size: 0.95rem;
        opacity: 0.8;
        flex-grow: 1;
        color: #cccccc;
    }
    
    /* Section styling */
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin: 3rem 0 0.5rem 0;
        color: #f0f2f6;
    }
    
    .section-subtitle {
        text-align: center;
        color: #00cc99; /* Accent for subtitle */
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
    
    /* Use case boxes */
    .use-case-box {
        background: #232738;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #00ffc6;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .use-case-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #00ffc6;
        margin-bottom: 0.5rem;
    }
    
    .use-case-box ul, .use-case-box li {
        color: #cccccc;
        list-style-type: '👉 '; /* Custom bullet */
    }
    
    .use-case-box li {
        margin-bottom: 0.5rem;
    }
    
    /* CTA section */
    .cta-section {
        background: #00cc99; /* Solid accent background */
        padding: 3rem;
        border-radius: 15px;
        text-align: center;
        color: #1a1d2d;
        margin: 3rem 0;
        box-shadow: 0 5px 20px rgba(0,204,153,0.5);
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #1a1d2d; /* Dark text on bright background */
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 2rem;
        color: #cccccc;
        margin-top: 3rem;
        background: #232738;
        border-radius: 15px;
        border-top: 3px solid #00cc99;
    }
    
    .custom-footer strong {
        color: #f0f2f6;
    }
    
    .custom-footer a {
        color: #00ffc6;
        text-decoration: none;
        font-weight: 600;
    }
    
    .custom-footer a:hover {
        color: #00cc99;
        text-decoration: underline;
    }
    
    /* Buttons - Primary Action */
    .stButton>button {
        background: #00cc99;
        color: #1a1d2d;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 700;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 204, 153, 0.5);
        background: #00ffc6;
    }
    
    /* Download Buttons - Secondary Action */
    .stDownloadButton>button {
        background: #232738;
        color: #00cc99;
        border: 2px solid #00cc99;
        padding: 0.75rem 2rem;
        font-size: 0.9rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 204, 153, 0.2);
        color: #00ffc6;
        border-color: #00ffc6;
    }
    
    /* Reroute the Radio Buttons to look better on dark theme */
    div[data-testid="stRadio"] label {
        background: #232738;
        padding: 10px 15px;
        border-radius: 5px;
        border: 1px solid #3d4560;
        margin-bottom: 5px;
        cursor: pointer;
        transition: all 0.2s;
    }

    div[data-testid="stRadio"] label:has(input:checked) {
        background: #00cc991a; /* Very light teal shade */
        border-color: #00ffc6;
        box-shadow: 0 0 10px rgba(0,204,153,0.3);
    }
    
    /* Responsive Design (Keep for mobile) */
    @media (max-width: 768px) {
        .hero-logo { font-size: 5rem; }
        .hero-title { font-size: 3rem; }
        .hero-subtitle { font-size: 1.2rem; }
        .hero-description { font-size: 1rem; }
        .section-title { font-size: 2rem; }
        .feature-card, .assessment-card, .use-case-box { margin-bottom: 1.5rem; }
    }
    
    @media (max-width: 480px) {
        .hero-logo { font-size: 4rem; }
        .hero-title { font-size: 2.2rem; }
        .hero-subtitle { font-size: 1rem; }
        .hero-description { font-size: 0.9rem; }
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
    """Display the authoritative "Midnight Compliance" landing page"""
    
    # Hero Section - BIG CENTERED
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-content'>
            <div class='hero-logo'>🎯</div>
            <div class='hero-title'>DecisionGuide</div>
            <div class='hero-subtitle'>Open-source assessment framework for GRC professionals</div>
            <div class='hero-description'>
                Make consistent, defensible decisions through structured logic flows. 
                Built with empathy for professionals who need clarity in complex assessments.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("<div class='section-title'>Why DecisionGuide?</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Everything you need for professional GRC assessments</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🔍</div>
            <div class='feature-title'>Transparent Logic</div>
            <div class='feature-text'>
                See exactly how decisions are reached with clear, step-by-step reasoning. 
                Every path is documented and traceable.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🔒</div>
            <div class='feature-title'>Privacy First</div>
            <div class='feature-text'>
                Zero-document approach means no file uploads, no data collection. 
                All processing happens locally in your browser.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📄</div>
            <div class='feature-title'>Audit Ready</div>
            <div class='feature-text'>
                Export professional reports in PDF, JSON, or TXT formats. 
                Complete audit trails for compliance documentation.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Available Assessments
    st.markdown("<div class='section-title'>📋 Available Assessments</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Choose an assessment to get started</div>", unsafe_allow_html=True)
    
    trees = load_trees()
    
    # Use consistent card styling with the new dark theme
    cols = st.columns(min(len(trees), 3))
    
    # Define a set of different gradients for variety, all within the dark/teal family
    dark_gradients = [
        "linear-gradient(135deg, #1a1d2d 0%, #2a3148 100%)",
        "linear-gradient(135deg, #2a3148 0%, #1a1d2d 100%)",
        "linear-gradient(135deg, #1f2334 0%, #282d3e 100%)",
    ]
    
    for idx, (tree_id, tree_data) in enumerate(trees.items()):
        with cols[idx % 3]:
            gradient = dark_gradients[idx % len(dark_gradients)]
            
            # Applying the assessment-card style from the new CSS
            st.markdown(f"""
            <div class='assessment-card' style='background: {gradient};'>
                <div>
                    <div class='assessment-title'>{tree_data.get('title', 'Assessment')}</div>
                    <div class='assessment-description'>{tree_data.get('description', '')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Start Assessment →", key=f"start_{tree_id}", use_container_width=True):
                st.session_state.selected_tree = tree_id
                st.session_state.show_landing = False
                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    # Use Cases Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🎯 Who Is This For?</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='use-case-box'>
            <div class='use-case-title'>👨‍💼 For Auditors</div>
            <ul>
                <li>Standardize assessment approaches across teams</li>
                <li>Generate consistent, defensible decisions</li>
                <li>Produce audit-ready documentation instantly</li>
            </ul>
        </div>
        
        <div class='use-case-box'>
            <div class='use-case-title'>📊 For Risk Managers</div>
            <ul>
                <li>Classify vendors systematically</li>
                <li>Tier risks consistently across organization</li>
                <li>Document decision rationale clearly</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='use-case-box'>
            <div class='use-case-title'>✅ For Compliance Teams</div>
            <ul>
                <li>Determine regulatory requirements quickly</li>
                <li>Apply jurisdiction-specific rules accurately</li>
                <li>Maintain complete audit trails</li>
            </ul>
        </div>
        
        <div class='use-case-box'>
            <div class='use-case-title'>🛡️ For Security Teams</div>
            <ul>
                <li>Assess incident severity objectively</li>
                <li>Make reporting decisions confidently</li>
                <li>Document incident response choices</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class='cta-section'>
        <div class='cta-title'>Ready to Make Better Decisions?</div>
        <p style='font-size: 1.1rem; margin-bottom: 1.5rem; color: #1a1d2d;'>
            Join GRC professionals using DecisionGuide for consistent, defensible assessments
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class='custom-footer'>
        <p style='font-size: 1.1rem; margin-bottom: 0.5rem;'>
            <strong>DecisionGuide: Making structured, smart decisions—one at a time.</strong>
        </p>
        <p style='margin-bottom: 1rem; color: #cccccc;'>
            Built with empathy for students and professionals who need clarity in complex assessments.
        </p>
        <p>
            <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank'>
                ⭐ Star on GitHub
            </a>
            &nbsp;|&nbsp;
            <a href='https://github.com/Adeshola3/DecisionGuide/issues' target='_blank'>
                💬 Contribute
            </a>
        </p>
        <p style='margin-top: 1.5rem; font-size: 0.9rem; color: #666;'>
            Open source • MIT License • Made with 💙
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
        st.markdown(f"<div style='color: #00ffc6; font-size: 1.2rem; font-weight: 700; margin-bottom: 10px;'>📊 Question {current_question}</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        options = list(node["options"].keys())
        
        if node_id in answers:
            selected = answers[node_id]
        else:
            # Note: The custom radio button styling is applied globally via CSS
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
    # Pass path_so_far=[] to the initial call
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
        
        # Use custom markdown for result header
        st.markdown("<h3 style='color: #00ffc6;'>Result</h3>", unsafe_allow_html=True)
        st.markdown(f"**Decision code:** `{result['decision']}`")
        if result['explanation']:
            st.write(result['explanation'])

        # Use custom markdown for path header
        st.markdown("<h3 style='color: #00ffc6;'>Path Taken (Audit Trail)</h3>", unsafe_allow_html=True)
        # Use a bullet list with a custom icon for the path
        st.markdown("<div style='background: #232738; padding: 15px; border-radius: 8px;'>", unsafe_allow_html=True)
        for step in result['path']:
            st.markdown(f"<p style='margin-bottom: 5px; color: #cccccc;'>&nbsp;&nbsp;➡️ {step}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("<h3 style='color: #00ffc6;'>Export Options</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
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
            if st.button("🔄 Start over"):
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
