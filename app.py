import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import json
from datetime import datetime
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.colored_header import colored_header

# Page configuration
st.set_page_config(
    page_title="SG Career Atlas",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 0rem 1rem;
    }
    
    .stButton>button {
        background-color: #00BFA5;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #00A693;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    
    .search-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 2rem;
    }
    
    .career-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        border: 1px solid #e0e0e0;
    }
    
    .career-card:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        transform: translateY(-3px);
        border-color: #00BFA5;
    }
    
    .skill-tag {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.2rem;
        display: inline-block;
    }
    
    .header-gradient {
        background: linear-gradient(135deg, #00BFA5 0%, #00A693 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 8px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00BFA5;
        color: white;
    }
    
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_career' not in st.session_state:
    st.session_state.selected_career = None
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Sidebar navigation
with st.sidebar:
    st.markdown("# 🧭 SG Career Atlas")
    st.markdown("---")
    
    selected = option_menu(
        menu_title=None,
        options=["Home", "Career Explorer", "Skills Assessment", "Market Insights", "Learning Hub", "AI Assistant"],
        icons=["house", "search", "clipboard-check", "graph-up", "book", "robot"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f8f9fa"},
            "icon": {"color": "#00BFA5", "font-size": "18px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "0px",
                "padding": "10px",
                "border-radius": "8px",
                "margin-bottom": "5px"
            },
            "nav-link-selected": {"background-color": "#00BFA5", "color": "white"},
        }
    )
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    st.metric("Active Users", "12,543", "↑ 8.2%")
    st.metric("Career Paths", "1,847", "↑ 3.5%")
    st.metric("Skills Tracked", "5,234", "↑ 12.1%")

# Main content area
if selected == "Home":
    # Header
    st.markdown("""
    <div class="header-gradient">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">Welcome to SG Career Atlas</h1>
        <p style="margin-top: 0.5rem; font-size: 1.2rem; opacity: 0.9;">Your AI-powered career guidance platform for Singapore</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search section
    col1, col2, col3 = st.columns([2, 3, 1])
    with col2:
        search_query = st.text_input("🔍 Search careers, skills, or industries...", placeholder="e.g., Data Scientist, Python, FinTech")
        if search_query:
            st.session_state.search_history.append(search_query)
    
    # Feature cards
    st.markdown("### 🚀 Explore Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="career-card">
            <h3>🎯 Career Pathways</h3>
            <p>Discover career trajectories and progression paths tailored to your skills and interests.</p>
            <ul>
                <li>1,800+ career paths mapped</li>
                <li>Industry-specific guidance</li>
                <li>Salary benchmarks</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="career-card">
            <h3>📊 Skills Analytics</h3>
            <p>Analyze skill gaps and get personalized recommendations for career advancement.</p>
            <ul>
                <li>5,000+ skills tracked</li>
                <li>Real-time market demand</li>
                <li>Certification paths</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="career-card">
            <h3>🤖 AI Career Coach</h3>
            <p>Get personalized career advice powered by advanced AI and local market insights.</p>
            <ul>
                <li>24/7 availability</li>
                <li>Contextual recommendations</li>
                <li>Interview preparation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Trending careers section
    st.markdown("### 📈 Trending Careers in Singapore")
    
    # Sample data for trending careers
    trending_data = pd.DataFrame({
        'Career': ['Data Scientist', 'Cloud Architect', 'UX Designer', 'Cybersecurity Analyst', 'AI Engineer'],
        'Growth': [45, 38, 32, 41, 52],
        'Avg Salary': [120000, 135000, 95000, 110000, 145000],
        'Openings': [1234, 892, 756, 1045, 623]
    })
    
    fig = px.bar(trending_data, x='Career', y='Growth', 
                 title='Career Growth Rate (%)',
                 color='Growth',
                 color_continuous_scale='teal')
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

elif selected == "Career Explorer":
    colored_header(
        label="Career Explorer",
        description="Discover career opportunities across industries",
        color_name="green-70"
    )
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        industry = st.selectbox("Industry", ["All", "Technology", "Finance", "Healthcare", "Manufacturing", "Education"])
    with col2:
        experience = st.selectbox("Experience Level", ["All", "Entry Level", "Mid Level", "Senior Level", "Executive"])
    with col3:
        salary_range = st.select_slider("Salary Range (SGD)", options=["0-50k", "50k-100k", "100k-150k", "150k+"])
    with col4:
        job_type = st.selectbox("Job Type", ["All", "Full-time", "Part-time", "Contract", "Freelance"])
    
    # Career listings
    st.markdown("### 🎯 Recommended Careers")
    
    careers = [
        {
            "title": "Senior Data Scientist",
            "company": "Tech Innovations Pte Ltd",
            "salary": "$120,000 - $150,000",
            "skills": ["Python", "Machine Learning", "SQL", "TensorFlow"],
            "match": 92
        },
        {
            "title": "Cloud Solutions Architect",
            "company": "Digital Transformation Corp",
            "salary": "$130,000 - $160,000",
            "skills": ["AWS", "Azure", "Kubernetes", "DevOps"],
            "match": 87
        },
        {
            "title": "Product Manager",
            "company": "FinTech Solutions",
            "salary": "$100,000 - $130,000",
            "skills": ["Product Strategy", "Agile", "Analytics", "Leadership"],
            "match": 85
        }
    ]
    
    for career in careers:
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="career-card">
                    <h4>{career['title']}</h4>
                    <p style="color: #666; margin: 0.5rem 0;">{career['company']}</p>
                    <p style="color: #00BFA5; font-weight: 600; margin: 0.5rem 0;">{career['salary']}</p>
                    <div style="margin-top: 1rem;">
                        {''.join([f'<span class="skill-tag">{skill}</span>' for skill in career['skills']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 2rem 0;">
                    <h2 style="color: #00BFA5; margin: 0;">{career['match']}%</h2>
                    <p style="color: #666; font-size: 0.9rem;">Match</p>
                </div>
                """, unsafe_allow_html=True)

elif selected == "Skills Assessment":
    colored_header(
        label="Skills Assessment",
        description="Evaluate your skills and identify growth areas",
        color_name="blue-70"
    )
    
    # Assessment options
    assessment_type = st.radio(
        "Choose assessment type:",
        ["Quick Skills Check", "Comprehensive Assessment", "Industry-Specific Assessment"],
        horizontal=True
    )
    
    if assessment_type == "Quick Skills Check":
        st.markdown("### 🎯 Quick Skills Check")
        
        # Skills input
        col1, col2 = st.columns([3, 1])
        with col1:
            skills_input = st.text_area("Enter your skills (comma-separated)", 
                                      placeholder="e.g., Python, Data Analysis, Machine Learning, SQL")
        with col2:
            if st.button("Analyze Skills", type="primary"):
                if skills_input:
                    # Simulated skill analysis
                    st.markdown("### 📊 Skills Analysis Results")
                    
                    skills = [s.strip() for s in skills_input.split(',')]
                    skill_levels = np.random.randint(60, 95, size=len(skills))
                    market_demand = np.random.randint(70, 100, size=len(skills))
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(name='Your Level', x=skills, y=skill_levels, marker_color='#00BFA5'))
                    fig.add_trace(go.Bar(name='Market Demand', x=skills, y=market_demand, marker_color='#FF6B6B'))
                    
                    fig.update_layout(
                        title='Skills Assessment Overview',
                        barmode='group',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Recommendations
                    st.markdown("### 💡 Recommendations")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        <div class="career-card">
                            <h4>🎯 Skills to Develop</h4>
                            <ul>
                                <li>Cloud Computing (AWS/Azure)</li>
                                <li>DevOps Practices</li>
                                <li>Advanced Machine Learning</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown("""
                        <div class="career-card">
                            <h4>📚 Recommended Courses</h4>
                            <ul>
                                <li>AWS Solutions Architect</li>
                                <li>Kubernetes Fundamentals</li>
                                <li>Deep Learning Specialization</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

elif selected == "Market Insights":
    colored_header(
        label="Market Insights",
        description="Real-time job market trends and analytics",
        color_name="orange-70"
    )
    
    # Market overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Job Openings", "15,234", "↑ 12.3%", delta_color="normal")
    with col2:
        st.metric("Avg. Salary Growth", "5.8%", "↑ 0.3%", delta_color="normal")
    with col3:
        st.metric("Skills in Demand", "847", "↑ 45", delta_color="normal")
    with col4:
        st.metric("New Companies", "234", "↑ 18", delta_color="normal")
    
    style_metric_cards()
    
    # Industry trends
    st.markdown("### 📊 Industry Growth Trends")
    
    # Sample data for industry trends
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    tech_growth = [100, 108, 115, 112, 125, 132]
    finance_growth = [100, 103, 107, 110, 108, 115]
    healthcare_growth = [100, 105, 110, 118, 122, 128]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=tech_growth, name='Technology', line=dict(color='#00BFA5', width=3)))
    fig.add_trace(go.Scatter(x=months, y=finance_growth, name='Finance', line=dict(color='#FF6B6B', width=3)))
    fig.add_trace(go.Scatter(x=months, y=healthcare_growth, name='Healthcare', line=dict(color='#4ECDC4', width=3)))
    
    fig.update_layout(
        title='Industry Growth Index (Base: 100)',
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top skills
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔥 Hottest Skills")
        hot_skills = pd.DataFrame({
            'Skill': ['AI/ML', 'Cloud Computing', 'Cybersecurity', 'Data Analytics', 'DevOps'],
            'Demand_Score': [95, 92, 88, 85, 82]
        })
        
        fig = px.bar(hot_skills, x='Demand_Score', y='Skill', orientation='h',
                     color='Demand_Score', color_continuous_scale='teal')
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Salary Ranges by Role")
        salary_data = pd.DataFrame({
            'Role': ['Junior Dev', 'Senior Dev', 'Team Lead', 'Manager', 'Director'],
            'Min': [50000, 80000, 100000, 120000, 150000],
            'Max': [70000, 120000, 140000, 180000, 250000]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Min Salary', x=salary_data['Role'], y=salary_data['Min'], marker_color='lightblue'))
        fig.add_trace(go.Bar(name='Max Salary', x=salary_data['Role'], y=salary_data['Max'], marker_color='darkblue'))
        fig.update_layout(barmode='group', height=300)
        st.plotly_chart(fig, use_container_width=True)

elif selected == "Learning Hub":
    colored_header(
        label="Learning Hub",
        description="Curated learning resources for career development",
        color_name="violet-70"
    )
    
    # Learning categories
    learning_category = st.selectbox(
        "Select Learning Category",
        ["All Categories", "Technical Skills", "Soft Skills", "Leadership", "Industry Certifications"]
    )
    
    # Featured courses
    st.markdown("### 🌟 Featured Learning Paths")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="career-card">
            <h4>🤖 AI & Machine Learning Path</h4>
            <p style="color: #666;">Master AI/ML from basics to advanced</p>
            <hr>
            <p><strong>Duration:</strong> 6 months</p>
            <p><strong>Level:</strong> Intermediate</p>
            <p><strong>Skills:</strong> Python, TensorFlow, NLP</p>
            <div style="margin-top: 1rem;">
                <span class="skill-tag">🔥 Trending</span>
                <span class="skill-tag">Certificate</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="career-card">
            <h4>☁️ Cloud Architecture Path</h4>
            <p style="color: #666;">Become a certified cloud architect</p>
            <hr>
            <p><strong>Duration:</strong> 4 months</p>
            <p><strong>Level:</strong> Advanced</p>
            <p><strong>Skills:</strong> AWS, Azure, DevOps</p>
            <div style="margin-top: 1rem;">
                <span class="skill-tag">High Demand</span>
                <span class="skill-tag">Hands-on</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="career-card">
            <h4>📊 Data Analytics Path</h4>
            <p style="color: #666;">From data to insights</p>
            <hr>
            <p><strong>Duration:</strong> 3 months</p>
            <p><strong>Level:</strong> Beginner</p>
            <p><strong>Skills:</strong> SQL, Tableau, Python</p>
            <div style="margin-top: 1rem;">
                <span class="skill-tag">Popular</span>
                <span class="skill-tag">Project-based</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Learning resources
    st.markdown("### 📚 Resources by Type")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📹 Video Courses", "📖 Books", "🎯 Projects", "🏆 Certifications"])
    
    with tab1:
        st.markdown("#### Recommended Video Courses")
        courses = [
            {"title": "Complete Python Bootcamp", "provider": "Udemy", "rating": 4.8, "students": "1.2M"},
            {"title": "AWS Certified Solutions Architect", "provider": "Coursera", "rating": 4.7, "students": "800K"},
            {"title": "Google Data Analytics Certificate", "provider": "Google", "rating": 4.9, "students": "500K"}
        ]
        for course in courses:
            st.markdown(f"""
            **{course['title']}** | {course['provider']}  
            ⭐ {course['rating']} | 👥 {course['students']} students
            """)
    
    with tab2:
        st.markdown("#### Must-Read Books")
        books = [
            "Clean Code by Robert C. Martin",
            "The Lean Startup by Eric Ries",
            "Designing Data-Intensive Applications by Martin Kleppmann"
        ]
        for book in books:
            st.markdown(f"- 📚 {book}")
    
    with tab3:
        st.markdown("#### Hands-on Projects")
        st.markdown("""
        - 🔨 Build a full-stack web application
        - 🤖 Create a machine learning model for prediction
        - 📊 Develop a data visualization dashboard
        - ☁️ Deploy a microservices architecture on cloud
        """)
    
    with tab4:
        st.markdown("#### Industry Certifications")
        certs = pd.DataFrame({
            'Certification': ['AWS Solutions Architect', 'Google Cloud Professional', 'Microsoft Azure Admin', 'Certified Kubernetes Admin'],
            'Difficulty': ['Intermediate', 'Advanced', 'Intermediate', 'Advanced'],
            'Value': [95, 92, 88, 90]
        })
        st.dataframe(certs, use_container_width=True)

elif selected == "AI Assistant":
    colored_header(
        label="AI Career Assistant",
        description="Get personalized career guidance powered by AI",
        color_name="red-70"
    )
    
    # Chat interface
    st.markdown("### 💬 Chat with Your AI Career Coach")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI Career Assistant. I can help you with career planning, skill development, job search strategies, and more. What would you like to explore today?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your career..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response (simulated)
        with st.chat_message("assistant"):
            response = f"""Based on your question about "{prompt}", here's my guidance:

I understand you're interested in exploring this topic. Let me provide you with some insights:

1. **Current Market Trends**: This area is showing significant growth in Singapore's job market.
2. **Key Skills**: Focus on developing both technical and soft skills relevant to your query.
3. **Action Steps**: Consider taking online courses, networking with professionals, and gaining hands-on experience.

Would you like me to elaborate on any specific aspect?"""
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Quick action buttons
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 Resume Review"):
            st.info("Upload your resume for AI-powered feedback and suggestions.")
    
    with col2:
        if st.button("🎯 Career Match"):
            st.info("Take a quick assessment to find careers that match your profile.")
    
    with col3:
        if st.button("💼 Interview Prep"):
            st.info("Practice common interview questions with AI feedback.")
    
    with col4:
        if st.button("📊 Salary Insights"):
            st.info("Get personalized salary benchmarks based on your experience.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>© 2024 SG Career Atlas | Empowering careers in Singapore 🇸🇬</p>
</div>
""", unsafe_allow_html=True)
