import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from datetime import datetime


API_KEY = st.secrets["OPENWEATHER_API_KEY"] 
BASE_URL = "https://api.openweathermap.org/data/2.5"


st.set_page_config(
    page_title="Weather Analytics",
    page_icon="⛈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Global Settings */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #000000;  /* Changed to black */
        color: #ffffff;
    }

    /* Remove Streamlit branding for clean look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Input Section Styling */
    .stTextInput > div > div > input {
        background-color: #1f2937;
        color: white;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6, #2563EB);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.5);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563EB, #1D4ED8);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.6);
        transform: translateY(-2px);
    }

    /* Custom Metric Cards (Glassmorphism) */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s;
        margin-bottom: 1rem;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(59, 130, 246, 0.5);
    }
    .metric-label {
        font-size: 0.9rem;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #F3F4F6;
    }
    
    /* Header Container */
    .header-container {
        padding: 2rem 0;
        text-align: center;
        margin-bottom: 2rem;
    }
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(left, #60A5FA, #34D399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #E5E7EB;
        margin: 2rem 0 1rem 0;
        border-left: 4px solid #3B82F6;
        padding-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown('<div class="header-container"><div class="header-title">Weather Analytics</div></div>', unsafe_allow_html=True)

# ================= INPUT SECTION =================
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        city = st.text_input("", placeholder="Search City (e.g., London, Dubai)", label_visibility="collapsed")
    with col_btn:
        search_btn = st.button("Search")

# ================= FUNCTIONS =================
def fetch_current_weather(city):
    url = f"{BASE_URL}/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    return requests.get(url, params=params).json()

def fetch_forecast_weather(city):
    url = f"{BASE_URL}/forecast"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    return requests.get(url, params=params).json()

# ================= MAIN LOGIC =================
if search_btn and city:

    with st.spinner("Analyzing atmospheric data..."):
        current_data = fetch_current_weather(city)
        forecast_data = fetch_forecast_weather(city)

    if current_data.get("cod") != 200:
        st.error(f"❌ Could not find data for '{city}'. Please check the spelling.")
    else:
        # -------- Current Weather Data --------
        temp = current_data["main"]["temp"]
        feels_like = current_data["main"]["feels_like"]
        humidity = current_data["main"]["humidity"]
        wind = current_data["wind"]["speed"]
        condition = current_data["weather"][0]["main"]
        description = current_data["weather"][0]["description"].title()
        icon = current_data["weather"][0]["icon"]

        # -------- Header Info --------
        st.markdown(f"<h2 style='text-align:center; color: white;'>Current Weather in {city.title()}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color: #9CA3AF; margin-bottom: 30px;'>{description} • {datetime.now().strftime('%A, %d %B %Y')}</p>", unsafe_allow_html=True)

        cols = st.columns(4)
        
        # Define metrics data structure
        metrics_data = [
            ("Temperature", f"{round(temp, 1)}°C"),
            ("Feels Like", f"{round(feels_like, 1)}°C"),
            ("Humidity", f"{humidity}%"),
            ("Wind Speed", f"{wind} m/s")
        ]

        for col, (label, value) in zip(cols, metrics_data):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)

        # -------- Condition Row --------
        st.markdown("---")
        
        # ================= ANALYSIS =================
        st.markdown('<div class="section-header">Forecast Analytics</div>', unsafe_allow_html=True)

        forecast_list = forecast_data["list"]
        times = [datetime.strptime(i["dt_txt"], "%Y-%m-%d %H:%M:%S") for i in forecast_list]
        temps = [i["main"]["temp"] for i in forecast_list]
        humidity_list = [i["main"]["humidity"] for i in forecast_list]
        wind_list = [i["wind"]["speed"] for i in forecast_list]

       
        row1_col1, row1_col2 = st.columns([2, 1])

        # -------- Temperature Trend (Plotly Area Chart) --------
        with row1_col1:
            fig1 = px.area(
                x=times, 
                y=temps, 
                title="<b>5-Day Temperature Trend</b>",
                labels={'x': 'Time', 'y': 'Temperature (°C)'},
                color_discrete_sequence=["#3B82F6"]
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_size=18,
                hovermode="x unified"
            )
            fig1.update_xaxes(showgrid=False)
            fig1.update_yaxes(showgrid=True, gridcolor='#374151')
            st.plotly_chart(fig1, use_container_width=True)

        # -------- Humidity Gauge (Plotly Indicator) --------
    
        with row1_col2:
            fig2 = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = humidity,
                title = {'text': "<b>Current Humidity</b>", 'font': {'size': 18, 'color': 'white'}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#1CB5E0"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "#333",
                    'steps': [
                        {'range': [0, 40], 'color': 'rgba(28, 181, 224, 0.3)'},
                        {'range': [40, 70], 'color': 'rgba(28, 181, 224, 0.6)'},
                        {'range': [70, 100], 'color': 'rgba(28, 181, 224, 0.9)'}
                    ],
                }
            ))
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "white", 'family': "Inter"},
                height=300,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig2, use_container_width=True)

        # -------- Wind Trend (Plotly Bar Chart) --------
     
        st.markdown("<br>", unsafe_allow_html=True)
        fig3 = px.bar(
            x=times, 
            y=wind_list,
            title="<b>Wind Velocity Forecast</b>",
            labels={'x': 'Time', 'y': 'Speed (m/s)'},
            color=wind_list,
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=18
        )
        fig3.update_xaxes(showgrid=False)
        fig3.update_yaxes(showgrid=True, gridcolor='#374151')
        st.plotly_chart(fig3, use_container_width=True)
