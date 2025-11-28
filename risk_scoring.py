# risk_scoring.py

# Place this file in the same directory as app.py

import streamlit as st

class RiskScorer:
“”“Handles risk scoring calculations for decision trees”””

```
def __init__(self, tree_data):
    self.tree_data = tree_data
    self.scoring_config = tree_data.get('scoring', {})
    self.thresholds = self.scoring_config.get('thresholds', {
        'low': 0,
        'medium': 30,
        'high': 60,
        'critical': 85
    })

def calculate_score(self, answers):
    """
    Calculate cumulative risk score from all answers
    
    Args:
        answers: List of dicts with 'node_id' and 'choice' keys
        
    Returns:
        int: Risk score between 0-100
    """
    total_score = 0
    
    for answer in answers:
        node_id = answer.get('node_id')
        choice = answer.get('choice')
        
        # Get the node from tree data
        node = self.tree_data['nodes'].get(node_id)
        
        if node and 'options' in node:
            option_data = node['options'].get(choice)
            
            # Add risk weight if it exists
            if option_data and 'risk_weight' in option_data:
                total_score += option_data['risk_weight']
    
    # Ensure score stays within 0-100 range
    return max(0, min(100, total_score))

def get_risk_level(self, score):
    """
    Determine risk level based on score and thresholds
    
    Args:
        score: int between 0-100
        
    Returns:
        tuple: (risk_level_string, emoji_icon, color)
    """
    if score >= self.thresholds['critical']:
        return "CRITICAL", "🔴", "red"
    elif score >= self.thresholds['high']:
        return "HIGH RISK", "🟠", "orange"
    elif score >= self.thresholds['medium']:
        return "MEDIUM RISK", "🟡", "yellow"
    else:
        return "LOW RISK", "🟢", "green"

def get_risk_details(self, score):
    """
    Get detailed risk assessment with recommendations
    
    Args:
        score: int between 0-100
        
    Returns:
        dict: Risk details including level, recommendations, and priority
    """
    level, icon, color = self.get_risk_level(score)
    
    recommendations = {
        "CRITICAL": {
            "priority": "IMMEDIATE",
            "action": "Requires immediate remediation and management attention",
            "timeline": "Address within 24-48 hours",
            "escalation": "Escalate to senior management"
        },
        "HIGH RISK": {
            "priority": "HIGH",
            "action": "Requires prompt attention and mitigation plan",
            "timeline": "Address within 1-2 weeks",
            "escalation": "Notify risk owner and management"
        },
        "MEDIUM RISK": {
            "priority": "MEDIUM",
            "action": "Develop mitigation plan and monitor regularly",
            "timeline": "Address within 1-3 months",
            "escalation": "Document and track in risk register"
        },
        "LOW RISK": {
            "priority": "LOW",
            "action": "Standard monitoring and periodic review",
            "timeline": "Review quarterly",
            "escalation": "Standard documentation"
        }
    }
    
    return {
        "score": score,
        "level": level,
        "icon": icon,
        "color": color,
        "recommendation": recommendations.get(level, recommendations["LOW RISK"])
    }

def get_score_breakdown(self, answers):
    """
    Get detailed breakdown of how score was calculated
    
    Args:
        answers: List of answer dicts
        
    Returns:
        list: Breakdown of each answer's contribution to score
    """
    breakdown = []
    
    for answer in answers:
        node_id = answer.get('node_id')
        choice = answer.get('choice')
        
        node = self.tree_data['nodes'].get(node_id)
        
        if node and 'options' in node:
            option_data = node['options'].get(choice)
            risk_weight = option_data.get('risk_weight', 0) if option_data else 0
            
            breakdown.append({
                'question': node.get('text', 'Unknown question'),
                'answer': choice,
                'risk_weight': risk_weight,
                'impact': 'Increases risk' if risk_weight > 0 else 'Decreases risk' if risk_weight < 0 else 'Neutral'
            })
    
    return breakdown
```

def display_current_risk_score(scorer, answers):
“”“Display current risk score in Streamlit sidebar”””
if not answers:
return

```
score = scorer.calculate_score(answers)
level, icon, color = scorer.get_risk_level(score)

st.sidebar.markdown("### 📊 Current Risk Assessment")
st.sidebar.metric(
    label="Risk Score",
    value=f"{score}/100"
)
st.sidebar.markdown(f"{icon} **{level}**")

# Progress bar colored by risk level
if color == "red":
    st.sidebar.error(f"Current Score: {score}/100")
elif color == "orange":
    st.sidebar.warning(f"Current Score: {score}/100")
elif color == "yellow":
    st.sidebar.info(f"Current Score: {score}/100")
else:
    st.sidebar.success(f"Current Score: {score}/100")
```

def display_final_risk_report(scorer, answers):
“”“Display comprehensive final risk report”””
score = scorer.calculate_score(answers)
risk_details = scorer.get_risk_details(score)
breakdown = scorer.get_score_breakdown(answers)

```
st.markdown("---")
st.markdown("## 📊 Risk Assessment Report")

# Risk score summary
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Risk Score", f"{score}/100")

with col2:
    st.metric("Risk Level", risk_details['level'])

with col3:
    st.metric("Priority", risk_details['recommendation']['priority'])

# Risk level indicator with color
st.markdown(f"### {risk_details['icon']} {risk_details['level']}")

# Alert based on severity
if risk_details['level'] == "CRITICAL":
    st.error("⚠️ **CRITICAL RISK IDENTIFIED** - Immediate action required")
elif risk_details['level'] == "HIGH RISK":
    st.warning("⚠️ **HIGH RISK** - Prompt attention needed")
elif risk_details['level'] == "MEDIUM RISK":
    st.info("ℹ️ **MEDIUM RISK** - Monitor and plan mitigation")
else:
    st.success("✅ **LOW RISK** - Continue standard monitoring")

# Recommendations
st.markdown("### 📋 Recommended Actions")
rec = risk_details['recommendation']

st.write(f"**Action Required:** {rec['action']}")
st.write(f"**Timeline:** {rec['timeline']}")
st.write(f"**Escalation:** {rec['escalation']}")

# Score breakdown
with st.expander("📊 View Detailed Score Breakdown"):
    st.markdown("#### How Your Score Was Calculated")
    
    for item in breakdown:
        risk_weight = item['risk_weight']
        
        if risk_weight > 0:
            st.markdown(f"**{item['question']}**")
            st.markdown(f"- Answer: {item['answer']}")
            st.markdown(f"- Impact: +{risk_weight} points ⬆️ (Increases risk)")
        elif risk_weight < 0:
            st.markdown(f"**{item['question']}**")
            st.markdown(f"- Answer: {item['answer']}")
            st.markdown(f"- Impact: {risk_weight} points ⬇️ (Decreases risk)")
        else:
            st.markdown(f"**{item['question']}**")
            st.markdown(f"- Answer: {item['answer']}")
            st.markdown(f"- Impact: {risk_weight} points ➡️ (Neutral)")
        
        st.markdown("---")
    
    st.markdown(f"**Total Risk Score: {score}/100**")
```