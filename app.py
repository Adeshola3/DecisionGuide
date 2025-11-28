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

# Premium, cutting-edge CSS design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global Reset & Base Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: #0a0a0a;
        color: #ffffff;
    }
    
    /* Typography - Bold & Clear */
    .stMarkdown, .stMarkdown p, .stMarkdown li {
        color: #e0e0e0 !important;
        line-height: 1.7;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* ============================================ */
    /* HERO SECTION - DRAMATIC & BOLD */
    /* ============================================ */
    
    .hero-wrapper {
        position: relative;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        margin: -2rem -2rem 0 -2rem;
        padding: 2rem;
    }
    
    /* Animated Gradient Background */
    .hero-wrapper::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(236, 72, 153, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(59, 130, 246, 0.2) 0%, transparent 50%);
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { opacity: 1; transform: scale(1) rotate(0deg); }
        50% { opacity: 0.8; transform: scale(1.1) rotate(5deg); }
    }
    
    /* Grid Pattern Overlay */
    .hero-wrapper::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
    }
    
    .hero-content {
        position: relative;
        z-index: 10;
        text-align: center;
        max-width: 1000px;
    }
    
    .hero-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 2rem;
        color: #ffffff;
        animation: fadeInUp 0.8s ease;
    }
    
    .hero-title {
        font-size: 7rem;
        font-weight: 900;
        line-height: 1.1;
        letter-spacing: -4px;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: fadeInUp 0.8s ease 0.2s backwards;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #b4b4b4;
        margin-bottom: 2.5rem;
        font-weight: 400;
        line-height: 1.6;
        animation: fadeInUp 0.8s ease 0.4s backwards;
    }
    
    .hero-cta-group {
        display: flex;
        gap: 1rem;
        justify-content: center;
        animation: fadeInUp 0.8s ease 0.6s backwards;
        flex-wrap: wrap;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Scroll Indicator */
    .scroll-indicator {
        position: absolute;
        bottom: 3rem;
        left: 50%;
        transform: translateX(-50%);
        animation: bounce 2s infinite;
        color: rgba(255, 255, 255, 0.5);
        font-size: 2rem;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateX(-50%) translateY(0); }
        50% { transform: translateX(-50%) translateY(10px); }
    }
    
    /* ============================================ */
    /* FEATURE CARDS - GLASS MORPHISM DESIGN */
    /* ============================================ */
    
    .features-section {
        padding: 8rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .section-header {
        text-align: center;
        margin-bottom: 5rem;
    }
    
    .section-label {
        display: inline-block;
        padding: 0.5rem 1.25rem;
        background: rgba(167, 139, 250, 0.1);
        border: 1px solid rgba(167, 139, 250, 0.3);
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #a78bfa;
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-description {
        font-size: 1.25rem;
        color: #b4b4b4;
        max-width: 700px;
        margin: 0 auto;
    }
    
    .feature-card {
        position: relative;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-color), transparent);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        border-color: rgba(255, 255, 255, 0.2);
        background: rgba(255, 255, 255, 0.05);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            0 0 100px rgba(167, 139, 250, 0.1);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-icon-wrapper {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary));
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
        font-size: 2rem;
        transition: transform 0.4s ease;
    }
    
    .feature-card:hover .feature-icon-wrapper {
        transform: scale(1.1) rotate(5deg);
    }
    
    .feature-title {
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #ffffff;
    }
    
    .feature-description {
        color: #b4b4b4;
        font-size: 1.05rem;
        line-height: 1.7;
    }
    
    /* ============================================ */
    /* ASSESSMENT CARDS - DYNAMIC DESIGN */
    /* ============================================ */
    
    .assessments-section {
        padding: 8rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .assessment-card {
        position: relative;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 3rem;
        height: 350px;
        display: flex;
        flex-direction: column;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
        margin-bottom: 2rem;
    }
    
    .assessment-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: var(--card-gradient);
        opacity: 0;
        transition: opacity 0.4s ease;
        z-index: 0;
    }
    
    .assessment-card:hover::before {
        opacity: 0.1;
    }
    
    .assessment-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5);
    }
    
    .assessment-content {
        position: relative;
        z-index: 1;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }
    
    .assessment-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        filter: grayscale(0.3);
        transition: all 0.4s ease;
    }
    
    .assessment-card:hover .assessment-icon {
        filter: grayscale(0);
        transform: scale(1.1);
    }
    
    .assessment-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #ffffff;
    }
    
    .assessment-description {
        color: #b4b4b4;
        font-size: 1.05rem;
        line-height: 1.7;
        flex-grow: 1;
    }
    
    /* ============================================ */
    /* USE CASES - MODERN LAYOUT */
    /* ============================================ */
    
    .use-cases-section {
        padding: 8rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .use-case-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .use-case-card:hover {
        transform: translateX(10px);
        border-color: var(--accent-color);
        background: rgba(255, 255, 255, 0.05);
    }
    
    .use-case-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .use-case-icon {
        font-size: 2rem;
    }
    
    .use-case-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    .use-case-card ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .use-case-card li {
        color: #b4b4b4;
        padding-left: 2rem;
        margin-bottom: 1rem;
        position: relative;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    .use-case-card li::before {
        content: '→';
        position: absolute;
        left: 0;
        color: var(--accent-color);
        font-weight: bold;
    }
    
    /* ============================================ */
    /* CTA SECTION - BOLD & ATTENTION GRABBING */
    /* ============================================ */
    
    .cta-section {
        margin: 8rem auto;
        max-width: 1200px;
        padding: 6rem 3rem;
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 32px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .cta-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(167, 139, 250, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .cta-content {
        position: relative;
        z-index: 1;
    }
    
    .cta-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .cta-description {
        font-size: 1.25rem;
        color: #b4b4b4;
        margin-bottom: 2.5rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* ============================================ */
    /* BUTTONS - PREMIUM DESIGN */
    /* ============================================ */
    
    .stButton>button {
        background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 10px 30px rgba(167, 139, 250, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(167, 139, 250, 0.5) !important;
    }
    
    .stButton>button:active {
        transform: translateY(0) scale(0.98) !important;
    }
    
    /* Download Buttons */
    .stDownloadButton>button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 0.875rem 1.75rem !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stDownloadButton>button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* ============================================ */
    /* ASSESSMENT PAGE */
    /* ============================================ */
    
    .assessment-page-wrapper {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .question-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
    }
    
    .question-number {
        display: inline-block;
        background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%);
        color: white;
        padding: 0.5rem 1.25rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        letter-spacing: 1px;
    }
    
    /* Radio Buttons - Custom Design */
    .stRadio > div {
        background: transparent !important;
        padding: 0 !important;
        gap: 1rem !important;
    }
    
    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 1.25rem 1.5rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        margin-bottom: 0.75rem !important;
    }
    
    .stRadio > div > label:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(167, 139, 250, 0.5) !important;
        transform: translateX(5px) !important;
    }
    
    .stRadio > div > label > div {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
    }
    
    .stRadio label span {
        color: #ffffff !important;
    }
    
    /* Result Card */
    .result-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
    }
    
    .result-badge {
        display: inline-block;
        background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }
    
    /* Path Steps */
    .path-step {
        background: rgba(255, 255, 255, 0.03);
        border-left: 3px solid #a78bfa;
        padding: 1rem 1.5rem;
        margin-bottom: 0.75rem;
        border-radius: 0 8px 8px 0;
        color: #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .path-step:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateX(5px);
    }
    
    /* Info/Alert Boxes */
    .stAlert {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        color: #60a5fa !important;
    }
    
    div[data-baseweb="notification"] {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Success Message */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 12px !important;
        color: #34d399 !important;
    }
    
    /* Footer */
    .footer-section {
        text-align: center;
        padding: 4rem 2rem;
        margin-top: 8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .footer-section a {
        color: #a78bfa;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    .footer-section a:hover {
        color: #ec4899;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        margin: 3rem 0;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 3.5rem;
            letter-spacing: -2px;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .section-title {
            font-size: 2.5rem;
        }
        
        .feature-card,
        .assessment-card,
        .use-case-card {
            margin-bottom: 1.5rem;
        }
        
        .cta-title {
            font-size: 2.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .section-title {
            font-size: 2rem;
        }
    }
    
    /* Smooth Animations */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
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
    """Premium landing page design"""
    
    # Hero Section - Dramatic entrance
    st.markdown("""
    <div class='hero-wrapper'>
        <div class='hero-content'>
            <div class='hero-badge'>🎯 Open Source GRC Framework</div>
            <h1 class='hero-title'>DecisionGuide</h1>
            <p class='hero-subtitle'>
                Make consistent, defensible decisions through structured logic flows.<br>
                Built for GRC professionals who demand clarity in complex assessments.
            </p>
        </div>
        <div class='scroll-indicator'>↓</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section with glass morphism
    st.markdown("""
    <div class='features-section'>
        <div class='section-header'>
            <span class='section-label'>Why Choose DecisionGuide</span>
            <h2 class='section-title'>Built for Excellence</h2>
            <p class='section-description'>
                Every feature designed to make your assessment workflow seamless and professional
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card' style='--accent-color: #a78bfa; --accent-secondary: #ec4899;'>
            <div class='feature-icon-wrapper'>🔍</div>
            <h3 class='feature-title'>Crystal Clear Logic</h3>
            <p class='feature-description'>
                Every decision is traced step-by-step. No black boxes, no mysteries; just transparent, 
                defensible reasoning you can confidently present to stakeholders.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card' style='--accent-color: #ec4899; --accent-secondary: #a78bfa;'>
            <div class='feature-icon-wrapper'>🔒</div>
            <h3 class='feature-title'>Zero-Trust Privacy</h3>
            <p class='feature-description'>
                No file uploads. No data collection. No servers. Everything runs in your browser. 
                Your sensitive assessments stay exactly where they should—with you.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card' style='--accent-color: #3b82f6; --accent-secondary: #8b5cf6;'>
            <div class='feature-icon-wrapper'>📄</div>
            <h3 class='feature-title'>Audit-Grade Reports</h3>
            <p class='feature-description'>
                Export to PDF, JSON, or TXT with complete decision trails. Built for compliance, 
                designed for auditors, ready for any review or certification process.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Assessments Section
    st.markdown("""
    <div class='assessments-section'>
        <div class='section-header'>
            <span class='section-label'>Get Started</span>
            <h2 class='section-title'>Available Assessments</h2>
            <p class='section-description'>
                Choose an assessment to begin your structured decision-making process
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    trees = load_trees()
    
    assessment_configs = [
        {
            "icon": "🔐",
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "color": "#a78bfa"
        },
        {
            "icon": "⚖️",
            "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            "color": "#ec4899"
        },
        {
            "icon": "🛡️",
            "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            "color": "#3b82f6"
        },
    ]
    
    cols = st.columns(min(len(trees), 3))
    
    for idx, (tree_id, tree_data) in enumerate(trees.items()):
        with cols[idx % 3]:
            config = assessment_configs[idx % len(assessment_configs)]
            
            st.markdown(f"""
            <div class='assessment-card' style='--card-gradient: {config["gradient"]}; --accent-color: {config["color"]};'>
                <div class='assessment-content'>
                    <div class='assessment-icon'>{config["icon"]}</div>
                    <h3 class='assessment-title'>{tree_data.get('title', 'Assessment')}</h3>
                    <p class='assessment-description'>{tree_data.get('description', '')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Start Assessment →", key=f"start_{tree_id}", use_container_width=True):
                st.session_state.selected_tree = tree_id
                st.session_state.show_landing = False
                st.rerun()
    
    # Use Cases Section
    st.markdown("""
    <div class='use-cases-section'>
        <div class='section-header'>
            <span class='section-label'>Use Cases</span>
            <h2 class='section-title'>Who Benefits?</h2>
            <p class='section-description'>
                Built for professionals who need consistent, defensible decision-making
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='use-case-card' style='--accent-color: #a78bfa;'>
            <div class='use-case-header'>
                <span class='use-case-icon'>👨‍💼</span>
                <h3 class='use-case-title'>Auditors</h3>
            </div>
            <ul>
                <li>Standardise assessment methodology across teams</li>
                <li>Generate consistent, repeatable audit decisions</li>
                <li>Document complete reasoning for findings</li>
                <li>Produce audit-ready evidence instantly</li>
            </ul>
        </div>
        
        <div class='use-case-card' style='--accent-color: #ec4899;'>
            <div class='use-case-header'>
                <span class='use-case-icon'>📊</span>
                <h3 class='use-case-title'>Risk Managers</h3>
            </div>
            <ul>
                <li>Classify vendors with objective criteria</li>
                <li>Apply risk tiers systematically</li>
                <li>Track decision rationale over time</li>
                <li>Ensure consistency in risk assessments</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='use-case-card' style='--accent-color: #3b82f6;'>
            <div class='use-case-header'>
                <span class='use-case-icon'>✅</span>
                <h3 class='use-case-title'>Compliance Teams</h3>
            </div>
            <ul>
                <li>Map requirements to regulations accurately</li>
                <li>Apply jurisdiction rules consistently</li>
                <li>Maintain complete compliance audit trails</li>
                <li>Demonstrate due diligence to regulators</li>
            </ul>
        </div>
        
        <div class='use-case-card' style='--accent-color: #8b5cf6;'>
            <div class='use-case-header'>
                <span class='use-case-icon'>🛡️</span>
                <h3 class='use-case-title'>Security Teams</h3>
            </div>
            <ul>
                <li>Rate incident severity objectively</li>
                <li>Make reporting decisions with confidence</li>
                <li>Document security response choices</li>
                <li>Standardise threat classification</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class='cta-section'>
        <div class='cta-content'>
            <h2 class='cta-title'>Ready to Transform Your Decisions?</h2>
            <p class='cta-description'>
                Join forward-thinking GRC professionals using DecisionGuide for consistent, 
                defensible, and transparent assessments that stand up to scrutiny.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class='footer-section'>
        <p style='font-size: 1.25rem; margin-bottom: 1rem; font-weight: 600;'>
            DecisionGuide: Making structured, smart decisions—one at a time.
        </p>
        <p style='margin-bottom: 2rem; color: #b4b4b4;'>
            Built with empathy for students and professionals who need clarity in complex assessments.
        </p>
        <p style='font-size: 1.05rem;'>
            <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank'>⭐ Star on GitHub</a>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <a href='https://github.com/Adeshola3/DecisionGuide/issues' target='_blank'>💬 Contribute</a>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <a href='https://github.com/Adeshola3/DecisionGuide#readme' target='_blank'>📖 Documentation</a>
        </p>
        <p style='margin-top: 2.5rem; font-size: 0.95rem; color: #6b7280;'>
            Open source • MIT License • Made with 💙 by Adeshola
        </p>
    </div>
    """, unsafe_allow_html=True)


def show_assessment_page():
    """Premium assessment page design"""
    trees = load_trees()
    
    st.markdown("<div class='assessment-page-wrapper'>", unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Home", key="back_btn"):
        st.session_state.show_landing = True
        st.session_state.pop('selected_tree', None)
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    selected_tree_id = st.session_state.get('selected_tree')
    
    if not selected_tree_id or selected_tree_id not in trees:
        st.error("❌ Assessment not found")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    tree = trees[selected_tree_id]
    
    # Assessment header
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h1 style='font-size: 3rem; margin-bottom: 1rem;'>{tree.get('title', 'Assessment')}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if tree.get("description"):
        st.info(f"ℹ️ {tree['description']}")
    
    st.markdown("<br>", unsafe_allow_html=True)

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
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        result = st.session_state[result_key]
        
        # Result Display
        st.markdown(f"""
        <div class='result-card'>
            <span class='result-badge'>Final Decision</span>
            <h3 style='font-size: 1.75rem; margin-bottom: 1rem; color: #ffffff;'>{result['decision']}</h3>
            {f"<p style='color: #b4b4b4; font-size: 1.05rem; line-height: 1.7;'>{result['explanation']}</p>" if result['explanation'] else ""}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🗺️ Decision Path")
        st.markdown("<div style='background: rgba(255, 255, 255, 0.03); padding: 2rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);'>", unsafe_allow_html=True)
        for i, step in enumerate(result['path'], 1):
            st.markdown(f"<div class='path-step'><strong>{i}.</strong> {step}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 📥 Export Your Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pdf_buffer = export_to_pdf(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📄 PDF Report",
                data=pdf_buffer,
                file_name=get_filename(tree.get("title", "Assessment"), "pdf"),
                mime="application/pdf",
                use_container_width=True
            )
        
        with col2:
            json_data = export_to_json(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📋 JSON Data",
                data=json_data,
                file_name=get_filename(tree.get("title", "Assessment"), "json"),
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            text_data = export_to_text(
                tree.get("title", "Assessment"),
                result['decision'],
                result['explanation'],
                result['path']
            )
            st.download_button(
                label="📝 Text File",
                data=text_data,
                file_name=get_filename(tree.get("title", "Assessment"), "txt"),
                mime="text/plain",
                use_container_width=True
            )
        
        with col4:
            if st.button("🔄 New Assessment", use_container_width=True):
                st.session_state[answers_key] = {}
                st.session_state[result_key] = None
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)


def traverse_tree_interactive(tree, node_id, answers, path_so_far):
    """Interactively traverse the tree"""
    nodes = tree["nodes"]
    node = nodes[node_id]
    
    node_label = node.get("text", "")
    node_type = node.get("type", "choice")
    
    if node_type == "choice":
        current_question = len(answers) + 1
        
        st.markdown(f"""
        <div class='question-card'>
            <span class='question-number'>Question {current_question}</span>
            <h3 style='font-size: 1.5rem; color: #ffffff; margin-bottom: 1.5rem;'>{node_label}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        options = list(node["options"].keys())
        
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
        st.markdown(f"<p style='color: #e0e0e0;'>{node_label}</p>", unsafe_allow_html=True)
        return None, None, path_so_far + [node_label]
    
    else:
        st.warning(f"⚠️ Unknown node type: {node_type}")
        return None, None, path_so_far


def main():
    if 'show_landing' not in st.session_state:
        st.session_state.show_landing = True
    
    if st.session_state.show_landing:
        show_landing_page()
    else:
        show_assessment_page()


if __name__ == "__main__":
    main()