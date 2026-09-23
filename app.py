import os
import asyncio
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Tamil Nadu Public Transport Assistant",
    page_icon="🚌",
    layout="wide"
)

# --- CUSTOM CSS STYLING ---
st.markdown("""
    <style>
    /* Global App Background */
    .stApp {
        background-color: #0B132B;
        color: #FFFFFF;
    }
    
    /* Top Header Gradient Line */
    .main-header {
        background: linear-gradient(90deg, #FF7B00 0%, #00F2FE 50%, #4FACFE 100%);
        height: 6px;
        border-radius: 3px;
        margin-bottom: 25px;
    }
    
    /* Main Title Styling - Massive & Uppercase */
    .title-text {
        font-size: 3.2rem !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        text-align: left;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 10px;
        line-height: 1.1;
    }
    
    .subtitle-text {
        font-size: 1.2rem;
        color: #00F2FE;
        font-weight: 600;
        margin-bottom: 25px;
        letter-spacing: 0.5px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1C2541;
        border-right: 1px solid #3A506B;
    }
    
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    /* Inputs Styling */
    .stTextInput input {
        background-color: #0B132B !important;
        color: white !important;
        border: 1px solid #3A506B !important;
        border-radius: 6px;
    }

    /* Dropdown Box Main Container */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #162447 !important;
        color: #FFFFFF !important;
        border: 2px solid #00F2FE !important;
        border-radius: 8px;
    }
    
    .stSelectbox div[data-baseweb="select"] div {
        color: #FFFFFF !important;
    }

    /* FORCED DROPDOWN MENU POPOVER OVERRIDE */
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
        background-color: #162447 !important;
        border: 2px solid #00F2FE !important;
        border-radius: 8px !important;
    }

    li[role="option"] {
        background-color: #162447 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    li[role="option"]:hover {
        background-color: #00F2FE !important;
        color: #0B132B !important;
    }

    /* Button Styling */
    .stButton button {
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
        color: #0B132B;
        font-weight: 800;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        transition: 0.3s;
    }
    .stButton button:hover {
        opacity: 0.85;
        color: #000000;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1C2541;
        border-radius: 6px;
        color: #FFFFFF;
        padding: 10px 20px;
        font-weight: 600;
        border: 1px solid #3A506B;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00F2FE, #4FACFE) !important;
        color: #0B132B !important;
        font-weight: 800;
    }

    /* Footer Branding Style */
    .footer-container {
        text-align: center;
        margin-top: 60px;
        padding: 25px;
        border-top: 1px solid #3A506B;
        color: #8D99AE;
        font-size: 14px;
        background-color: #0B132B;
    }
    .footer-highlight {
        color: #00F2FE;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<div class="main-header"></div>', unsafe_allow_html=True)
st.markdown('<p class="title-text">🚌 TAMIL NADU PUBLIC TRANSPORT ASSISTANT</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">✨ Unified MTC, TNSTC & SETC Route & Crowd Predictor | Powered by Multi-Agent AI</p>', unsafe_allow_html=True)

# --- SIDEBAR UI ---
with st.sidebar:
    # Highly Visible Clean Gold/Dark Emblem Box (Guaranteed Color Change)
    st.markdown("""
        <div style="background: linear-gradient(135deg, #FFB703, #FB8500); padding: 14px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 2px solid #FFFFFF; box-shadow: 0 4px 10px rgba(0,0,0,0.4);">
            <h3 style="color: #0B132B; margin: 0; font-size: 15px; font-weight: 900;">🏛️ TAMIL NADU STATE TRANSIT</h3>
            <p style="color: #0B132B; margin: 0; font-size: 11px; font-weight: 700;">Government of Tamil Nadu Initiative</p>
        </div>
    """, unsafe_allow_html=True)

    st.header("🚍 Transit Configuration")

    # Dropdown to choose service options
    transport_service = st.selectbox(
        "Select Transport Corporation:",
        [
            "Unified (MTC + TNSTC + SETC)",
            "MTC (Metropolitan City Buses - Chennai)",
            "TNSTC (Regional & Town Buses across TN)",
            "SETC (Long-Distance Express Services)"
        ]
    )

    st.markdown("---")
    st.subheader("📍 Journey Details")
    starting_point = st.text_input("From (Starting Point):", placeholder="e.g., Madurai Mattuthavani")
    destination = st.text_input("To (Destination):", placeholder="e.g., Chennai Koyambedu")
    travel_time = st.text_input("Expected Time / Day:", placeholder="e.g., Tomorrow 8:00 AM Peak Hour")

    st.markdown("<br>", unsafe_allow_html=True)
    run_search = st.button("Run Multi-Agent Analyzer 🚀", use_container_width=True)

# --- DEFINE SERPERDEV SEARCH TOOL ---
async def search_transit_web(query: str) -> str:
    """Searches the web using SerperDev API for real-time bus routes, timings, and transit data in Tamil Nadu."""
    serper_api_key = os.getenv("SERPER_API_KEY")
    if not serper_api_key:
        return "SerperDev API key not found. Proceeding with internal agent knowledge base."
    
    url = "https://google.serper.dev/search"
    payload = {"q": query, "gl": "in", "hl": "en"}
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        data = response.json()
        results = []
        if "organic" in data:
            for item in data["organic"][:3]:
                results.append(f"- {item.get('title')}: {item.get('snippet')}")
        return "\n".join(results) if results else "No direct live web results found."
    except Exception as e:
        return f"Error connecting to SerperDev search: {str(e)}"

serper_tool = FunctionTool(
    search_transit_web, 
    description="Search live web data for Tamil Nadu bus routes, MTC/TNSTC/SETC schedules, and transit updates."
)

# --- MAIN RUN LOGIC ---
if run_search:
    if not starting_point or not destination:
        st.warning("⚠️ Please provide both a Starting Point and a Destination in the sidebar.")
    else:
        if not os.getenv("OPENAI_API_KEY"):
            st.error("❌ OPENAI_API_KEY is missing. Please configure it in your .env file.")
        else:
            model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

            async def run_pipeline():
                agent_tools = [serper_tool]

                # --- 4 AGENTS DEFINITION ---
                route_agent = AssistantAgent(
                    name="Route_Schedule_Agent",
                    model_client=model_client,
                    tools=agent_tools,
                    system_message=(
                        f"You are the expert Route & Schedule Agent for {transport_service} in Tamil Nadu. "
                        "Use your search tool to look up live bus networks, route numbers, boarding stops, "
                        "and approximate travel schedules between the given source and destination."
                    )
                )

                crowd_agent = AssistantAgent(
                    name="Crowd_Traffic_Analyst_Agent",
                    model_client=model_client,
                    system_message=(
                        "You are the Crowd & Traffic Analyst Agent. Analyze the travel context, time of day, "
                        "peak office hours, and regional festival rushes across Tamil Nadu to predict crowd density, "
                        "congestion levels, and seating availability."
                    )
                )

                advisor_agent = AssistantAgent(
                    name="Commute_Advisor_Agent",
                    model_client=model_client,
                    system_message=(
                        "You are the Commute Advisor Agent. Based on the routes and crowd predictions, "
                        "suggest smart alternative strategies, less crowded travel timings, or multi-modal connections "
                        "(combining MTC, TNSTC, or SETC efficiently)."
                    )
                )

                guide_agent = AssistantAgent(
                    name="Transport_Guide_Agent",
                    model_client=model_client,
                    system_message=(
                        "You are the final Transport Guide Agent. Synthesize all insights from the preceding agents "
                        "into a clean, well-formatted, professional layout suitable for a Streamlit user dashboard."
                    )
                )

                task_query = (
                    f"Plan a trip from {starting_point} to {destination} using {transport_service} "
                    f"at time: {travel_time}. Search for real route options and provide schedule details."
                )

                # --- EXECUTION STATUS TRACKER ---
                with st.status("🔍 Step 1/4: Route & Schedule Agent querying transport networks...", expanded=True) as status:
                    res1 = await route_agent.run(task=task_query)
                    out1 = res1.messages[-1].content
                    st.write(out1)
                    status.update(label="✅ Route Mapping Completed!", state="complete", expanded=False)

                with st.status("👥 Step 2/4: Crowd & Traffic Analyst Agent evaluating passenger density...", expanded=True) as status:
                    res2 = await crowd_agent.run(task=f"Analyze crowd levels for these routes:\n{out1}")
                    out2 = res2.messages[-1].content
                    st.write(out2)
                    status.update(label="✅ Crowd Prediction Completed!", state="complete", expanded=False)

                with st.status("💡 Step 3/4: Commute Advisor Agent formulating smart alternatives...", expanded=True) as status:
                    res3 = await advisor_agent.run(task=f"Provide alternate optimization based on:\n{out2}")
                    out3 = res3.messages[-1].content
                    st.write(out3)
                    status.update(label="✅ Advisory Generation Completed!", state="complete", expanded=False)

                with st.status("🎯 Step 4/4: Transport Guide Agent preparing final dashboard view...", expanded=True) as status:
                    res4 = await guide_agent.run(task=f"Format this final travel advisory package cleanly:\n{out3}")
                    out4 = res4.messages[-1].content
                    st.write(out4)
                    status.update(label="✅ Multi-Agent Workflow Fully Finished!", state="complete", expanded=True)

                return out1, out2, out3, out4

            with st.spinner("🤖 Multi-agent transport network is collaborating... Please hold on."):
                r_out, c_out, a_out, f_out = asyncio.run(run_pipeline())

            st.success("🎉 Journey Plan Generated Successfully!")

            # Display Tabbed Results
            tab1, tab2, tab3, tab4 = st.tabs([
                "🚌 Route & Schedule", 
                "👥 Crowd Analysis", 
                "💡 Commute Advisor", 
                "🎯 Final Guide View"
            ])
            with tab1:
                st.markdown(r_out)
            with tab2:
                st.markdown(c_out)
            with tab3:
                st.markdown(a_out)
            with tab4:
                st.markdown(f_out)

else:
    st.info("👈 Select your transport service, enter your source & destination in the left sidebar, and click **'Run Multi-Agent Analyzer'**.")

# --- COPYRIGHT & POWERED BY FOOTER ---
st.markdown("""
    <div class="footer-container">
        <p>© 2026 Tamil Nadu Public Transport Assistant. All rights reserved.</p>
        <p>Designed & Developed with ❤️ for Tamil Nadu Commuters | <span class="footer-highlight">Powered by Cibi Chakravarthy</span></p>
    </div>
""", unsafe_allow_html=True)