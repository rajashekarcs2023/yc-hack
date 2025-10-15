# 🎨 PixelPilot - Automated Frontend Development Workflow

[![Built with Dedalus](https://img.shields.io/badge/Built%20with-Dedalus-blue)](https://dedalus.ai)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **An intelligent multi-agent system that automates the entire frontend development lifecycle—from design specifications to deployed, tested applications.**

PixelPilot orchestrates four specialized AI agents that work together to extract specifications from Notion, generate production-ready Next.js code, deploy to Vercel, perform automated browser testing, and iterate based on feedback—all without human intervention.

---

## 🌟 Key Features

- **📝 Intelligent Specs Extraction** - Automatically reads and parses design specifications from Notion
- **🤖 Multi-API Code Generation** - Robust fallback chain (V0 → Claude → OpenAI) for reliable code generation
- **🚀 Automated Deployment** - Seamless integration with Vercel for instant production deployments
- **🧪 Browser Testing** - Automated visual and functional testing using Playwright MCP
- **🔄 Feedback Loop** - Continuous iteration based on test results written back to Notion
- **🛠️ Smart Error Fixing** - Automatic detection and resolution of common Next.js/Tailwind issues
- **📦 Dependency Management** - Intelligent package.json validation and dependency injection

---

## 🏗️ Architecture

PixelPilot consists of four specialized agents that form an automated development pipeline:

```
┌─────────────────────────────────────────────────────────────────┐
│                     PixelPilot Orchestrator                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
        │   Agent 1    │ │  Agent 2  │ │   Agent 3   │
        │   Specs +    │ │  Project  │ │   Browser   │
        │   Code Gen   │ │  Mgmt +   │ │   Testing   │
        │              │ │  Deploy   │ │             │
        └───────┬──────┘ └─────┬─────┘ └──────┬──────┘
                │               │               │
                └───────────────┼───────────────┘
                                │
                        ┌───────▼──────┐
                        │   Agent 4    │
                        │  Feedback &  │
                        │  Iteration   │
                        └──────────────┘
```

---

## 🤖 Agent System

### **Agent 1: Specs Extraction + Code Generation**
**File:** `agent1_specs_generation.py`

**Purpose:** Extracts design specifications from Notion and generates production-ready Next.js code.

**Key Capabilities:**
- Direct integration with Notion MCP for full specification extraction (1472+ characters)
- Multi-API fallback strategy for reliable code generation:
  - Primary: V0 API for Next.js components
  - Fallback 1: Claude API (Anthropic)
  - Fallback 2: OpenAI GPT-4
- Universal response parsing to handle different API output formats
- Complete project structure generation (components, pages, configs, styles)
- TypeScript + Tailwind CSS support out of the box

**Tools:**
- `extract_notion_specs()` - Fetches complete specifications from Notion
- `generate_v0_code()` - Primary code generation using V0 API
- `generate_claude_code()` - Fallback using Claude API
- `generate_openai_code()` - Secondary fallback using OpenAI

**Output:** Complete Next.js 14 project with TypeScript, Tailwind CSS, and all necessary configurations.

---

### **Agent 2: Project Management + Deployment**
**File:** `agent2_project_deployment.py`

**Purpose:** Manages dependencies, fixes errors, validates builds, and deploys to Vercel.

**Key Capabilities:**
- Automated dependency installation and validation
- Smart error detection and automatic fixing:
  - Missing Tailwind CSS dependencies
  - PostCSS configuration issues
  - Next.js configuration problems
  - Image hostname configuration
  - Client/Server component boundaries
- Production build testing before deployment
- Vercel CLI integration with public deployment flags
- Deployment URL extraction and validation

**Tools:**
- `install_dependencies()` - npm install with timeout handling
- `fix_project_errors()` - Runs automated error detection and fixing
- `test_dev_server()` - Validates production build
- `deploy_to_vercel()` - Deploys to Vercel and extracts deployment URL

**Integration:** Uses `automated_error_fixer.py` for comprehensive error detection and resolution.

**Output:** Live Vercel deployment URL with validated, production-ready application.

---

### **Agent 3: Browser Testing**
**File:** `agent3_browser_testing.py`

**Purpose:** Performs automated browser testing using Playwright to validate functionality and design.

**Key Capabilities:**
- Automated browser navigation using Playwright MCP
- Visual regression testing
- Functional testing of interactive elements
- Responsive design validation
- Screenshot capture for visual analysis
- Accessibility testing
- Performance metrics collection

**Tools:**
- `navigate_to_url()` - Opens deployment URL in browser
- `test_interactive_elements()` - Validates buttons, forms, interactions
- `capture_screenshot()` - Takes screenshots for visual testing
- `validate_responsive_design()` - Tests mobile/desktop layouts
- `check_accessibility()` - Runs accessibility audits

**Output:** Comprehensive test report with visual evidence and functional test results.

---

### **Agent 4: Feedback Iteration**
**File:** `agent4_feedback_iteration.py`

**Purpose:** Analyzes test results, writes feedback to Notion, and triggers iteration cycles.

**Key Capabilities:**
- Intelligent feedback analysis from test results
- Structured feedback writing to Notion document
- Issue prioritization and categorization
- Iteration trigger based on feedback severity
- Design deviation detection
- Functional bug identification
- Performance issue tracking

**Tools:**
- `analyze_test_results()` - Parses and categorizes test results
- `write_feedback_to_notion()` - Updates Notion with structured feedback
- `prioritize_issues()` - Ranks issues by severity
- `trigger_iteration()` - Initiates new development cycle if needed

**Output:** Updated Notion document with detailed feedback and iteration recommendations.

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required
- Python 3.12+
- Node.js 18+
- npm or yarn
- Vercel CLI (npm install -g vercel)

# API Keys
- Dedalus API Key
- Anthropic API Key (for Claude)
- OpenAI API Key
- Notion Integration Token
```

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/rajashekarcs2023/yc-hack.git
cd yc-hack
```

2. **Set up Python environment:**
```bash
python -m venv yc-venv
source yc-venv/bin/activate  # On Windows: yc-venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys:
# DEDALUS_API_KEY=your_dedalus_key
# ANTHROPIC_API_KEY=your_claude_key
# OPENAI_API_KEY=your_openai_key
# NOTION_API_TOKEN=your_notion_token
```

4. **Set up Notion MCP:**
```bash
# Configure your Notion page ID in the agent files
# Default page: pixelpilot specification document
```

### Running PixelPilot

**Full Orchestrated Workflow:**
```bash
python pixelpilot_orchestrator.py
```

**Individual Agents:**
```bash
# Agent 1: Specs + Code Generation
python agent1_specs_generation.py

# Agent 2: Deployment
python agent2_project_deployment.py pixelpilot-project

# Agent 3: Browser Testing
python agent3_browser_testing.py https://your-deployment-url.vercel.app

# Agent 4: Feedback Iteration
python agent4_feedback_iteration.py
```

---

## 📁 Project Structure

```
pixelpilot/
├── agent1_specs_generation.py      # Specs extraction + code generation
├── agent2_project_deployment.py    # Project management + deployment
├── agent3_browser_testing.py       # Browser testing with Playwright
├── agent4_feedback_iteration.py    # Feedback analysis + iteration
├── pixelpilot_orchestrator.py      # Main orchestration system
├── automated_error_fixer.py        # Smart error detection and fixing
├── dedalus_notion_tool.py          # Notion MCP integration
├── step1_test_notion_extraction.py # Notion extraction testing
├── requirements.txt                # Python dependencies
├── .env                            # Environment configuration
└── pixelpilot-project/             # Generated Next.js project
    ├── app/                        # Next.js app directory
    ├── components/                 # React components
    ├── styles/                     # CSS and Tailwind styles
    ├── package.json                # Node dependencies
    ├── tailwind.config.js          # Tailwind configuration
    └── tsconfig.json               # TypeScript configuration
```

---

## 🛠️ Technical Stack

### AI & Automation
- **[Dedalus](https://dedalus.ai)** - AI agent orchestration platform
- **Claude API** - Code generation and analysis
- **OpenAI GPT-4** - Fallback code generation
- **V0 by Vercel** - Next.js component generation

### Frontend
- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling

### DevOps & Testing
- **Vercel** - Deployment platform
- **Playwright** - Browser automation and testing
- **MCP (Model Context Protocol)** - Tool integration standard

### Integrations
- **Notion MCP** - Specification management
- **Browser MCP** - Automated testing

---

## 🔧 Configuration

### Notion Setup

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Share your specification page with the integration
3. Copy the page ID from the URL
4. Add credentials to `.env`

### Vercel Setup

1. Install Vercel CLI: `npm install -g vercel`
2. Login: `vercel login`
3. The agents will handle deployment automatically

### Automated Error Fixing

The system automatically detects and fixes:
- ✅ Missing Tailwind CSS dependencies
- ✅ PostCSS configuration issues
- ✅ Next.js image hostname configuration
- ✅ Turbopack compatibility issues
- ✅ Client/Server component boundaries
- ✅ Package.json validation

---

## 📊 Workflow Example

**Input (Notion):**
```markdown
# Profile Card Component Spec

Design Tokens:
- Card Background: #ffffff
- Border Radius: 12px
- Button Background: #2563eb
- Font: Inter, sans-serif

Responsive Behavior:
- ≥500px: Horizontal layout
- <500px: Vertical stack

Functional Requirements:
- Like button with counter
- Keyboard accessible
```

**Output (Deployed App):**
- ✅ Production Next.js app on Vercel
- ✅ Fully styled with Tailwind CSS
- ✅ TypeScript type safety
- ✅ Responsive design working
- ✅ Interactive functionality tested
- ✅ Feedback written to Notion

---

## 🤝 Contributing

We welcome contributions! This project was built during a hackathon and there's plenty of room for improvement.

**Areas for Enhancement:**
- OAuth support for Figma MCP integration
- Vision model support for design analysis
- More comprehensive test coverage
- Additional deployment platforms
- Enhanced error recovery strategies

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- **Dedalus Team** - For the amazing AI agent platform and hands-on debugging support
- **Anthropic** - For Claude API powering code generation
- **Vercel** - For seamless deployment infrastructure
- **Notion** - For MCP integration enabling specification management

---

## 📧 Contact

Built by Radhika Danda for YC Hackathon

**Project Link:** [https://github.com/rajashekarcs2023/yc-hack](https://github.com/rajashekarcs2023/yc-hack)

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ using [Dedalus](https://dedalus.ai)

</div>