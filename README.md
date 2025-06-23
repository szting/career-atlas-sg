# SG Career Atlas - Streamlit App

## 🧭 AI-Powered Career Guidance for Singapore

SG Career Atlas is a comprehensive career guidance platform built with Streamlit, featuring RAG-based AI assistance for Singapore professionals.

## ✨ Features

- **🤖 AI Career Assistant**: RAG-powered search and recommendations
- **🔍 Career Explorer**: Discover opportunities across industries
- **📊 Market Insights**: Real-time salary and growth data
- **🎯 Skills Assessment**: Personalized skill gap analysis
- **📚 Learning Resources**: Curated career development content

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the App**
   ```bash
   streamlit run app.py
   ```

3. **Open Browser**
   Navigate to `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Fork this repository**
2. **Connect to Streamlit Cloud**
3. **Deploy directly from GitHub**

## 🛠️ Tech Stack

- **Framework**: Streamlit
- **Visualization**: Plotly, Altair
- **UI Components**: streamlit-option-menu, streamlit-extras
- **Data Processing**: Pandas, NumPy
- **Styling**: Custom CSS with Inter font

## 📁 Project Structure

```
sg-career-atlas/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── .streamlit/        # Streamlit configuration (optional)
```

## 🎨 Design Features

- **Modern UI**: Clean, professional interface with teal color scheme
- **Responsive Design**: Optimized for desktop and mobile
- **Interactive Components**: Dynamic charts and visualizations
- **Custom Styling**: Beautiful CSS animations and hover effects

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.streamlit/secrets.toml` file for production:

```toml
[general]
api_key = "your-api-key"
database_url = "your-database-url"
```

## 📊 Data Sources

Currently uses simulated data for demonstration. In production, integrate with:

- Singapore job market APIs
- Salary benchmarking services
- Skills assessment platforms
- Learning management systems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team

---

**Built with ❤️ for Singapore's career development community**
