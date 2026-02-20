import streamlit as st

def apply_custom_styles():
    """Apply custom styles to the Streamlit app"""
    
    # Custom CSS for additional styling
    st.markdown("""
    <style>
        /* Main elements */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #1B5E20;
            font-weight: 600;
        }
        
        h1 {
            font-size: 2.4rem;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        h2 {
            font-size: 1.8rem;
            margin: 1.5rem 0 1rem 0;
        }
        
        /* Cards and containers */
        .stCard {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            background-color: #FFFFFF;
            border-left: 4px solid #4CAF50;
        }
        
        /* Results section */
        .result-container {
            padding: 1rem;
            border-radius: 8px;
            background-color: #E8F5E9;
            margin: 1rem 0;
        }
        
        /* Status indicators */
        .status-healthy {
            color: #2E7D32;
            font-weight: bold;
        }
        
        .status-warning {
            color: #FF8F00;
            font-weight: bold;
        }
        
        .status-danger {
            color: #C62828;
            font-weight: bold;
        }
        
        /* Upload section */
        .uploadedImage {
            max-height: 400px;
            width: auto;
            margin: 0 auto;
            display: block;
            border-radius: 5px;
        }
        
        /* Analysis buttons */
        .stButton>button {
            border-radius: 6px;
            padding: 0.3rem 1rem;
            border: none;
            font-weight: 600;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Sidebar */
        .sidebar .sidebar-content {
            background-color: #E8F5E9;
        }
        
        /* Footer */
        footer {
            text-align: center;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #E0E0E0;
            font-size: 0.8rem;
            color: #757575;
        }
        
        /* Custom progress bars */
        .progress-bar-bg {
            width: 100%;
            height: 20px;
            background-color: #E0E0E0;
            border-radius: 10px;
            margin: 10px 0;
        }
        
        .progress-bar-fill {
            height: 100%;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-weight: bold;
            line-height: 20px;
            font-size: 12px;
        }
        
        /* Tab styling */
        button[data-baseweb="tab"] {
            background-color: #E8F5E9;
            border-radius: 4px 4px 0 0;
        }
        
        button[data-baseweb="tab"]:hover {
            background-color: #C8E6C9;
        }
        
        button[aria-selected="true"] {
            background-color: #81C784 !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_result_card(title, content, status="normal"):
    """Render a styled result card with appropriate status color"""
    
    if status == "healthy":
        status_color = "#4CAF50"  # Green
        icon = "✅"
    elif status == "warning":
        status_color = "#FF9800"  # Orange/Amber
        icon = "⚠️"
    elif status == "danger":
        status_color = "#F44336"  # Red
        icon = "❌"
    else:
        status_color = "#2196F3"  # Blue
        icon = "ℹ️"
    
    st.markdown(f"""
    <div style="
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: white;
        border-left: 5px solid {status_color};
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="color: {status_color}; margin-top:0;">{icon} {title}</h3>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)

def render_progress_bar(value, max_value=100, label="", color="#4CAF50"):
    """Render a custom progress bar"""
    
    percentage = min(100, max(0, (value / max_value) * 100))
    
    st.markdown(f"""
    <div style="margin: 0.5rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span>{label}</span>
            <span><b>{value}</b>/{max_value}</span>
        </div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: {percentage}%; background-color: {color};">
                {int(percentage)}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(title, value, description=None, trend=None, trend_value=None):
    """Render a styled metric card with optional trend indicator"""
    
    trend_html = ""
    if trend is not None and trend_value is not None:
        if trend == "up":
            trend_color = "#4CAF50"  # Green
            trend_icon = "↑"
        elif trend == "down":
            trend_color = "#F44336"  # Red
            trend_icon = "↓"
        else:
            trend_color = "#757575"  # Gray
            trend_icon = "→"
            
        trend_html = f"""
        <div style="color: {trend_color}; font-size: 0.8rem; margin-top: 5px;">
            {trend_icon} {trend_value}
        </div>
        """
    
    description_html = ""
    if description:
        description_html = f"""
        <div style="color: #757575; font-size: 0.9rem; margin-top: 5px;">
            {description}
        </div>
        """
    
    st.markdown(f"""
    <div style="
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="color: #757575; font-size: 0.9rem;">{title}</div>
        <div style="font-size: 1.8rem; font-weight: bold; color: #1B5E20;">{value}</div>
        {description_html}
        {trend_html}
    </div>
    """, unsafe_allow_html=True)
