# 🎵 Music Streaming Trends Analysis Dashboard

![Music Dashboard](https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Data Analysis](https://img.shields.io/badge/Data-Analysis-green?style=for-the-badge&logo=pandas)
[![Open in Streamlit](https://img.shields.io/badge/Streamlit-Open%20App-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white)](https://adp7ebd2nzhdfdu3nkvsj2.streamlit.app/)

## 📋 Project Overview

This project provides a comprehensive analysis of global music streaming trends from 2018-2024, featuring an interactive Streamlit dashboard that transforms complex data insights into actionable business intelligence for the music industry.

### 🎯 Objectives

- **Analyze** global music streaming patterns and user behavior
- **Identify** key trends across demographics, genres, and geographical regions
- **Develop** strategic recommendations for music industry stakeholders
- **Present** findings through an intuitive, interactive dashboard suitable for executive presentations

## 🏗️ Repository Structure

```
📁 musictrends/
├── 📂 data/                    # Dataset(s)
│   └── Global_Music_Streaming_Listener_Preferences.csv
├── 📂 notebooks/               # Jupyter notebooks for analysis
│   └── music_trends_analysis_clean.ipynb
├── 📂 panel/                   # Streamlit dashboard
│   └── app.py
├── .gitattributes             # Git attributes configuration
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

## 🔍 Key Features

### 📊 Interactive Dashboard Sections

1. **📈 Dataset Overview**
   - Headline metrics, data shape, and sample composition
   - Platform distribution and top countries by users
   - Data quality cues and quick-glance KPIs

2. **👥 Age-Based Analysis**
   - Individual-age view with generation bands (Gen Z, Millennials, Gen X)
   - Metrics: Minutes/day, Songs Liked, Discover Weekly Engagement (%), Repeat Song Rate (%)
   - Generation insights and variable ranges

3. **🌍 Country Analysis**
   - Country rankings for key metrics with flag annotations
   - Top 5 leaders by metric and sample size transparency
   - Identification of expansion “white spaces”

4. **🎼 Genre Preferences**
   - Top genres overall and by country (interactive grouped bars)
   - Coverage of Top-N and genre diversity indicators
   - Regional preferences for localized content strategy

5. **⏰ Listening Time Analysis**
   - Global distribution (Morning/Afternoon/Night)
   - Breakdown by country and by age/generation
   - Timing recommendations for notifications and releases

6. **📱 Platforms by Generation**
   - Platform preference split across Gen Z, Millennials, Gen X
   - Platform dominance and positioning cues

7. **🗺️ Unified Choropleth Map**
   - Country-level map switchable across quantitative metrics and total users
   - Quick identification of concentration and opportunity zones

8. **📈 Correlation Analysis**
   - Heatmap of numerical variables and strongest pairs
   - Guides for hypothesis generation and A/B test ideas

9. **🧭 Strategic Insights**
   - Data-driven recommendations, roadmap, and monetization levers
   - KPIs for growth, engagement, revenue, and content

### 🎨 Dashboard Highlights

- **Interactive Visualizations**: Plotly-powered charts with hover effects and zoom capabilities
- **Real-time Filtering**: Dynamic data exploration with multiple filter options
- **Professional Design**: Clean, corporate-ready interface suitable for stakeholder presentations
- **Mobile Responsive**: Optimized for different screen sizes
- **Export Ready**: Charts can be downloaded for presentations

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jufercar/musictrends.git
   cd musictrends
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
- **Records**: ~5,000 users
- **Time Period**: 2018–2024
- **Geography**: Global coverage across 50+ countries
- **Source**: Kaggle – Global Music Streaming Trends and Listener Insights
   (https://www.kaggle.com/datasets/atharvasoundankar/global-music-streaming-trends-and-listener-insights)

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

## 📐 Statistical Methods (Summary)

The analysis and dashboard leverage a practical set of statistical tests and diagnostics (via NumPy/Pandas/SciPy) to support decisions:

- Normality tests: Shapiro–Wilk, D’Agostino’s K², Anderson–Darling
- Variance homogeneity: Levene’s test
- Mean/median comparisons: Independent t-test, Mann–Whitney U, Kruskal–Wallis
- Association: Chi-square test of independence (categoricals)
- Correlation: Pearson (linear), Spearman (rank, monotonic)
- Uncertainty: Standard Error of the Mean (SEM), Q–Q plots for distribution checks

Interpretation principles used in the project:
- Prefer non-parametric tests when normality/homoscedasticity is not met
- Emphasize effect sizes and practical significance alongside p-values
- Use correlation analysis to ideate product/marketing experiments (not to infer causality)

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
- **Data Processing**: Pandas, NumPy, SciPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Analysis**: Jupyter Notebooks
- **Deployment**: Local server and Streamlit Cloud ready

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

- **v1.0.0** – Initial release

## 🏆 Acknowledgments

- **Dataset (Kaggle)**: Global Music Streaming Trends and Listener Insights – by Atharva Soundankar
   https://www.kaggle.com/datasets/atharvasoundankar/global-music-streaming-trends-and-listener-insights
   Please credit the dataset author and Kaggle page in any public use.
- **Visualization Libraries**: Plotly team for excellent charting capabilities
- **Streamlit Community**: For the amazing dashboard framework
- **Contributors**: All team members who made this project possible

---

<div align="center">

**🎵 Transform Data into Music Industry Intelligence 🎵**

[View Dashboard](http://localhost:8501) • [Report Issues](https://github.com/jufercar/musictrends/issues) • [Request Features](https://github.com/jufercar/musictrends/discussions)

</div>