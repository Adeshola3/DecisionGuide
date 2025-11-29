# DecisionGuide

**Open-source assessment tool for GRC professionals**

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://decisionguide.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**[Try it live →](https://decisionguide.streamlit.app)**

---

## 🎯 What is DecisionGuide?

DecisionGuide helps governance, risk, and compliance (GRC) professionals make **consistent, defensible decisions** through structured assessment logic.

**The Problem:**  
Risk and compliance teams often make inconsistent decisions because there's no standardized framework. Same vendor, different auditors, different outcomes.

**The Solution:**  
Research-backed assessment logic (ISO 27001, GDPR, NIST CSF) that guides not automates professional judgment.

### Why DecisionGuide?

✅ **Transparent logic** - See exactly how decisions are reached  
✅ **Zero-document approach** - No file uploads, no privacy risks  
✅ **Audit-ready exports** - PDF, JSON, and TXT formats with full decision trail  
✅ **Open source & extensible** - Add your own assessment frameworks  
✅ **Free forever** - No subscriptions, no paywalls  

---

## 🚀 Features

### Current Assessment Frameworks

- **DPIA Requirement Check** - Determine if Data Protection Impact Assessment is required (with jurisdiction-specific guidance for UK, EU, US, Nigeria)
- **Incident Reporting** - Decide whether security incidents require external reporting
- **Vendor Risk Tiering** - Classify vendors as Low, Medium, or High risk

### Core Capabilities

- 🎯 **Interactive decision trees** - Questions appear one at a time based on your answers
- 📊 **Full audit trail** - Complete path from questions to final decision
- 📄 **Professional exports** - Download results as PDF, JSON, or TXT
- 🔒 **Privacy-first** - All processing happens locally, no data collection
- 🌐 **Jurisdiction support** - Tailored guidance for different regulatory frameworks

---

## 📸 See It In Action

