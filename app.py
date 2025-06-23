import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import requests
from PIL import Image
import json
import random

# Page configuration
st.set_page_config(
    page_title="SG Career Atlas - AI-Powered Career Guidance",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styles */
    .header-container {
        background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #ffffff, #a7f3d0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .header-subtitle {
        font-size: 1.25rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%);
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid #14b8a6;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(20, 184, 166, 0.2);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0f766e;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: #374151;
        line-height: 1.6;
    }
    
    /* Stats Cards */
    .stats-card {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0f766e;
        margin-bottom: 0.5rem;
    }
    
    .stats-label {
        color: #6b7280;
        font-weight: 500;
    }
    
    /* Search Box */
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
    }
    
    /* Career Cards */
    .career-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #14b8a6;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .career-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.5rem;
    }
    
    .career-salary {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0f766e;
        margin-bottom: 0.5rem;
    }
    
    .career-growth {
        color: #059669;
        font-weight: 500;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Button */
    .stButton > button {
        background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(20, 184, 166, 0.4);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        .feature-card {
            padding: 1.5rem;
        }
        .stats-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# Sample career data (in production, this would come from your RAG system)
CAREER_DATA = {
    "Software Engineer": {
        "salary_range": "S$70,000 - S$150,000",
        "growth_rate": "+15%",
        "description": "Design and develop software applications using various programming languages",
        "skills": ["Python", "JavaScript", "React", "Node.js", "AWS"],
        "industry": "Technology"
    },
    "Data Scientist": {
        "salary_range": "S$80,000 - S$180,000",
        "growth_rate": "+22%",
        "description": "Analyze complex data to help organizations make informed decisions",
        "skills": ["Python", "R", "Machine Learning", "SQL", "Tableau"],
        "industry": "Technology"
    },
    "Digital Marketing Manager": {
        "salary_range": "S$60,000 - S$120,000",
        "growth_rate": "+18%",
        "description": "Develop and execute digital marketing strategies across multiple channels",
        "skills": ["Google Analytics", "SEO", "Social Media", "Content Marketing", "PPC"],
        "industry": "Marketing"
    },
    "Financial Analyst": {
        "salary_range": "S$55,000 - S$110,000",
        "growth_rate": "+12%",
        "description": "Analyze financial data and market trends to guide investment decisions",
        "skills": ["Excel", "Financial Modeling", "Bloomberg", "SQL", "Python"],
        "industry": "Finance"
    },
    "UX Designer": {
        "salary_range": "S$65,000 - S$130,000",
        "growth_rate": "+20%",
        "description": "Design user-centered digital experiences and interfaces",
        "skills": ["Figma", "Adobe Creative Suite", "User Research", "Prototyping", "HTML/CSS"],
        "industry": "Design"
    }
}

INDUSTRY_TRENDS = {
    "Technology": {"growth": 25, "jobs": 15000, "avg_salary": 95000},
    "Finance": {"growth": 12, "jobs": 8000, "avg_salary": 85000},
    "Healthcare": {"growth": 18, "jobs": 12000, "avg_salary": 75000},
    "Marketing": {"growth": 15, "jobs": 6000, "avg_salary": 70000},
    "Design": {"growth": 20, "jobs": 4000, "avg_salary": 80000}
}

def simulate_rag_search(query):
    """Simulate RAG-based search results"""
    results = []
    query_lower = query.lower()
    
    for career, data in CAREER_DATA.items():
        if (query_lower in career.lower() or 
            query_lower in data['description'].lower() or
            any(query_lower in skill.lower() for skill in data['skills']) or
            query_lower in data['industry'].lower()):
            results.append({
                'career': career,
                'relevance': random.uniform(0.7, 1.0),
                **data
            })
    
    return sorted(results, key=lambda x: x['relevance'], reverse=True)

def main():
    # Header Section
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🧭 SG Career Atlas</h1>
        <p class="header-subtitle">Navigate Your Career Journey with AI Intelligence</p>
        <p style="font-size: 1.1rem; opacity: 0.8;">Discover personalized career paths, market insights, and growth opportunities tailored specifically for Singapore's dynamic job landscape.</p>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Menu
    selected = option_menu(
        menu_title=None,
        options=["🏠 Home", "🔍 Career Explorer", "📊 Market Insights", "🎯 Skills Assessment", "📚 Resources"],
        icons=["house", "search", "graph-up", "target", "book"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#f0fdfa"},
            "icon": {"color": "#0f766e", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#ccfbf1",
                "color": "#374151"
            },
            "nav-link-selected": {"background-color": "#14b8a6", "color": "white"},
        }
    )

    if selected == "🏠 Home":
        show_home_page()
    elif selected == "🔍 Career Explorer":
        show_career_explorer()
    elif selected == "📊 Market Insights":
        show_market_insights()
    elif selected == "🎯 Skills Assessment":
        show_skills_assessment()
    elif selected == "📚 Resources":
        show_resources()

def show_home_page():
    # AI-Powered Search Section
    st.markdown("""
    <div class="search-container">
        <h2 style="text-align: center; color: #111827; margin-bottom: 1rem;">Ask Our AI Career Assistant</h2>
        <p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">Get instant insights about careers, salaries, skills, and industry trends</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search Interface
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input(
            "",
            placeholder="Ask about careers, salaries, skills, or industry trends...",
            key="main_search"
        )
    with col2:
        search_button = st.button("🔍 Search", key="search_btn")
    
    if search_button and search_query:
        with st.spinner("🤖 AI is analyzing your query..."):
            results = simulate_rag_search(search_query)
            st.session_state.search_results = results
    
    # Display Search Results
    if st.session_state.search_results:
        st.markdown("### 🎯 Search Results")
        for result in st.session_state.search_results[:3]:
            st.markdown(f"""
            <div class="career-card">
                <div class="career-title">{result['career']}</div>
                <div class="career-salary">💰 {result['salary_range']}</div>
                <div class="career-growth">📈 Growth: {result['growth_rate']}</div>
                <p style="margin-top: 1rem; color: #6b7280;">{result['description']}</p>
                <div style="margin-top: 1rem;">
                    <strong>Key Skills:</strong> {', '.join(result['skills'][:3])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Quick Stats Section
    st.markdown("### 📈 Platform Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">500+</div>
            <div class="stats-label">Career Paths</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">50K+</div>
            <div class="stats-label">Data Points</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">95%</div>
            <div class="stats-label">Satisfaction</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">24/7</div>
            <div class="stats-label">AI Support</div>
        </div>
        """, unsafe_allow_html=True)

    # Features Section
    st.markdown("### 🚀 Platform Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧭</div>
            <div class="feature-title">Career Path Discovery</div>
            <div class="feature-description">Explore diverse career opportunities tailored to Singapore's job market with AI-powered insights.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Market Intelligence</div>
            <div class="feature-description">Get real-time salary benchmarks, industry trends, and growth projections for informed decisions.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">Skills Gap Analysis</div>
            <div class="feature-description">Identify skill gaps and receive personalized learning recommendations to advance your career.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤝</div>
            <div class="feature-title">Industry Networks</div>
            <div class="feature-description">Connect with professionals and discover networking opportunities in your field of interest.</div>
        </div>
        """, unsafe_allow_html=True)

def show_career_explorer():
    st.markdown("## 🔍 Career Explorer")
    st.markdown("Discover and explore career opportunities across Singapore's job market.")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        industry_filter = st.selectbox("Industry", ["All"] + list(INDUSTRY_TRENDS.keys()))
    with col2:
        salary_filter = st.selectbox("Salary Range", ["All", "S$50K-70K", "S$70K-100K", "S$100K+"])
    with col3:
        growth_filter = st.selectbox("Growth Rate", ["All", "High (>20%)", "Medium (10-20%)", "Low (<10%)"])
    
    # Career Cards
    st.markdown("### Available Careers")
    for career, data in CAREER_DATA.items():
        if industry_filter == "All" or data['industry'] == industry_filter:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="career-card">
                    <div class="career-title">{career}</div>
                    <div class="career-salary">💰 {data['salary_range']}</div>
                    <div class="career-growth">📈 Growth: {data['growth_rate']}</div>
                    <p style="margin-top: 1rem; color: #6b7280;">{data['description']}</p>
                    <div style="margin-top: 1rem;">
                        <strong>Industry:</strong> {data['industry']} | <strong>Key Skills:</strong> {', '.join(data['skills'][:3])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button(f"Learn More", key=f"learn_{career}"):
                    st.info(f"Detailed information about {career} would be displayed here.")

def show_market_insights():
    st.markdown("## 📊 Market Insights")
    st.markdown("Real-time market data and industry trends for Singapore.")
    
    # Industry Growth Chart
    st.markdown("### Industry Growth Trends")
    industries = list(INDUSTRY_TRENDS.keys())
    growth_rates = [INDUSTRY_TRENDS[ind]['growth'] for ind in industries]
    
    fig = px.bar(
        x=industries,
        y=growth_rates,
        title="Industry Growth Rates (%)",
        color=growth_rates,
        color_continuous_scale="Teal"
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif")
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Salary Comparison
    st.markdown("### Average Salary by Industry")
    salaries = [INDUSTRY_TRENDS[ind]['avg_salary'] for ind in industries]
    
    fig2 = px.scatter(
        x=growth_rates,
        y=salaries,
        size=[INDUSTRY_TRENDS[ind]['jobs'] for ind in industries],
        color=industries,
        title="Growth Rate vs Average Salary",
        labels={'x': 'Growth Rate (%)', 'y': 'Average Salary (S$)'}
    )
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif")
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Market Summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Fastest Growing Industry", "Technology", "25%")
    with col2:
        st.metric("Highest Paying Industry", "Technology", "S$95,000")
    with col3:
        st.metric("Most Job Openings", "Technology", "15,000")

def show_skills_assessment():
    st.markdown("## 🎯 Skills Assessment")
    st.markdown("Evaluate your current skills and discover areas for improvement.")
    
    # Skills Assessment Form
    with st.form("skills_assessment"):
        st.markdown("### Current Skills Evaluation")
        
        col1, col2 = st.columns(2)
        with col1:
            technical_skills = st.multiselect(
                "Technical Skills",
                ["Python", "JavaScript", "React", "SQL", "AWS", "Machine Learning", "Data Analysis", "Excel"]
            )
            experience_level = st.selectbox(
                "Experience Level",
                ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior Level (6+ years)"]
            )
        
        with col2:
            soft_skills = st.multiselect(
                "Soft Skills",
                ["Leadership", "Communication", "Problem Solving", "Project Management", "Teamwork", "Creativity"]
            )
            career_interest = st.selectbox(
                "Career Interest",
                list(CAREER_DATA.keys())
            )
        
        submitted = st.form_submit_button("🔍 Analyze Skills")
        
        if submitted:
            st.success("✅ Skills assessment completed!")
            
            # Show recommendations
            st.markdown("### 📋 Personalized Recommendations")
            
            if career_interest in CAREER_DATA:
                required_skills = CAREER_DATA[career_interest]['skills']
                missing_skills = [skill for skill in required_skills if skill not in technical_skills]
                
                if missing_skills:
                    st.markdown("#### 🎯 Skills to Develop")
                    for skill in missing_skills:
                        st.markdown(f"- **{skill}**: High priority for {career_interest}")
                else:
                    st.markdown("#### 🎉 Great Match!")
                    st.markdown(f"Your skills align well with {career_interest} requirements!")
                
                # Learning recommendations
                st.markdown("#### 📚 Recommended Learning Paths")
                for skill in missing_skills[:3]:
                    st.markdown(f"""
                    <div style="background: #f0fdfa; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; border-left: 4px solid #14b8a6;">
                        <strong>{skill}</strong><br>
                        <small>Estimated time: 2-3 months | Difficulty: Intermediate</small>
                    </div>
                    """, unsafe_allow_html=True)

def show_resources():
    st.markdown("## 📚 Resources")
    st.markdown("Curated resources to accelerate your career growth.")
    
    # Resource Categories
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Career Guides", "🎓 Learning Paths", "💼 Job Market", "🤝 Networking"])
    
    with tab1:
        st.markdown("### Career Development Guides")
        guides = [
            {"title": "Complete Guide to Tech Careers in Singapore", "type": "PDF", "duration": "30 min read"},
            {"title": "Salary Negotiation Strategies", "type": "Video", "duration": "45 min"},
            {"title": "Building Your Professional Brand", "type": "Article", "duration": "15 min read"},
            {"title": "Interview Preparation Checklist", "type": "Checklist", "duration": "10 min"}
        ]
        
        for guide in guides:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 0.75rem; margin: 1rem 0; border: 1px solid #e5e7eb;">
                <h4 style="color: #111827; margin-bottom: 0.5rem;">{guide['title']}</h4>
                <p style="color: #6b7280; margin-bottom: 1rem;">Type: {guide['type']} | Duration: {guide['duration']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Recommended Learning Paths")
        paths = [
            {"title": "Data Science Fundamentals", "skills": ["Python", "Statistics", "Machine Learning"], "duration": "3 months"},
            {"title": "Full-Stack Development", "skills": ["JavaScript", "React", "Node.js", "Databases"], "duration": "4 months"},
            {"title": "Digital Marketing Mastery", "skills": ["SEO", "Google Analytics", "Social Media", "Content Marketing"], "duration": "2 months"},
            {"title": "Financial Analysis", "skills": ["Excel", "Financial Modeling", "Bloomberg", "Python"], "duration": "3 months"}
        ]
        
        for path in paths:
            st.markdown(f"""
            <div style="background: #f0fdfa; padding: 1.5rem; border-radius: 0.75rem; margin: 1rem 0; border: 1px solid #14b8a6;">
                <h4 style="color: #0f766e; margin-bottom: 0.5rem;">{path['title']}</h4>
                <p style="color: #374151; margin-bottom: 0.5rem;">Duration: {path['duration']}</p>
                <p style="color: #6b7280;"><strong>Skills:</strong> {', '.join(path['skills'])}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Job Market Intelligence")
        st.markdown("- **Weekly Job Market Report**: Latest trends and opportunities")
        st.markdown("- **Salary Benchmarking Tool**: Compare your compensation")
        st.markdown("- **Company Culture Insights**: Reviews and ratings")
        st.markdown("- **Remote Work Opportunities**: Flexible job listings")
    
    with tab4:
        st.markdown("### Networking Opportunities")
        events = [
            {"title": "Singapore Tech Meetup", "date": "Next Tuesday", "type": "In-person"},
            {"title": "Data Science Community", "date": "This Friday", "type": "Virtual"},
            {"title": "Startup Networking Night", "date": "Next Week", "type": "Hybrid"},
            {"title": "Women in Tech Singapore", "date": "Monthly", "type": "In-person"}
        ]
        
        for event in events:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 0.75rem; margin: 1rem 0; border: 1px solid #e5e7eb;">
                <h4 style="color: #111827; margin-bottom: 0.5rem;">{event['title']}</h4>
                <p style="color: #6b7280;">📅 {event['date']} | 📍 {event['type']}</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
