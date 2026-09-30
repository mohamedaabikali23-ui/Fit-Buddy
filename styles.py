"""
FitBuddy - Custom UI Theme and Styling
High-end dark mode aesthetics, glassmorphism, responsive cards, and vibrant accents.
"""

def get_custom_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1250px !important;
    }

    /* Top Hero Header */
    .hero-header {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(6, 182, 212, 0.12) 50%, rgba(99, 102, 241, 0.08) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 26px 30px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.22) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 30%, #34d399 70%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
        max-width: 720px;
        line-height: 1.5;
    }

    /* Stat Cards */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }
    .stat-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 20px;
        position: relative;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: rgba(52, 211, 153, 0.4);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 0 15px 0 rgba(16, 185, 129, 0.15);
    }
    .stat-icon {
        font-size: 1.5rem;
        margin-bottom: 8px;
        display: inline-block;
    }
    .stat-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #9ca3af;
        margin-bottom: 4px;
    }
    .stat-value {
        font-size: 1.85rem;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
        color: #f9fafb;
        margin-bottom: 4px;
        line-height: 1.1;
    }
    .stat-subtext {
        font-size: 0.8rem;
        color: #6b7280;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .badge-green { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-blue { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .badge-amber { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-purple { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
    .badge-rose { background: rgba(244, 63, 94, 0.15); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.3); }

    /* Macro Bar */
    .macro-bar-container {
        background: #1f2937;
        border-radius: 9999px;
        height: 14px;
        display: flex;
        overflow: hidden;
        margin: 12px 0 16px 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    }
    .macro-segment {
        height: 100%;
        transition: width 0.4s ease;
    }
    .macro-protein { background: linear-gradient(90deg, #10b981, #34d399); }
    .macro-carbs { background: linear-gradient(90deg, #0284c7, #38bdf8); }
    .macro-fat { background: linear-gradient(90deg, #f59e0b, #fbbf24); }

    /* Section Cards */
    .section-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 24px;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Chat Messages */
    .chat-bubble-user {
        background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 100%);
        color: #ffffff;
        padding: 14px 18px;
        border-radius: 18px 18px 4px 18px;
        margin-left: auto;
        max-width: 80%;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(29, 78, 216, 0.25);
    }
    .chat-bubble-assistant {
        background: #1e293b;
        color: #f1f5f9;
        padding: 16px 20px;
        border-radius: 18px 18px 18px 4px;
        border: 1px solid #334155;
        max-width: 85%;
        margin-bottom: 14px;
        line-height: 1.6;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    /* Primary Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.6rem !important;
        font-size: 1.02rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35) !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-1px) scale(1.01) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid #1f2937;
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 10px 10px 0 0;
        font-weight: 600;
        font-size: 0.95rem;
        color: #94a3b8;
        background-color: transparent;
        border: none;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        color: #34d399 !important;
        border-bottom: 3px solid #10b981 !important;
        background-color: rgba(16, 185, 129, 0.08) !important;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .hero-title { font-size: 1.6rem; }
        .hero-header { padding: 18px; }
        .stat-grid { grid-template-columns: 1fr; }
    }
    </style>
    """
