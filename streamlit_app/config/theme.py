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
    "width": 1920,
    "height": 1080,
    "margin": {"l": 80, "r": 80, "t": 100, "b": 80},
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    .stApp {
        background: var(--bg-primary);
        font-family: var(--font-family);
        color: var(--text-primary);
    }
    [data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--primary-dark);
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700;
    h1 {
        font-size: 28px;
        color: var(--primary-light);
    .element-container {
        background: var(--bg-card);
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
    [data-testid="stMetricValue"] {
        font-size: 20px;
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary);
        font-size: 14px;
        font-weight: 500;
    .stButton > button {
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    .dataframe {
        background: var(--bg-card) !important;
    .dataframe th {
        background: linear-gradient(135deg, #9b87f5 0%, #7E69AB 50%, #6E59A5 100%) !important;
        color: white !important;
        padding: 12px;
    .dataframe td {
        color: var(--text-secondary) !important;
        padding: 10px;
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background: var(--bg-tertiary);
        border: 1px solid var(--primary-dark);
        border-radius: 4px;
    .stAlert {
        border-left: 4px solid var(--primary-medium);
        padding: 1.5rem;
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        padding: 8px;
    .stTabs [data-baseweb="tab"] {
        background: transparent;
    .stSpinner > div {
        border-top-color: var(--primary-light);
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed var(--primary-medium);
        border-radius: 12px;
    .stToast {
        border-left: 4px solid var(--primary-light);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
</style>
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
