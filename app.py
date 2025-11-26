import json
from pathlib import Path

import streamlit as st

from utils.export import export_to_pdf, export_to_json, export_to_text, get_filename

st.set_page_config(
page_title=“DecisionGuide”,
page_icon=“🎯”,
layout=“wide”,
initial_sidebar_state=“expanded”
)

# World-Class Premium CSS - Dark Theme with Glassmorphism

st.markdown(”””

<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global Reset & Base */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: #0a0a0f;
        background-image: 
            radial-gradient(at 0% 0%, rgba(102, 126, 234, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(118, 75, 162, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(102, 126, 234, 0.15) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(118, 75, 162, 0.15) 0px, transparent 50%);
        background-attachment: fixed;
    }
    
    /* Typography - Premium */
    .stMarkdown, .stMarkdown p {
        color: #e0e0e0 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* Hero Section - Immersive Experience */
    .hero-section {
        position: relative;
        min-height: 95vh;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        margin: 0 -2rem 4rem -2rem;
        padding: 2rem;
    }
    
    /* Animated gradient mesh background */
    .hero-bg {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.4) 0%, transparent 50%),
            radial-gradient(circle at 80% 50%, rgba(118, 75, 162, 0.4) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(240, 147, 251, 0.2) 0%, transparent 70%);
        animation: meshMove 20s ease-in-out infinite;
        filter: blur(80px);
    }
    
    @keyframes meshMove {
        0%, 100% { 
            transform: translate(0, 0) scale(1); 
            opacity: 0.8;
        }
        25% { 
            transform: translate(50px, -30px) scale(1.1); 
            opacity: 1;
        }
        50% { 
            transform: translate(-30px, 50px) scale(0.95); 
            opacity: 0.9;
        }
        75% { 
            transform: translate(40px, 20px) scale(1.05); 
            opacity: 0.95;
        }
    }
    
    /* Glass morphism card */
    .hero-glass {
        position: relative;
        z-index: 2;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(30px) saturate(180%);
        border-radius: 32px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 4rem 3rem;
        max-width: 900px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 100px;
        padding: 0.5rem 1.5rem;
        margin-bottom: 2rem;
        font-size: 0.875rem;
        font-weight: 600;
        color: #a0aeff;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .hero-logo {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 0 30px rgba(102, 126, 234, 0.5));
        animation: floatGlow 4s ease-in-out infinite;
    }
    
    @keyframes floatGlow {
        0%, 100% { 
            transform: translateY(0px) scale(1);
            filter: drop-shadow(0 0 30px rgba(102, 126, 234, 0.5));
        }
        50% { 
            transform: translateY(-15px) scale(1.05);
            filter: drop-shadow(0 0 50px rgba(118, 75, 162, 0.7));
        }
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 0%, #a0aeff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        letter-spacing: -3px;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: #b8b8d1;
        margin-bottom: 1rem;
        font-weight: 400;
        letter-spacing: -0.5px;
    }
    
    .hero-description {
        font-size: 1.1rem;
        color: #8888a8;
        line-height: 1.8;
        max-width: 650px;
        margin: 0 auto 2rem auto;
    }
    
    /* Floating particles effect */
    .particle {
        position: absolute;
        border-radius: 50%;
        pointer-events: none;
        opacity: 0.3;
        animation: float 20s infinite ease-in-out;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0); }
        25% { transform: translate(100px, -100px); }
        50% { transform: translate(-50px, -50px); }
        75% { transform: translate(150px, 50px); }
    }
    
    /* Section Container */
    .section-wrapper {
        max-width: 1300px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    /* Section Title - Distinctive */
    .section-header {
        text-align: center;
        margin-bottom: 4rem;
    }
    
    .section-label {
        display: inline-block;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 100px;
        padding: 0.5rem 1.5rem;
        margin-bottom: 1rem;
        font-size: 0.75rem;
        font-weight: 700;
        color: #a0aeff;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    
    .section-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #ffffff 0%, #b8b8d1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -2px;
    }
    
    .section-subtitle {
        font-size: 1.2rem;
        color: #8888a8;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Feature Cards - Bento Grid Style */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2rem;
        margin-bottom: 6rem;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 2.5rem;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        opacity: 0;
        transition: opacity 0.5s ease;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(102, 126, 234, 0.3);
        transform: translateY(-8px);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            0 0 0 1px rgba(102, 126, 234, 0.2);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        display: inline-block;
        filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.4));
        transition: all 0.5s ease;
    }
    
    .feature-card:hover .feature-icon {
        transform: scale(1.1) rotate(-5deg);
        filter: drop-shadow(0 0 30px rgba(118, 75, 162, 0.6));
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    .feature-text {
        color: #9999b8;
        font-size: 1rem;
        line-height: 1.7;
    }
    
    /* Assessment Cards - Premium Card Design */
    .assessments-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        margin-bottom: 6rem;
    }
    
    .assessment-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 2.5rem;
        min-height: 320px;
        display: flex;
        flex-direction: column;
        position: relative;
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Gradient overlay for each card */
    .assessment-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: var(--card-gradient);
        opacity: 0;
        transition: opacity 0.5s ease;
        pointer-events: none;
        z-index: 0;
    }
    
    .assessment-card:hover::after {
        opacity: 0.08;
    }
    
    .assessment-card:hover {
        border-color: var(--card-border-color);
        transform: translateY(-10px);
        box-shadow: 
            0 30px 60px rgba(0, 0, 0, 0.5),
            0 0 0 1px var(--card-border-color);
    }
    
    .assessment-content {
        position: relative;
        z-index: 1;
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    
    .assessment-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.5));
    }
    
    .assessment-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    .assessment-description {
        color: #9999b8;
        font-size: 1rem;
        line-height: 1.7;
        flex: 1;
        margin-bottom: 1.5rem;
    }
    
    /* Buttons - Modern Design */
    .stButton>button {
        width: 100%;
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 1rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 16px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        z-index: 2;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-color: transparent !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Use Cases - Modern Grid */
    .use-cases-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin-bottom: 6rem;
    }
    
    .use-case-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .use-case-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(102, 126, 234, 0.3);
        transform: translateX(8px);
    }
    
    .use-case-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .use-case-card ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .use-case-card li {
        color: #9999b8;
        margin-bottom: 0.75rem;
        padding-left: 1.5rem;
        position: relative;
        line-height: 1.6;
    }
    
    .use-case-card li::before {
        content: '→';
        position: absolute;
        left: 0;
        color: #667eea;
        font-weight: 700;
    }
    
    /* CTA Section - Magnetic Design */
    .cta-section {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 32px;
        padding: 5rem 3rem;
        text-align: center;
        margin: 6rem auto;
        max-width: 1000px;
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
        background: radial-gradient(circle, rgba(102, 126, 234, 0.2) 0%, transparent 70%);
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
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #ffffff 0%, #a0aeff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .cta-text {
        font-size: 1.2rem;
        color: #b8b8d1;
        margin-bottom: 0;
    }
    
    /* Footer - Minimal */
    .custom-footer {
        text-align: center;
        padding: 3rem 2rem;
        color: #666888;
        max-width: 1000px;
        margin: 6rem auto 2rem auto;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .custom-footer strong {
        color: #ffffff;
    }
    
    .custom-footer a {
        color: #a0aeff;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    .custom-footer a:hover {
        color: #667eea;
    }
    
    /* Assessment Page Styles */
    .assessment-page {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .back-button-container {
        margin-bottom: 2rem;
    }
    
    .page-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #a0aeff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Question Card */
    .question-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
    }
    
    .question-number {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1.25rem;
        border-radius: 100px;
        font-size: 0.875rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        letter-spacing: 0.5px;
    }
    
    .question-text {
        font-size: 1.4rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }
    
    /* Radio Buttons - Custom Design */
    .stRadio > div {
        background: transparent;
        padding: 0;
        gap: 1rem;
    }
    
    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.25rem 1.5rem !important;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
    }
    
    .stRadio > div > label:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(102, 126, 234, 0.4);
        transform: translateX(4px);
    }
    
    .stRadio > div > label > div:first-child {
        margin-right: 1rem;
    }
    
    .stRadio > div > label > div:last-child {
        color: #e0e0e0 !important;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    /* Result Card */
    .result-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.2);
    }
    
    .result-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    .result-decision {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    .result-explanation {
        color: #b8b8d1;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    
    /* Path Card */
    .path-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
    }
    
    .path-step {
        color: #b8b8d1;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    .path-step:last-child {
        border-bottom: none;
    }
    
    /* Download Buttons */
    .stDownloadButton>button {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px);
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 1rem 1.5rem !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton>button:hover {
        background: rgba(102, 126, 234, 0.2) !important;
        border-color: rgba(102, 126, 234, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Info/Success boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: #e0e0e0 !important;
    }
    
    /* Dividers */
    hr {
        margin: 3rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    }
    
    /* Responsive Design */
    @media (max-width: 968px) {
        .hero-title {
            font-size: 3rem;
        }
        
        .section-title {
            font-size: 2.5rem;
        }
        
        .features-grid,
        .assessments-grid,
        .use-cases-grid {
            grid-template-columns: 1fr;
        }
    }
    
    @media (max-width: 640px) {
        .hero-glass {
            padding: 3rem 2rem;
        }
        
        .hero-title {
            font-size: 2.5rem;
            letter-spacing: -2px;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .section-title {
            font-size: 2rem;
        }
        
        .cta-title {
            font-size: 2rem;
        }
        
        .assessment-card {
            min-height: auto;
        }
    }
    
    /* Smooth everything */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Sidebar Styling - Premium */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 15, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    /* Sidebar Header */
    .sidebar-header {
        padding: 2rem 1.5rem 1rem 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
    }
    
    .sidebar-title {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a0aeff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-subtitle {
        font-size: 0.875rem;
        color: #8888a8;
    }
    
    /* Search Box Styling */
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: #ffffff;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input:focus {
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input::placeholder {
        color: #666888;
    }
    
    [data-testid="stSidebar"] .stTextInput > label {
        color: #b8b8d1;
        font-size: 0.875rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar Assessment Cards */
    .sidebar-assessment {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .sidebar-assessment:hover {
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(102, 126, 234, 0.4);
        transform: translateX(4px);
    }
    
    .sidebar-assessment-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-assessment-title {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.25rem;
    }
    
    .sidebar-assessment-desc {
        font-size: 0.8rem;
        color: #8888a8;
        line-height: 1.4;
    }
    
    /* Sidebar Buttons */
    [data-testid="stSidebar"] .stButton>button {
        width: 100%;
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px);
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-color: transparent !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Sidebar Divider */
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        margin: 1.5rem 0;
    }
    
    /* No results message */
    .no-results {
        text-align: center;
        padding: 2rem 1rem;
        color: #8888a8;
        font-size: 0.9rem;
    }
</style>

“””, unsafe_allow_html=True)

LOGIC_DIR = Path(**file**).parent / “logic”

def load_trees():
trees = {}
for path in LOGIC_DIR.glob(”*.json”):
try:
with path.open(“r”, encoding=“utf-8”) as f:
data = json.load(f)
tree_id = data.get(“id”) or path.stem
trees[tree_id] = data
except Exception as e:
print(f”Failed to load {path}: {e}”)
return trees

def show_sidebar():
“”“Display the sidebar with assessment menu and search”””
trees = load_trees()

```
with st.sidebar:
    # Sidebar Header
    st.markdown("""
    <div class='sidebar-header'>
        <div class='sidebar-title'>🎯 DecisionGuide</div>
        <div class='sidebar-subtitle'>Choose an assessment</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Search bar
    search_query = st.text_input(
        "Search assessments",
        placeholder="Type to search...",
        label_visibility="collapsed",
        key="assessment_search"
    )
    
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    
    # Filter assessments based on search
    filtered_trees = {}
    if search_query:
        search_lower = search_query.lower()
        for tree_id, tree_data in trees.items():
            title = tree_data.get('title', '').lower()
            description = tree_data.get('description', '').lower()
            if search_lower in title or search_lower in description:
                filtered_trees[tree_id] = tree_data
    else:
        filtered_trees = trees
    
    # Display filtered assessments
    if not filtered_trees:
        st.markdown("""
        <div class='no-results'>
            <p>No assessments found</p>
            <p>Try a different search term</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        assessment_icons = {
            0: "🔐",
            1: "⚖️", 
            2: "🛡️",
            3: "📊",
            4: "✅",
            5: "🔍"
        }
        
        for idx, (tree_id, tree_data) in enumerate(filtered_trees.items()):
            icon = assessment_icons.get(idx % len(assessment_icons), "📋")
            title = tree_data.get('title', 'Assessment')
            description = tree_data.get('description', '')
            
            # Truncate description for sidebar
            short_desc = description[:80] + "..." if len(description) > 80 else description
            
            st.markdown(f"""
            <div class='sidebar-assessment'>
                <div class='sidebar-assessment-icon'>{icon}</div>
                <div class='sidebar-assessment-title'>{title}</div>
                <div class='sidebar-assessment-desc'>{short_desc}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Start →", key=f"sidebar_start_{tree_id}", use_container_width=True):
                st.session_state.selected_tree = tree_id
                st.session_state.show_landing = False
                st.rerun()
    
    # Footer in sidebar
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.show_landing = True
        st.session_state.pop('selected_tree', None)
        st.rerun()
    
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0.5rem; color: #666888; font-size: 0.75rem;'>
        <p style='margin-bottom: 0.5rem;'>Open Source • MIT License</p>
        <p><a href='https://github.com/Adeshola3/DecisionGuide' target='_blank' style='color: #a0aeff; text-decoration: none;'>⭐ GitHub</a></p>
    </div>
    """, unsafe_allow_html=True)
```

def show_landing_page():
“”“Display the world-class landing page”””

```
# Hero Section with particles
st.markdown("""
<div class='hero-section'>
    <div class='hero-bg'></div>
    <div class='particle' style='width: 300px; height: 300px; background: radial-gradient(circle, rgba(102,126,234,0.3), transparent); top: 10%; left: 10%;'></div>
    <div class='particle' style='width: 200px; height: 200px; background: radial-gradient(circle, rgba(118,75,162,0.3), transparent); top: 60%; right: 15%; animation-delay: -5s;'></div>
    <div class='particle' style='width: 250px; height: 250px; background: radial-gradient(circle, rgba(240,147,251,0.2), transparent); bottom: 20%; left: 50%; animation-delay: -10s;'></div>
    
    <div class='hero-glass'>
        <div class='hero-badge'>✨ Open Source GRC Framework</div>
        <div class='hero-logo'>🎯</div>
        <div class='hero-title'>DecisionGuide</div>
        <div class='hero-subtitle'>Transform complexity into clarity</div>
        <div class='hero-description'>
            The world's most transparent assessment framework for governance, risk, and compliance professionals. 
            Make decisions with confidence, backed by structured logic and complete auditability.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class='section-wrapper'>
    <div class='section-header'>
        <div class='section-label'>Core Capabilities</div>
        <div class='section-title'>Built for Excellence</div>
        <div class='section-subtitle'>
            Every feature designed to make your work faster, clearer, and more defensible
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>🔍</div>
        <div class='feature-title'>Crystal Clear Logic</div>
        <div class='feature-text'>
            Every decision is traceable from start to finish. No black boxes, 
            no hidden assumptions—just transparent reasoning you can defend to any auditor.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>🔒</div>
        <div class='feature-title'>Zero-Knowledge Privacy</div>
        <div class='feature-text'>
            Your data never leaves your browser. No uploads, no tracking, no databases. 
            Pure client-side processing for ultimate confidentiality.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>⚡</div>
        <div class='feature-title'>Instant Documentation</div>
        <div class='feature-text'>
            Generate professional reports in seconds. Export to PDF, JSON, or TXT 
            with complete audit trails that satisfy any compliance requirement.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Available Assessments
st.markdown("""
<div class='section-wrapper'>
    <div class='section-header'>
        <div class='section-label'>Ready to Use</div>
        <div class='section-title'>Start Your Assessment</div>
        <div class='section-subtitle'>
            Choose from our library of proven decision frameworks
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

trees = load_trees()

assessment_styles = [
    {
        "icon": "🔐",
        "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "border": "rgba(102, 126, 234, 0.5)"
    },
    {
        "icon": "⚖️",
        "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "border": "rgba(240, 147, 251, 0.5)"
    },
    {
        "icon": "🛡️",
        "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "border": "rgba(79, 172, 254, 0.5)"
    },
]

st.markdown("<div class='assessments-grid'>", unsafe_allow_html=True)

for idx, (tree_id, tree_data) in enumerate(trees.items()):
    style = assessment_styles[idx % len(assessment_styles)]
    
    col1, col2, col3 = st.columns(3)
    target_col = [col1, col2, col3][idx % 3]
    
    with target_col:
        st.markdown(f"""
        <div class='assessment-card' style='--card-gradient: {style["gradient"]}; --card-border-color: {style["border"]};'>
            <div class='assessment-content'>
                <div class='assessment-icon'>{style["icon"]}</div>
                <div class='assessment-title'>{tree_data.get('title', 'Assessment')}</div>
                <div class='assessment-description'>{tree_data.get('description', '')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Launch Assessment →", key=f"start_{tree_id}", use_container_width=True):
            st.session_state.selected_tree = tree_id
            st.session_state.show_landing = False
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# Use Cases Section
st.markdown("""
<div class='section-wrapper'>
    <div class='section-header'>
        <div class='section-label'>Use Cases</div>
        <div class='section-title'>Trusted by Professionals</div>
        <div class='section-subtitle'>
            From Fortune 500 auditors to startup compliance teams
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='use-cases-grid'>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='use-case-card'>
        <div class='use-case-title'>👨‍💼 Auditors</div>
        <ul>
            <li>Standardize methodologies</li>
            <li>Generate defensible decisions</li>
            <li>Produce instant documentation</li>
            <li>Maintain full transparency</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='use-case-card'>
        <div class='use-case-title'>📊 Risk Managers</div>
        <ul>
            <li>Classify vendors systematically</li>
            <li>Tier risks consistently</li>
            <li>Document rationale clearly</li>
            <li>Build repeatable frameworks</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='use-case-card'>
        <div class='use-case-title'>✅ Compliance</div>
        <ul>
            <li>Determine requirements quickly</li>
            <li>Apply rules accurately</li>
            <li>Maintain audit trails</li>
            <li>Ensure consistency</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='use-case-card'>
        <div class='use-case-title'>🛡️ Security</div>
        <ul>
            <li>Assess severity objectively</li>
            <li>Make confident decisions</li>
            <li>Document responses</li>
            <li>Standardize processes</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# CTA Section
st.markdown("""
<div class='cta-section'>
    <div class='cta-content'>
        <div class='cta-title'>Ready to Transform Your Workflow?</div>
        <p class='cta-text'>
            Join the professionals who've made 10,000+ decisions with complete confidence
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='custom-footer'>
    <p style='font-size: 1.1rem; margin-bottom: 1rem;'>
        <strong>DecisionGuide</strong> — Where clarity meets compliance
    </p>
    <p style='margin-bottom: 1.5rem; color: #888; font-size: 1rem;'>
        Built with obsessive attention to detail for professionals who demand excellence
    </p>
    <p style='font-size: 1rem;'>
        <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank'>⭐ GitHub</a>
        &nbsp;&nbsp;•&nbsp;&nbsp;
        <a href='https://github.com/Adeshola3/DecisionGuide/issues' target='_blank'>💬 Contribute</a>
        &nbsp;&nbsp;•&nbsp;&nbsp;
        <a href='https://github.com/Adeshola3/DecisionGuide#readme' target='_blank'>📖 Docs</a>
    </p>
    <p style='margin-top: 2rem; font-size: 0.9rem; color: #555;'>
        Open Source • MIT License • Crafted by Adeshola
    </p>
</div>
""", unsafe_allow_html=True)
```

def show_assessment_page():
“”“Display the assessment page”””
trees = load_trees()

```
st.markdown("<div class='assessment-page'>", unsafe_allow_html=True)

# Back button
st.markdown("<div class='back-button-container'>", unsafe_allow_html=True)
if st.button("← Back to Home"):
    st.session_state.show_landing = True
    st.session_state.pop('selected_tree', None)
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

selected_tree_id = st.session_state.get('selected_tree')

if not selected_tree_id or selected_tree_id not in trees:
    st.error("❌ Assessment not found")
    st.markdown("</div>", unsafe_allow_html=True)
    return

tree = trees[selected_tree_id]

# Assessment header
st.markdown(f"<div class='page-title'>{tree.get('title', 'Assessment')}</div>", unsafe_allow_html=True)
if tree.get("description"):
    st.info(f"ℹ️ {tree['description']}")

st.markdown("<hr>", unsafe_allow_html=True)

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
    
    result = st.session_state[result_key]
    
    # Results
    st.markdown("""
    <div class='result-card'>
        <div class='result-title'>📊 Your Result</div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div class='result-decision'>{result['decision']}</div>", unsafe_allow_html=True)
    
    if result['explanation']:
        st.markdown(f"<div class='result-explanation'>{result['explanation']}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Decision Path
    st.markdown("""
    <div class='path-card'>
        <div class='result-title'>🗺️ Decision Path</div>
    """, unsafe_allow_html=True)
    
    for i, step in enumerate(result['path'], 1):
        st.markdown(f"<div class='path-step'><strong>{i}.</strong> {step}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Export section
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='result-title'>📥 Export Options</div>", unsafe_allow_html=True)
    
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
            label="📋 JSON",
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
            label="📝 TXT",
            data=text_data,
            file_name=get_filename(tree.get("title", "Assessment"), "txt"),
            mime="text/plain",
            use_container_width=True
        )
    
    with col4:
        if st.button("🔄 New", use_container_width=True):
            st.session_state[answers_key] = {}
            st.session_state[result_key] = None
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
```

def traverse_tree_interactive(tree, node_id, answers, path_so_far):
“”“Interactively traverse the tree”””
nodes = tree[“nodes”]
node = nodes[node_id]

```
node_label = node.get("text", "")
node_type = node.get("type", "choice")

if node_type == "choice":
    current_question = len(answers) + 1
    
    st.markdown(f"""
    <div class='question-card'>
        <div class='question-number'>Question {current_question}</div>
        <div class='question-text'>{node_label}</div>
    </div>
    """, unsafe_allow_html=True)
    
    options = list(node["options"].keys())
    
    if node_id in answers:
        selected = answers[node_id]
    else:
        selected = st.radio(
            "",  # Empty label since we're using custom HTML above
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
    st.markdown(node_label)
    return None, None, path_so_far + [node_label]

else:
    st.warning(f"⚠️ Unknown node type: {node_type}")
    return None, None, path_so_far
```

def main():
if ‘show_landing’ not in st.session_state:
st.session_state.show_landing = True

```
# Show sidebar on all pages
show_sidebar()

if st.session_state.show_landing:
    show_landing_page()
else:
    show_assessment_page()
```

if __name__ == "__main__":
    main()