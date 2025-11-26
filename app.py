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

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom color scheme */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Hero section styling */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        opacity: 0.95;
    }
    
    .hero-description {
        font-size: 1.1rem;
        max-width: 700px;
        margin: 0 auto;
        opacity: 0.9;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #666;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Assessment cards */
    .assessment-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .assessment-card:hover {
        transform: translateY(-5px);
    }
    
    .assessment-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .assessment-description {
        font-size: 0.95rem;
        opacity: 0.9;
        flex-grow: 1;
    }
    
    /* Section styling */
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin: 3rem 0 2rem 0;
        color: #2d3748;
    }
    
    .section-subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }
    
    /* Use case boxes */
    .use-case-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .use-case-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    /* CTA section */
    .cta-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 3rem 0;
    }
    
    .cta-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        margin-top: 3rem;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
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
    """Display the colorful professional landing page"""
    
    # Hero Section
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>🎯 DecisionGuide</div>
        <div class='hero-subtitle'>Open-source assessment framework for GRC professionals</div>
        <div class='hero-description'>
            Make consistent, defensible decisions through structured logic flows. 
            Built with empathy for professionals who need clarity in complex assessments.
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
    
    # Create gradient colors for cards
    gradients = [
        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
    ]
    
    cols = st.columns(min(len(trees), 3))
    
    for idx, (tree_id, tree_data) in enumerate(trees.items()):
        with cols[idx % 3]:
            gradient = gradients[idx % len(gradients)]
            
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
        <p style='font-size: 1.1rem; margin-bottom: 1.5rem;'>
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
        <p style='margin-bottom: 1rem;'>
            Built with empathy for students and professionals who need clarity in complex assessments.
        </p>
        <p>
            <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank' 
               style='color: #667eea; text-decoration: none; font-weight: 600;'>
                ⭐ Star on GitHub
            </a>
            &nbsp;|&nbsp;
            <a href='https://github.com/Adeshola3/DecisionGuide/issues' target='_blank' 
               style='color: #667eea; text-decoration: none; font-weight: 600;'>
                💬 Contribute
            </a>
        </p>
        <p style='margin-top: 1.5rem; font-size: 0.9rem; color: #999;'>
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
        st.write(f"**Decision code:** {result['decision']}")
        if result['explanation']:
            st.write(result['explanation'])

        st.markdown("### Path taken")
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