**[Try the live demo →](https://decisionguide.streamlit.app)** to see DecisionGuide in action!

---

### Assessment Flow
*Questions appear one at a time as you answer*

### Export Options
*Download professional audit-ready reports in multiple formats*

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** - Interactive web interface
- **ReportLab** - PDF generation
- **JSON** - Decision tree logic (easy to read and modify)

---

## 🚀 Quick Start

### Try Online (Easiest)

**[Launch DecisionGuide →](https://decisionguide.streamlit.app)**

No installation required!

### Run Locally

**1. Clone the repository:**
```bash
git clone https://github.com/Adeshola3/DecisionGuide.git
cd DecisionGuide
```

**2. Install dependencies:**

```bash
pip install -r requirements.txt
```

**3. Run the app:**

```bash
streamlit run app.py
```

**4. Open your browser:**
Visit `http://localhost:8501`

-----

## 📖 How It Works

### Decision Tree Structure

Each assessment is defined by a simple JSON file in the `logic/` folder:

```json
{
  "id": "vendor_risk",
  "title": "Vendor Risk Assessment",
  "description": "Assess vendor risk level",
  "root": "q1",
  "nodes": {
    "q1": {
      "type": "choice",
      "text": "Does vendor process sensitive data?",
      "options": {
        "Yes": {"next": "q2"},
        "No": {
          "decision": "LOW_RISK",
          "explanation": "No sensitive data processing."
        }
      }
    }
  }
}
```

**That’s it!** No Python coding required to add new assessments.

-----

## 🤝 Contributing

We welcome contributions! Here’s how you can help:

### Add a New Decision Tree

**Option 1: Code it yourself**

1. Create a new JSON file in `logic/` following the structure above
1. Test it locally with `streamlit run app.py`
1. Submit a pull request

**Option 2: Submit via form**
*(Coming soon)* Fill out our contribution form—no coding required!

## 🌟 Contribution Ideas

Here are practical ways you can contribute to DecisionGuide:

- 🌲 **Add new decision trees**  
  Examples: access reviews, encryption checks, DPIA deep-dive branches, data-retention logic, onboarding/offboarding checks, vendor risk workflows.  
  Just create a new JSON file under `/logic`.

- 🔧 **Refactor or enhance existing trees**  
  Improve clarity, strengthen logic, refine explanations, or map decisions more accurately to frameworks.

- 📚 **Improve documentation**  
  Add walkthroughs, examples, JSON schema explanations, or better guidance for contributors.

- 🐛 **Fix bugs or improve code quality**  
  Optimise the Python functions, improve error handling, simplify the decision engine, or enhance state management.

- 🎨 **UI/UX enhancements**  
  Better layout, improved spacing, summaries, breadcrumbs, multi-step navigation, or accessibility improvements.

- 🧪 **Add tests**  
  Create unit tests under `/tests` for tree traversal, JSON validation, and decision correctness.

- 🌍 **Jurisdiction-specific modules**  
  Add UK GDPR, EU GDPR, NDPR, HIPAA, CPRA, or industry-specific guidance displayed after a decision is reached.

- 🚀 **Feature contributions**  
  Enhanced export options, history tracking, evidence bundles, or integrations as the project evolves.

---

Feel free to open issues, submit PRs, or suggest improvements.  
Every contribution helps make DecisionGuide more useful to the GRC community!

### Guidelines

- Decision logic should reference established standards (ISO, NIST, GDPR, etc.)
- Keep questions clear and concise
- Provide actionable outcomes with explanations
- Test your changes before submitting

-----

## 🗺️ Roadmap

### ✅ Completed

- Interactive decision trees
- Session state persistence
- PDF/JSON/TXT export
- Jurisdiction-specific guidance
- 3 initial assessment frameworks

### 🔄 In Progress

- Contribution form for non-technical users
- Enhanced README and documentation

### 📋 Planned

- Progress indicators (Step X of Y)
- 15-20 assessment frameworks covering:
  - Cloud security assessments
  - Third-party risk management
  - Data classification
  - Access control reviews
  - Incident severity scoring
- Community contribution templates
- API for programmatic access

-----

## 💡 Use Cases

**For Auditors:**

- Standardize assessment approaches across team
- Generate consistent, defensible decisions
- Produce audit-ready documentation

**For Risk Managers:**

- Classify vendors systematically
- Tier risks consistently
- Document decision rationale

**For Compliance Teams:**

- Determine regulatory requirements (DPIA, breach notification, etc.)
- Apply jurisdiction-specific rules
- Maintain audit trails

**For Security Teams:**

- Assess incident severity
- Decide on reporting requirements
- Document incident response decisions

-----

## 🌟 Approach

DecisionGuide is built on three principles:

**1. Human-in-the-loop**  
We guide decisions, not automate them. Professional judgment remains central.

**2. Transparency**  
Every decision shows the full path taken. No black boxes.

**3. Accessibility**  
Free, open-source, and usable by anyone—from junior analysts to senior auditors.

-----

## 📄 License

This project is licensed under the MIT License - see the <LICENSE> file for details.

-----

## 🙏 Acknowledgments

Built with inspiration from:

- ISACA’s CISA framework
- ISO 27001/27002 standards
- NIST Cybersecurity Framework
- GDPR Article 35 (DPIA requirements)
- Real-world GRC challenges faced by practitioners

-----

## 📬 Contact & Feedback

- **Issues:** [GitHub Issues](https://github.com/Adeshola3/DecisionGuide/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Adeshola3/DecisionGuide/discussions)
- **Live Demo:** [decisionguide.streamlit.app](https://decisionguide.streamlit.app)

-----

## ⭐ Support the Project

If DecisionGuide helps your work, please:

- ⭐ Star this repository
- 🔗 Share with your network
- 🤝 Contribute a decision tree
- 💬 Provide feedback

-----

**DecisionGuide: Making structured, smart decisions-one at a time.**

Built with empathy for students and professionals who need clarity in complex assessments.💕

🚀 **[Start making better decisions →](https://decisionguide.streamlit.app)**

​​​​​​​