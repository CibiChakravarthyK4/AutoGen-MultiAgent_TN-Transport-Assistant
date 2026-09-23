# AutoGen-MultiAgent_TN-Transport-Assistant

# 🚌 Tamil Nadu Public Transport Assistant

A **Multi-Agent AI-powered public transport assistant** built with python, Streamlit, AutoGen, and OpenAI to generate structured travel guidance across MTC, TNSTC, and SETC services in Tamil Nadu.

The application uses multiple specialized AI agents in a **sequential workflow**. Each agent focuses on a specific part of the journey-planning process and passes its output to the next agent.

## 🚀 Features
-   🚌 Route and schedule analysis
-   👥 Crowd and traffic prediction
-   💡 Alternative commute suggestions
-   🎯 Final consolidated travel advisory
-   🔎 Live web search using SerperDev
-   🤖 Multi-agent workflow using AutoGen
-   🖥️ Interactive Streamlit dashboard
-   📊 Step-by-step agent execution status
-   📑 Tabbed output for route, crowd, advisory, and final guide

## 🧠 Multi-Agent Architecture
The application uses four specialized AutoGen `AssistantAgent`instances:

### 1. 🚌 Route & Schedule Agent

Identifies relevant transport routes, boarding points, and approximate schedules for the selected transport corporation.

**Tool:** SerperDev web search

### 2. 👥 Crowd & Traffic Analyst Agent

Analyzes the journey context, travel time, peak hours, congestion, expected crowd levels, and seating availability.

### 3. 💡 Commute Advisor Agent

Uses the route and crowd analysis to suggest alternative travel timings, less-crowded options, and multi-modal travel strategies.

### 4. 🎯 Transport Guide Agent

Combines the preceding analysis and produces a clean, structured final travel advisory for the Streamlit dashboard.

## 🔄 Sequential Workflow

``` text
User Input
   │
   ├── Transport Corporation
   ├── Starting Point
   ├── Destination
   └── Expected Travel Time
            │
            ▼
   🚌 Route & Schedule Agent
            │
            ▼
   👥 Crowd & Traffic Agent
            │
            ▼
   💡 Commute Advisor Agent
            │
            ▼
   🎯 Transport Guide Agent
            │
            ▼
      Final Travel Advisory
```

The workflow passes each agent's output to the next agent:

``` text
Route Analysis
      ↓
Crowd Analysis
      ↓
Commute Optimization
      ↓
Final Travel Guide
```

## 🛠️ Technologies & Concepts Used

-   **Python** -- Core application development
-   **Streamlit** -- Interactive web application and dashboard
-   **AutoGen AgentChat** -- Multi-agent framework
-   **AssistantAgent** -- Specialized AI agents
-   **OpenAIChatCompletionClient** -- OpenAI model integration
-   **GPT-4o-mini** -- LLM used by the agents
-   **FunctionTool** -- Integrates the custom web-search function with
    the AI agent
-   **SerperDev API** -- Web search for transport-related information
-   **AsyncIO** -- Asynchronous agent execution
-   **python-dotenv** -- Environment variable management
-   **Session-free sequential workflow** -- Agent outputs are passed
    directly between stages

## 🔎 Web Search Tool

The application integrates a custom asynchronous search function with
AutoGen:

``` python
serper_tool = FunctionTool(
    search_transit_web,
    description="Search live web data for Tamil Nadu bus routes, MTC/TNSTC/SETC schedules, and transit updates."
)
```

The Route & Schedule Agent uses this tool to search for relevant transport information.

## 🖥️ User Interface

The Streamlit dashboard provides:

-   Transport corporation selection
-   Starting point input
-   Destination input
-   Expected travel time input
-   Multi-Agent Analyzer button
-   Agent execution status
-   Route & Schedule results
-   Crowd Analysis results
-   Commute Advisor results
-   Final Guide View

## 📋 Supported Transport Options

The application provides options for:

-   **Unified MTC + TNSTC + SETC**
-   **MTC -- Metropolitan City Buses**
-   **TNSTC -- Regional & Town Buses**
-   **SETC -- Long-Distance Express Services**

## 📂 Project Structure

``` text
Tamil-Nadu-Public-Transport-Assistant/
│
├── main.py
├── README.md
├── requirements.txt
├── .env
└── .gitignore
```

## ⚙️ Installation

### 1. Clone the repository
``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Tamil-Nadu-Public-Transport-Assistant
### 2. Create a virtual environment
``` bash
python -m venv venv
```
### 3. Activate the virtual environment
**Windows PowerShell:**

``` powershell
.\venv\Scripts\Activate.ps1
```
### 4. Install dependencies
``` bash
pip install -r requirements.txt
```
## 🔐 Environment Variables

Create a `.env` file in the project root:
``` env
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
```
Add `.env` to `.gitignore`:

``` text
.env
venv/
__pycache__/
```
> ⚠️ Never commit API keys or other secrets to GitHub.

## ▶️ Run the Application

Start the Streamlit application:

``` bash
streamlit run main.py
```

The application will open in your browser.

## 🎯 Example Use Case

``` text
Transport: SETC
From: Chennai
To: Coimbatore
Expected Time: 8:00 AM
```

The application processes the request through the four-agent workflow
and generates:

1.  Route and schedule information
2.  Crowd and traffic analysis
3.  Alternative commute strategies
4.  Final travel advisory

## 📌 Project Highlights

This project demonstrates practical implementation of:

-   Multi-Agent AI architecture
-   Specialized AI agents
-   Sequential agent workflows
-   LLM-powered analysis
-   Custom AI tools with `FunctionTool`
-   External web-search integration
-   Asynchronous AI execution
-   Streamlit-based GenAI application development

## 🔮 Future Enhancements

Potential improvements include:

-   Real-time bus tracking
-   Live government transport APIs
-   Fare and ticket information
-   Bus availability and seat information
-   Location/GPS integration
-   Route maps
-   Voice-based travel assistant
-   Tamil language support
-   Personalized commuter preferences
-   Persistent travel history

## 👨‍💻 Author

**CB Chakravarthy K**

