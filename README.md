# 🎵 Music Streaming Trends Analysis Dashboard

![Music Dashboard](https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Data Analysis](https://img.shields.io/badge/Data-Analysis-green?style=for-the-badge&logo=pandas)

## 📋 Project Overview

This project provides a comprehensive analysis of global music streaming trends from 2018-2024, featuring an interactive Streamlit dashboard that transforms complex data insights into actionable business intelligence for the music industry.

### 🎯 Objectives

- **Analyze** global music streaming patterns and user behavior
- **Identify** key trends across demographics, genres, and geographical regions
- **Develop** strategic recommendations for music industry stakeholders
- **Present** findings through an intuitive, interactive dashboard suitable for executive presentations

## 🏗️ Repository Structure

```
📁 sesion12proyecto-musictrends/
├── 📂 data/                    # Raw and processed datasets
│   └── Global_Music_Streaming_Listener_Preferences.csv
├── 📂 img/                     # Visualizations and charts
├── 📂 notebooks/               # Jupyter notebooks for data exploration
│   └── music_trends_analysis_clean.ipynb
├── 📂 panel/                   # Streamlit dashboard implementation
│   └── app.py
├── .gitattributes             # Git attributes configuration
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

## 🔍 Key Features

### 📊 Interactive Dashboard Sections

1. **📈 Dataset Overview**
   - Key metrics and statistics
   - Platform distribution analysis
   - Geographic coverage insights

2. **👥 Age-Based Analysis**
   - Generational behavior patterns (Gen Z, Millennials, Gen X)
   - Interactive variable selection
   - Streaming habits by age groups

3. **🌍 Country Analysis**
   - Global streaming patterns with country flags
   - Top performing regions
   - Cross-cultural music preferences

4. **🎼 Genre Preferences**
   - Most popular music genres
   - Genre distribution by country
   - Emerging trends identification

5. **⏰ Listening Time Analysis**
   - Peak listening hours
   - Generational listening patterns
   - Time-based user behavior

6. **🔍 Strategic Insights**
   - Data-driven business recommendations
   - Implementation roadmap
   - Revenue optimization strategies

### 🎨 Dashboard Highlights

- **Interactive Visualizations**: Plotly-powered charts with hover effects and zoom capabilities
- **Real-time Filtering**: Dynamic data exploration with multiple filter options
- **Professional Design**: Clean, corporate-ready interface suitable for stakeholder presentations
- **Mobile Responsive**: Optimized for different screen sizes
- **Export Ready**: Charts can be downloaded for presentations

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sesion12proyecto-musictrends.git
   cd sesion12proyecto-musictrends
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv .venv

   # On Windows
   .venv\Scripts\activate

   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**
   ```bash
   cd panel
   streamlit run app.py
   ```

5. **Open in browser**
   - The dashboard will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in the terminal



## 📊 Dataset Information

### Data Source
- **File**: `Global_Music_Streaming_Listener_Preferences.csv`
- **Records**: 100,000+ user profiles
- **Time Period**: 2018-2024
- **Geography**: Global coverage across 50+ countries

### Key Variables
- **Demographics**: Age, Country
- **Behavior**: Minutes streamed per day, Songs liked, Repeat rate
- **Preferences**: Top genre, Most played artist, Listening time
- **Platform**: Streaming service, Subscription type
- **Engagement**: Weekly engagement, Discovery metrics

## 🔬 Analysis Methodology

### 1. **Data Preparation**
- Data cleaning and quality assessment
- Missing value handling
- Feature engineering (age groups, segments)

### 2. **Exploratory Data Analysis**
- Univariate and bivariate analysis
- Correlation analysis
- Trend identification

### 3. **User Segmentation**
- Generational cohort analysis
- Behavioral clustering
- Geographic segmentation

### 4. **Strategic Analysis**
- Market opportunity identification
- Competitive landscape assessment
- Revenue optimization strategies

## 📈 Key Insights Summary

### 🎯 User Demographics
- **Age Distribution**: Balanced across generations with slight Millennial dominance
- **Geographic Spread**: Strong representation from North America, Europe, and emerging markets
- **Platform Preferences**: Diverse usage across major streaming platforms

### 🎵 Listening Behaviors
- **Genre Diversity**: Pop, Rock, and Hip-Hop dominate globally with regional variations
- **Temporal Patterns**: Evening listening peaks with generational differences
- **Engagement Levels**: High repeat listening rates indicate strong user loyalty

### 🌍 Market Opportunities
- **Emerging Markets**: Significant growth potential in underrepresented regions
- **Demographic Gaps**: Opportunities in specific age segments
- **Content Diversification**: Potential for genre expansion and localization

## 💼 Business Applications

### For Music Industry Executives
- **Strategic Planning**: Data-driven market expansion decisions
- **Content Strategy**: Genre and artist investment priorities
- **User Acquisition**: Targeted marketing campaign insights

### For Streaming Platforms
- **Feature Development**: User experience optimization
- **Personalization**: Enhanced recommendation algorithms
- **Market Penetration**: Geographic expansion strategies

### For Artists & Labels
- **Audience Analysis**: Fan demographic understanding
- **Release Strategy**: Optimal timing and platform selection
- **Market Entry**: New territory expansion planning

## 🛠️ Technical Implementation

### Technologies Used
- **Frontend**: Streamlit (Interactive dashboard)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Analysis**: Jupyter Notebooks
- **Deployment**: Local server (expandable to cloud)

### Performance Optimizations
- **Caching**: `@st.cache_data` for efficient data loading
- **Lazy Loading**: Progressive chart rendering
- **Memory Management**: Optimized data structures

## 📱 Usage Guide

### Navigation
1. **Sidebar Controls**: Use the left panel to switch between analysis sections
2. **Interactive Charts**: Click, zoom, and hover for detailed information
3. **Variable Selection**: Use dropdowns to explore different metrics
4. **Export Options**: Download charts using Plotly's built-in tools

### Best Practices for Presentations
- Start with the **Overview** section for context
- Use **Age Analysis** to discuss demographic trends
- Highlight **Country Analysis** for global market insights
- Conclude with **Strategic Insights** for actionable recommendations

## 🤝 Contributing

We welcome contributions to enhance the dashboard and analysis!

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Enhancement
- Additional visualization types
- Advanced statistical analysis
- Machine learning predictions
- Real-time data integration
- Cloud deployment setup

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♀️ Support

For questions, issues, or suggestions:

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact the development team

## 🔄 Version History

- **v1.0.0** - Initial release with core dashboard functionality
- **v1.1.0** - Enhanced visualizations and performance improvements
- **v1.2.0** - Added strategic insights and recommendations section

## 🏆 Acknowledgments

- **Data Source**: Music streaming platforms and industry reports
- **Visualization Libraries**: Plotly team for excellent charting capabilities
- **Streamlit Community**: For the amazing dashboard framework
- **Contributors**: All team members who made this project possible

---

<div align="center">

**🎵 Transform Data into Music Industry Intelligence 🎵**

[View Dashboard](http://localhost:8501) • [Report Issues](https://github.com/yourusername/sesion12proyecto-musictrends/issues) • [Request Features](https://github.com/yourusername/sesion12proyecto-musictrends/discussions)

</div>