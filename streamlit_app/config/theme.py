"""
ABACO Financial Intelligence Platform - 4K Theme Configuration
Enterprise-grade dark theme with purple gradients for superior visual analytics

ABACO_THEME = {
    # Primary Brand Colors (Purple Gradient Palette)
    "brand_primary_light": "#9b87f5",
    "brand_primary_medium": "#7E69AB",
    "brand_primary_dark": "#6E59A5",
    "brand_primary_darker": "#1A1F2C",
    
    # Background Colors (Dark Theme)
    "bg_primary": "#0a0a0a",
    "bg_secondary": "#1a1a1a",
    "bg_tertiary": "#2a2a2a",
    "bg_card": "#1e1e2e",
    "bg_hover": "#2e2e3e",
    
    # Text Colors
    "text_primary": "#ffffff",
    "text_secondary": "#b4b4b4",
    "text_muted": "#888888",
    "text_accent": "#9b87f5",
    
    # Accent Colors
    "accent_success": "#22c55e",
    "accent_warning": "#f59e0b",
    "accent_danger": "#ef4444",
    "accent_info": "#3b82f6",
    
    # Chart Colors (Purple-based Palette)
    "chart_colors": [
        "#9b87f5", "#7E69AB", "#6E59A5", "#D946EF",
        "#8B5CF6", "#A855F7", "#C084FC", "#E9D5FF"
    ],
    
    # Gradient Definitions
    "gradient_primary": "linear-gradient(135deg, #9b87f5 0%, #7E69AB 50%, #6E59A5 100%)",
    "gradient_secondary": "linear-gradient(135deg, #1A1F2C 0%, #2a2a2a 100%)",
    "gradient_accent": "linear-gradient(135deg, #D946EF 0%, #8B5CF6 100%)",
    
    # Typography
    "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "font_size_base": "16px",
    "font_size_large": "20px",
    "font_size_xlarge": "28px",
    
    # Spacing
    "spacing_xs": "0.5rem",
    "spacing_sm": "1rem",
    "spacing_md": "1.5rem",
    "spacing_lg": "2rem",
    "spacing_xl": "3rem",
    
    # Border Radius
    "border_radius_sm": "4px",
    "border_radius_md": "8px",
    "border_radius_lg": "12px",
    "border_radius_xl": "16px",
    
    # Shadows
    "shadow_sm": "0 1px 2px 0 rgba(0, 0, 0, 0.3)",
    "shadow_md": "0 4px 6px -1px rgba(0, 0, 0, 0.4)",
    "shadow_lg": "0 10px 15px -3px rgba(0, 0, 0, 0.5)",
    "shadow_xl": "0 20px 25px -5px rgba(0, 0, 0, 0.6)",
    
    # 4K Resolution Settings
    "chart_width": 3840,
    "chart_height": 2160,
    "dpi": 300,
    "export_scale": 4,
}

# Plotly Layout Template for 4K Resolution
PLOTLY_LAYOUT_4K = {
    "template": "plotly_dark",
    "paper_bgcolor": ABACO_THEME["bg_primary"],
    "plot_bgcolor": ABACO_THEME["bg_card"],
    "font": {
        "family": ABACO_THEME["font_family"],
        "size": 14,
        "color": ABACO_THEME["text_primary"]
    },
    "title": {
        "font": {
            "size": 24,
            "color": ABACO_THEME["text_primary"],
            "family": ABACO_THEME["font_family"]
        },
        "x": 0.5,
        "xanchor": "center"
    "legend": {
        "bgcolor": ABACO_THEME["bg_secondary"],
        "bordercolor": ABACO_THEME["brand_primary_medium"],
        "borderwidth": 1,
            "size": 12,
            "color": ABACO_THEME["text_secondary"]
        }
    "colorway": ABACO_THEME["chart_colors"],
    "width": 1920,  # Full HD default, can scale to 4K
    "height": 1080,
    "margin": {"l": 80, "r": 80, "t": 100, "b": 80},

# Custom CSS for Streamlit
CUSTOM_CSS = f"""
<style>
    /* Import Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {{
        background: {ABACO_THEME["bg_primary"]};
        font-family: {ABACO_THEME["font_family"]};
        color: {ABACO_THEME["text_primary"]};
    }}
    
    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {{
        background: {ABACO_THEME["bg_secondary"]};
        border-right: 1px solid {ABACO_THEME["brand_primary_dark"]};
    
    /* Header Styling */
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 700;
    
    h1 {{
        background: {ABACO_THEME["gradient_primary"]};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: {ABACO_THEME["font_size_xlarge"]};
    
    /* Card Styling */
    .element-container {{
        background: {ABACO_THEME["bg_card"]};
        border-radius: {ABACO_THEME["border_radius_md"]};
        padding: {ABACO_THEME["spacing_sm"]};
        margin: {ABACO_THEME["spacing_xs"]} 0;
        box-shadow: {ABACO_THEME["shadow_md"]};
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {{
        font-size: {ABACO_THEME["font_size_large"]};
        color: {ABACO_THEME["brand_primary_light"]};
    
    [data-testid="stMetricLabel"] {{
        color: {ABACO_THEME["text_secondary"]};
        font-size: 14px;
        font-weight: 500;
    
    /* Button Styling */
    .stButton > button {{
        border: none;
        padding: {ABACO_THEME["spacing_xs"]} {ABACO_THEME["spacing_md"]};
        font-weight: 600;
        transition: all 0.3s ease;
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: {ABACO_THEME["shadow_lg"]};
    
    /* DataFrame Styling */
    .dataframe {{
        background: {ABACO_THEME["bg_card"]} !important;
    
    .dataframe th {{
        background: {ABACO_THEME["gradient_primary"]} !important;
        color: {ABACO_THEME["text_primary"]} !important;
        padding: 12px;
    
    .dataframe td {{
        color: {ABACO_THEME["text_secondary"]} !important;
        padding: 10px;
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {{
        background: {ABACO_THEME["bg_tertiary"]};
        border: 1px solid {ABACO_THEME["brand_primary_dark"]};
        border-radius: {ABACO_THEME["border_radius_sm"]};
    
    /* Alert Boxes */
    .stAlert {{
        border-left: 4px solid {ABACO_THEME["brand_primary_medium"]};
        padding: {ABACO_THEME["spacing_md"]};
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        padding: 8px;
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
    
    .stTabs [aria-selected="true"] {{
    
    /* Spinner */
    .stSpinner > div {{
        border-top-color: {ABACO_THEME["brand_primary_light"]};
    
    /* Progress Bar */
    .stProgress > div > div > div {{
    
    /* Expander */
    .streamlit-expanderHeader {{
    
    /* File Uploader */
    [data-testid="stFileUploadDropzone"] {{
        border: 2px dashed {ABACO_THEME["brand_primary_medium"]};
        border-radius: {ABACO_THEME["border_radius_lg"]};
    
    /* Toast Messages */
    .stToast {{
        border-left: 4px solid {ABACO_THEME["brand_primary_light"]};
        box-shadow: {ABACO_THEME["shadow_xl"]};
</style>

# Plotly Chart Configuration for 4K Export
PLOTLY_CONFIG_4K = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    "toImageButtonOptions": {
        "format": "png",
        "filename": "abaco_chart_4k",
        "height": 2160,
        "width": 3840,
        "scale": 4
    }
