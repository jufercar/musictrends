import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.colors as pc
from scipy import stats
from scipy.stats import (shapiro, normaltest, anderson, levene, ttest_ind, 
                        mannwhitneyu, kruskal, chi2_contingency, pearsonr, 
                        spearmanr, sem, probplot)
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Music Trends Analysis",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling (Light Theme)
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        border: 1px solid #e1e5e9;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #1a1a1a;
    }
    .insight-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2196F3;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        color: #1a1a1a;
    }
    .stSelectbox > div > div > div {
        background-color: #ffffff;
        border: 1px solid #ced4da;
        color: #1a1a1a;
    }
    /* Ensure all text is dark */
    .stMarkdown, .stText {
        color: #1a1a1a !important;
    }
    /* Make sidebar lighter */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    /* Fix metric labels */
    .metric-container label {
        color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the music streaming data"""
    import os
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level and then into data folder
        data_path = os.path.join(os.path.dirname(script_dir), 'data', 'Global_Music_Streaming_Listener_Preferences.csv')
        
        # Verify file exists
        if not os.path.exists(data_path):
            # Try alternative paths for different deployment scenarios
            alternative_paths = [
                os.path.join(script_dir, '..', 'data', 'Global_Music_Streaming_Listener_Preferences.csv'),
                os.path.join(os.getcwd(), 'data', 'Global_Music_Streaming_Listener_Preferences.csv'),
                'data/Global_Music_Streaming_Listener_Preferences.csv'
            ]
            
            for alt_path in alternative_paths:
                if os.path.exists(alt_path):
                    data_path = alt_path
                    break
            else:
                raise FileNotFoundError(f"Dataset not found. Tried paths: {[data_path] + alternative_paths}")
        
        df = pd.read_csv(data_path)
        
        # Validate dataset structure
        required_columns = ['Age', 'Country', 'Streaming Platform', 'Top Genre']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Create age groups
        df['Age_Group'] = pd.cut(df['Age'],
                                bins=[0, 25, 41, 100],
                                labels=['Gen Z (13-25)', 'Millennials (26-41)', 'Gen X (42-60)'])

        return df
        
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        st.info("Please ensure the dataset 'Global_Music_Streaming_Listener_Preferences.csv' is in the 'data' folder.")
        st.stop()

def create_country_flags_dict():
    """Country flags mapping"""
    return {
        'Canada': '🇨🇦', 'Australia': '🇦🇺', 'Germany': '🇩🇪', 'France': '🇫🇷',
        'Spain': '🇪🇸', 'Italy': '🇮🇹', 'Netherlands': '🇳🇱', 'Sweden': '🇸🇪',
        'Norway': '🇳🇴', 'Denmark': '🇩🇰', 'Finland': '🇫🇮', 'Brazil': '🇧🇷',
        'Mexico': '🇲🇽', 'Argentina': '🇦🇷', 'Japan': '🇯🇵', 'South Korea': '🇰🇷',
        'India': '🇮🇳', 'China': '🇨🇳', 'Russia': '🇷🇺', 'Poland': '🇵🇱',
        'Belgium': '🇧🇪', 'Switzerland': '🇨🇭', 'Austria': '🇦🇹', 'Portugal': '🇵🇹',
        'Ireland': '🇮🇪', 'New Zealand': '🇳🇿', 'South Africa': '🇿🇦', 'Chile': '🇨🇱',
        'Colombia': '🇨🇴', 'Peru': '🇵🇪', 'Turkey': '🇹🇷', 'Greece': '🇬🇷',
        'Czech Republic': '🇨🇿', 'Hungary': '🇭🇺', 'Romania': '🇷🇴', 'Thailand': '🇹🇭',
        'Vietnam': '🇻🇳', 'Philippines': '🇵🇭', 'Indonesia': '🇮🇩', 'Malaysia': '🇲🇾',
        'Singapore': '🇸🇬', 'Israel': '🇮🇱', 'UAE': '🇦🇪', 'Saudi Arabia': '🇸🇦',
        'Egypt': '🇪🇬', 'Nigeria': '🇳🇬', 'Kenya': '🇰🇪', 'Morocco': '🇲🇦',
        'USA': '🇺🇸', 'UK': '🇬🇧', 'United States': '🇺🇸', 'United Kingdom': '🇬🇧'
    }

def create_age_analysis(df):
    """Create interactive age-based analysis chart"""
    # Define quantitative variables
    quantitative_vars = ['Minutes Streamed Per Day', 'Number of Songs Liked',
                        'Discover Weekly Engagement (%)', 'Repeat Song Rate (%)']

    # Filter available variables
    available_vars = [var for var in quantitative_vars if var in df.columns]

    if not available_vars:
        st.error("No quantitative variables found for age analysis")
        return None

    # Generation colors
    generation_colors = {
        'Gen Z (13-25)': '#FF6B6B',
        'Millennials (26-41)': '#4ECDC4',
        'Gen X (42-60)': '#45B7D1'
    }

    # Prepare data for individual ages
    age_data = []
    for age in range(13, 61):
        age_subset = df[df['Age'] == age]
        if len(age_subset) > 0:
            if age <= 25:
                generation = 'Gen Z (13-25)'
                color = generation_colors['Gen Z (13-25)']
            elif age <= 41:
                generation = 'Millennials (26-41)'
                color = generation_colors['Millennials (26-41)']
            else:
                generation = 'Gen X (42-60)'
                color = generation_colors['Gen X (42-60)']

            age_stats = {
                'Age': age,
                'Generation': generation,
                'Color': color,
                'Count': len(age_subset)
            }
            for var in available_vars:
                age_stats[var] = age_subset[var].mean()

            age_data.append(age_stats)

    age_df = pd.DataFrame(age_data)

    return age_df, available_vars, generation_colors

def create_country_analysis(df):
    """Create country-based analysis"""
    country_flags = create_country_flags_dict()

    quantitative_vars = ['Minutes Streamed Per Day', 'Number of Songs Liked',
                        'Discover Weekly Engagement (%)', 'Repeat Song Rate (%)']
    available_vars = [var for var in quantitative_vars if var in df.columns]

    if not available_vars:
        st.error("No quantitative variables found for country analysis")
        return None

    # Prepare data by country
    country_data = []
    countries = df['Country'].unique()
    colors = pc.qualitative.Set3 + pc.qualitative.Pastel + pc.qualitative.Set1

    for i, country in enumerate(countries):
        country_subset = df[df['Country'] == country]
        if len(country_subset) > 0:
            flag = country_flags.get(country, '🌍')
            color = colors[i % len(colors)]

            country_stats = {
                'Country': country,
                'Flag': flag,
                'Country_Flag': f"{flag} {country}",
                'Color': color,
                'Count': len(country_subset)
            }
            for var in available_vars:
                country_stats[var] = country_subset[var].mean()

            country_data.append(country_stats)

    country_df = pd.DataFrame(country_data)
    return country_df, available_vars

def create_listening_time_analysis(df):
    """Create listening time preferences analysis"""
    listening_time_col = 'Listening Time (Morning/Afternoon/Night)'

    if listening_time_col not in df.columns:
        st.error("Listening time column not found")
        return None

    # Time period colors
    time_colors = {
        'Morning': '#FFD700',
        'Afternoon': '#FF8C00',
        'Night': '#4169E1'
    }

    # Global distribution
    global_listening = df[listening_time_col].value_counts()
    global_percentages = (global_listening / len(df) * 100).round(1)

    global_df = pd.DataFrame({
        'Time_Period': global_listening.index,
        'Count': global_listening.values,
        'Percentage': global_percentages.values
    })

    return global_df, time_colors

def create_streaming_platform_analysis(df):
    """Create streaming platform preferences analysis by generation"""
    if 'Streaming Platform' not in df.columns or 'Age_Group' not in df.columns:
        st.error("Streaming Platform or Age_Group column not found")
        return None

    # Create cross-tabulation for generations and streaming platforms
    platform_gen_counts = df.groupby(['Age_Group', 'Streaming Platform']).size().reset_index(name='Count')
    gen_totals = df.groupby('Age_Group').size().reset_index(name='Total')
    platform_gen_counts = platform_gen_counts.merge(gen_totals, on='Age_Group')
    platform_gen_counts['Percentage'] = (platform_gen_counts['Count'] / platform_gen_counts['Total'] * 100).round(1)

    return platform_gen_counts

def create_unified_choropleth_data(df):
    """Create unified data for interactive choropleth maps with multiple variables"""
    if 'Country' not in df.columns:
        st.error("Country column not found")
        return None

    # Country to ISO code mapping
    country_iso_mapping = {
        'USA': 'USA',
        'UK': 'GBR', 
        'Canada': 'CAN',
        'Australia': 'AUS',
        'Germany': 'DEU',
        'France': 'FRA',
        'Brazil': 'BRA',
        'Japan': 'JPN',
        'South Korea': 'KOR',
        'India': 'IND'
    }
    
    # Define quantitative variables that exist in the dataset
    quantitative_vars = ['Minutes Streamed Per Day', 'Number of Songs Liked', 
                        'Discover Weekly Engagement (%)', 'Repeat Song Rate (%)']
    available_quantitative = [var for var in quantitative_vars if var in df.columns]
    
    # Calculate comprehensive data for each country
    choropleth_data = []
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country]
        if not country_data.empty:
            iso_code = country_iso_mapping.get(country, country)
            total_users = len(country_data)
            
            country_stats = {
                'Country': country,
                'ISO_Code': iso_code,
                'Total Users': total_users
            }
            
            # Add quantitative variables (averages)
            for var in available_quantitative:
                country_stats[var] = country_data[var].mean().round(1)
            
            # Add most popular genre if available
            if 'Top Genre' in df.columns:
                most_popular_genre = country_data['Top Genre'].value_counts().index[0]
                genre_percentage = (country_data['Top Genre'].value_counts().iloc[0] / total_users * 100).round(1)
                country_stats['Most Popular Genre'] = most_popular_genre
                country_stats['Genre Percentage'] = genre_percentage
            
            # Add most popular artist if available
            if 'Most Played Artist' in df.columns:
                most_popular_artist = country_data['Most Played Artist'].value_counts().index[0]
                artist_percentage = (country_data['Most Played Artist'].value_counts().iloc[0] / total_users * 100).round(1)
                country_stats['Most Popular Artist'] = most_popular_artist
                country_stats['Artist Percentage'] = artist_percentage
            
            choropleth_data.append(country_stats)
    
    return pd.DataFrame(choropleth_data), available_quantitative

def main():
    # Load data
    try:
        df = load_data()
    except FileNotFoundError as e:
        st.error(f"Dataset not found. Please ensure 'Global_Music_Streaming_Listener_Preferences.csv' is in the data folder.")
        st.error(f"Looking for file at: {e}")
        st.stop()

    # Header
    st.markdown('<h1 class="main-header">🎵 Music Streaming Trends Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Global Music Streaming Analysis (2018-2024)</p>', unsafe_allow_html=True)
    
    # Author and creation info
    st.markdown('''
    <div style="text-align: center; margin: 1rem 0; padding: 0.5rem; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;">
        <p style="margin: 0; font-size: 0.9rem; color: #495057;">
            <strong> </strong> J. Fern&#225;ndez Carrillo &nbsp;•&nbsp; 
            <strong> </strong> Octubre 2025
        </p>
    </div>
    ''', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.image("https://img.icons8.com/color/96/000000/music.png", width=80)
    st.sidebar.title("🎶 Dashboard Controls")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Users", f"{df.shape[0]:,}")

    with col2:
        st.metric("Countries", f"{df['Country'].nunique()}")

    with col3:
        st.metric("Avg Age", f"{df['Age'].mean():.1f} years")

    with col4:
        avg_streaming = df['Minutes Streamed Per Day'].mean() if 'Minutes Streamed Per Day' in df.columns else 0
        st.metric("Avg Daily Streaming", f"{avg_streaming:.0f} min")

    # Analysis sections
    analysis_option = st.sidebar.selectbox(
        "Select Analysis",
        ["📊 Overview", "👥 Age Analysis", "🌍 Country Analysis",
         "🎼 Genre Preferences", "📱 Platform Analysis", "🗺️ Geographic Maps", "⏰ Listening Times", "📈 Statistical Analysis", "🔍 Strategic Insights"]
    )

    if analysis_option == "📊 Overview":
        st.header("📊 Dataset Overview")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Dataset Statistics")
            st.markdown(f"""
            <div class="metric-card">
                <h4>📈 Data Coverage</h4>
                <p><strong>Total Records:</strong> {df.shape[0]:,}</p>
                <p><strong>Variables:</strong> {df.shape[1]}</p>
                <p><strong>Age Range:</strong> {df['Age'].min()}-{df['Age'].max()} years</p>
                <p><strong>Countries:</strong> {df['Country'].nunique()}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Top countries
            top_countries = df['Country'].value_counts().head(10)
            fig_countries = px.bar(
                x=top_countries.values,
                y=top_countries.index,
                orientation='h',
                title="Top 10 Countries by Users",
                labels={'x': 'Number of Users', 'y': 'Country'}
            )
            fig_countries.update_layout(height=400)
            st.plotly_chart(fig_countries, use_container_width=True)

        # Platform distribution
        if 'Streaming Platform' in df.columns:
            st.subheader("Streaming Platform Distribution")
            platform_counts = df['Streaming Platform'].value_counts()
            fig_platforms = px.pie(
                values=platform_counts.values,
                names=platform_counts.index,
                title="Market Share by Streaming Platform"
            )
            st.plotly_chart(fig_platforms, use_container_width=True)

    elif analysis_option == "👥 Age Analysis":
        st.header("👥 Age-Based Analysis")

        result = create_age_analysis(df)
        if result:
            age_df, available_vars, generation_colors = result

            # Variable selector
            selected_var = st.selectbox("Select Variable", available_vars)

            # Create age chart
            fig = px.bar(
                age_df,
                x='Age',
                y=selected_var,
                color='Generation',
                color_discrete_map=generation_colors,
                title=f"{selected_var} by Age and Generation",
                hover_data=['Count']
            )

            # Add generation background regions
            fig.add_vrect(x0=12.5, x1=25.5, fillcolor=generation_colors['Gen Z (13-25)'],
                          opacity=0.1, layer="below", line_width=0)
            fig.add_vrect(x0=25.5, x1=41.5, fillcolor=generation_colors['Millennials (26-41)'],
                          opacity=0.1, layer="below", line_width=0)
            fig.add_vrect(x0=41.5, x1=60.5, fillcolor=generation_colors['Gen X (42-60)'],
                          opacity=0.1, layer="below", line_width=0)

            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)

            # Generation insights
            st.subheader("Generation Insights")
            col1, col2, col3 = st.columns(3)

            for i, generation in enumerate(['Gen Z (13-25)', 'Millennials (26-41)', 'Gen X (42-60)']):
                gen_data = age_df[age_df['Generation'] == generation]
                avg_value = gen_data[selected_var].mean() if not gen_data.empty else 0
                user_count = gen_data['Count'].sum() if not gen_data.empty else 0
                
                # Get Minutes Streamed Per Day for this generation from original data
                original_gen_data = df[df['Age_Group'] == generation]
                avg_minutes = 0
                if not original_gen_data.empty and 'Minutes Streamed Per Day' in df.columns:
                    avg_minutes = original_gen_data['Minutes Streamed Per Day'].mean()

                with [col1, col2, col3][i]:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>{generation}</h4>
                        <p><strong>Avg {selected_var}:</strong> {avg_value:.1f}</p>
                        <p><strong>Minutes Streamed Per Day:</strong> {avg_minutes:.1f}</p>
                        <p><strong>Total Users:</strong> {user_count:,}</p>
                    </div>
                    """, unsafe_allow_html=True)

    elif analysis_option == "🌍 Country Analysis":
        st.header("🌍 Country-Based Analysis")

        result = create_country_analysis(df)
        if result:
            country_df, available_vars = result

            # Variable selector
            selected_var = st.selectbox("Select Variable", available_vars)

            # Sort by selected variable
            sorted_df = country_df.sort_values(selected_var, ascending=False)

            # Create country chart
            fig = px.bar(
                sorted_df,
                x='Country_Flag',
                y=selected_var,
                color=selected_var,
                color_continuous_scale='viridis',
                title=f"Countries by {selected_var}",
                hover_data=['Count'],
                labels={'Country_Flag': 'Country'}
            )

            fig.update_layout(
                height=600,
                xaxis_tickangle=-45,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

            # Top countries insights
            st.subheader(f"Top 5 Countries by {selected_var}")
            top_5 = sorted_df.head(5)

            for _, row in top_5.iterrows():
                st.markdown(f"""
                <div class="insight-box">
                    <strong>{row['Flag']} {row['Country']}</strong>: {row[selected_var]:.1f}
                    ({row['Count']:,} users)
                </div>
                """, unsafe_allow_html=True)

    elif analysis_option == "🎼 Genre Preferences":
        st.header("🎼 Music Genre Analysis")

        if 'Top Genre' in df.columns:
            # Genre distribution
            genre_counts = df['Top Genre'].value_counts()

            fig_genres = px.bar(
                x=genre_counts.index,
                y=genre_counts.values,
                title="Music Genres Distribution",
                color=genre_counts.values,
                color_continuous_scale='viridis',
                labels={'x': 'Genre', 'y': 'Number of Users'}
            )

            fig_genres.update_layout(
                height=500,
                xaxis_tickangle=-45,
                showlegend=False
            )
            st.plotly_chart(fig_genres, use_container_width=True)

            # Genre preferences by age groups
            if 'Age_Group' in df.columns:
                st.subheader("Genre Preferences by Generation")

                # Create cross-tabulation for age groups and genres
                age_genre_counts = df.groupby(['Age_Group', 'Top Genre']).size().reset_index(name='Count')
                age_totals = df.groupby('Age_Group').size().reset_index(name='Total')
                age_genre_counts = age_genre_counts.merge(age_totals, on='Age_Group')
                age_genre_counts['Percentage'] = (age_genre_counts['Count'] / age_genre_counts['Total'] * 100).round(1)

                # Generation colors
                generation_colors = {
                    'Gen Z (13-25)': '#FF6B6B',
                    'Millennials (26-41)': '#4ECDC4',
                    'Gen X (42-60)': '#45B7D1'
                }

                fig_age_genre = px.bar(
                    age_genre_counts,
                    x='Age_Group',
                    y='Percentage',
                    color='Top Genre',
                    title='Genre Preferences by Generation',
                    barmode='group',
                    hover_data=['Count', 'Total'],
                    labels={'Age_Group': 'Generation', 'Percentage': 'Percentage of Users'}
                )

                fig_age_genre.update_layout(
                    height=600,
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_age_genre, use_container_width=True)

            # Genre by country analysis
            if 'Country' in df.columns:
                st.subheader("Genre Preferences by Country")

                # Get all countries and top genres
                top_countries = df['Country'].value_counts().index.tolist()
                top_genres = df['Top Genre'].value_counts().head(6).index.tolist()

                # Filter data
                filtered_df = df[
                    (df['Country'].isin(top_countries)) &
                    (df['Top Genre'].isin(top_genres))
                ]

                # Create cross-tabulation
                country_genre_counts = filtered_df.groupby(['Country', 'Top Genre']).size().reset_index(name='Count')
                country_totals = filtered_df.groupby('Country').size().reset_index(name='Total')
                country_genre_counts = country_genre_counts.merge(country_totals, on='Country')
                country_genre_counts['Percentage'] = (country_genre_counts['Count'] / country_genre_counts['Total'] * 100).round(1)

                # Add flags
                country_flags = create_country_flags_dict()
                country_genre_counts['Country_Flag'] = country_genre_counts['Country'].apply(
                    lambda x: f"{country_flags.get(x, '🌍')} {x}"
                )

                fig_country_genre = px.bar(
                    country_genre_counts,
                    x='Country_Flag',
                    y='Percentage',
                    color='Top Genre',
                    title='Genre Preferences by Country',
                    barmode='group',
                    hover_data=['Count', 'Total'],
                    labels={'Country_Flag': 'Country', 'Percentage': 'Percentage of Users (%)'}
                )

                fig_country_genre.update_layout(
                    height=600,
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_country_genre, use_container_width=True)
        else:
            st.error("Genre data not available in the dataset")

    elif analysis_option == "📱 Platform Analysis":
        st.header("📱 Streaming Platform Analysis")

        if 'Streaming Platform' in df.columns:
            # Overall platform distribution
            st.subheader("Overall Platform Distribution")
            platform_counts = df['Streaming Platform'].value_counts()

            fig_platforms = px.pie(
                values=platform_counts.values,
                names=platform_counts.index,
                title="Market Share by Streaming Platform",
                hover_data=[platform_counts.values]
            )
            
            fig_platforms.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>' +
                             'Users: %{value:,}<br>' +
                             'Percentage: %{percent}<br>' +
                             '<extra></extra>'
            )
            st.plotly_chart(fig_platforms, use_container_width=True)

            # Platform preferences by generation
            if 'Age_Group' in df.columns:
                st.subheader("Platform Preferences by Generation")

                result = create_streaming_platform_analysis(df)
                if result is not None:
                    platform_gen_counts = result

                    # Create grouped bar chart
                    fig_platform_gen = px.bar(
                        platform_gen_counts,
                        x='Age_Group',
                        y='Percentage',
                        color='Streaming Platform',
                        title='Streaming Platform Preferences by Generation',
                        barmode='group',
                        hover_data=['Count', 'Total'],
                        labels={'Age_Group': 'Generation', 'Percentage': 'Percentage of Users'}
                    )

                    fig_platform_gen.update_layout(
                        height=600,
                        xaxis_tickangle=0,
                        legend=dict(
                            orientation="v",
                            yanchor="top",
                            y=1,
                            xanchor="left",
                            x=1.02
                        ),
                        xaxis=dict(gridcolor='lightgray'),
                        yaxis=dict(gridcolor='lightgray'),
                        plot_bgcolor='white',
                        margin=dict(r=150)
                    )
                    st.plotly_chart(fig_platform_gen, use_container_width=True)

                    # Platform insights by generation
                    st.subheader("Platform Insights by Generation")
                    col1, col2, col3 = st.columns(3)

                    generations = ['Gen Z (13-25)', 'Millennials (26-41)', 'Gen X (42-60)']
                    for i, generation in enumerate(generations):
                        gen_data = platform_gen_counts[platform_gen_counts['Age_Group'] == generation]
                        if not gen_data.empty:
                            top_platform_row = gen_data.loc[gen_data['Percentage'].idxmax()]
                            
                            with [col1, col2, col3][i]:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <h4>{generation}</h4>
                                    <p><strong>Preferred Platform:</strong> {top_platform_row['Streaming Platform']}</p>
                                    <p><strong>Usage:</strong> {top_platform_row['Percentage']:.1f}%</p>
                                    <p><strong>Total Users:</strong> {top_platform_row['Total']:,}</p>
                                </div>
                                """, unsafe_allow_html=True)

                    # Platform dominance analysis
                    st.subheader("Platform Dominance Analysis")
                    
                    for platform in df['Streaming Platform'].unique():
                        platform_data = platform_gen_counts[platform_gen_counts['Streaming Platform'] == platform]
                        if not platform_data.empty:
                            top_gen_row = platform_data.loc[platform_data['Percentage'].idxmax()]
                            total_platform_users = df[df['Streaming Platform'] == platform].shape[0]
                            
                            st.markdown(f"""
                            <div class="insight-box">
                                <strong>📱 {platform}</strong>: Most popular with <strong>{top_gen_row['Age_Group']}</strong> 
                                ({top_gen_row['Percentage']:.1f}% of that generation, {total_platform_users:,} total users)
                            </div>
                            """, unsafe_allow_html=True)

            # Subscription type analysis if available
            if 'Subscription Type' in df.columns:
                st.subheader("Subscription Type Distribution")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Overall subscription distribution
                    sub_counts = df['Subscription Type'].value_counts()
                    fig_subs = px.pie(
                        values=sub_counts.values,
                        names=sub_counts.index,
                        title="Premium vs Free Users",
                        color_discrete_map={'Premium': '#1f77b4', 'Free': '#ff7f0e'}
                    )
                    st.plotly_chart(fig_subs, use_container_width=True)
                
                with col2:
                    # Subscription by generation
                    if 'Age_Group' in df.columns:
                        sub_gen_counts = df.groupby(['Age_Group', 'Subscription Type']).size().reset_index(name='Count')
                        sub_gen_totals = df.groupby('Age_Group').size().reset_index(name='Total')
                        sub_gen_counts = sub_gen_counts.merge(sub_gen_totals, on='Age_Group')
                        sub_gen_counts['Percentage'] = (sub_gen_counts['Count'] / sub_gen_counts['Total'] * 100).round(1)
                        
                        fig_sub_gen = px.bar(
                            sub_gen_counts,
                            x='Age_Group',
                            y='Percentage',
                            color='Subscription Type',
                            title='Subscription Type by Generation',
                            barmode='group',
                            color_discrete_map={'Premium': '#1f77b4', 'Free': '#ff7f0e'}
                        )
                        st.plotly_chart(fig_sub_gen, use_container_width=True)

        else:
            st.error("Streaming Platform data not available in the dataset")

    elif analysis_option == "🗺️ Geographic Maps":
        st.header("🗺️ Interactive Geographic Analysis")

        if 'Country' in df.columns:
            choropleth_data, available_quantitative = create_unified_choropleth_data(df)
            
            if choropleth_data is not None and not choropleth_data.empty:
                # Create all map variables list
                all_map_variables = available_quantitative + ['Total Users']
                if 'Most Popular Genre' in choropleth_data.columns:
                    all_map_variables.append('Most Popular Genre')
                if 'Most Popular Artist' in choropleth_data.columns:
                    all_map_variables.append('Most Popular Artist')
                
                st.subheader("🗺️ Unified Interactive Choropleth Map")
                st.write("Select different variables to explore various aspects of music streaming across countries.")
                
                # Variable selector
                selected_variable = st.selectbox(
                    "Select Variable to Display:",
                    options=available_quantitative + ['Total Users'],
                    index=0,
                    help="Choose which metric to visualize on the world map"
                )

                # Create the choropleth map
                color_scale = 'Blues' if selected_variable == 'Total Users' else 'Viridis'
                
                fig_unified = px.choropleth(
                    choropleth_data,
                    locations='ISO_Code',
                    color=selected_variable,
                    hover_name='Country',
                    color_continuous_scale=color_scale,
                    title=f'Interactive Country Analysis: {selected_variable}',
                    labels={selected_variable: selected_variable}
                )
                
                # Update layout
                fig_unified.update_layout(
                    geo=dict(
                        showframe=False,
                        showcoastlines=True,
                        projection_type='equirectangular'
                    ),
                    height=600
                )
                
                st.plotly_chart(fig_unified, use_container_width=True)
                
                # Insights section
                st.subheader(f"📊 {selected_variable} Analysis")
                
                # Top countries for selected variable
                if selected_variable in available_quantitative + ['Total Users']:
                    rankings = choropleth_data.sort_values(selected_variable, ascending=False)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**🏆 Top Countries by {selected_variable}:**")
                        for i, (_, row) in enumerate(rankings.head(5).iterrows(), 1):
                            if selected_variable == 'Total Users':
                                st.markdown(f"{i}. **{row['Country']}**: {row[selected_variable]:,}")
                            else:
                                st.markdown(f"{i}. **{row['Country']}**: {row[selected_variable]:.1f}")
                    
                    with col2:
                        st.markdown(f"**📈 {selected_variable} Statistics:**")
                        if selected_variable == 'Total Users':
                            st.metric("Total Users", f"{choropleth_data[selected_variable].sum():,}")
                            st.metric("Average per Country", f"{choropleth_data[selected_variable].mean():.0f}")
                            st.metric("Top Country", f"{rankings.iloc[0]['Country']} ({rankings.iloc[0][selected_variable]:,})")
                        else:
                            st.metric("Global Average", f"{choropleth_data[selected_variable].mean():.1f}")
                            st.metric("Highest Value", f"{choropleth_data[selected_variable].max():.1f}")
                            st.metric("Top Country", f"{rankings.iloc[0]['Country']} ({rankings.iloc[0][selected_variable]:.1f})")
                
                # Additional insights for categorical data
                if 'Most Popular Genre' in choropleth_data.columns:
                    st.subheader("🎵 Genre Insights by Country")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Most Popular Genre by Country:**")
                        for _, row in choropleth_data.iterrows():
                            st.markdown(f"• **{row['Country']}**: {row['Most Popular Genre']} ({row['Genre Percentage']:.1f}%)")
                    
                    with col2:
                        # Genre distribution summary
                        genre_summary = choropleth_data['Most Popular Genre'].value_counts()
                        st.markdown("**Genre Dominance Summary:**")
                        for genre, count in genre_summary.items():
                            st.markdown(f"• **{genre}**: Leading in {count} {'country' if count == 1 else 'countries'}")
                
                if 'Most Popular Artist' in choropleth_data.columns:
                    st.subheader("🎤 Artist Insights by Country")
                    
                    st.markdown("**Most Popular Artist by Country:**")
                    for _, row in choropleth_data.iterrows():
                        st.markdown(f"• **{row['Country']}**: {row['Most Popular Artist']} ({row['Artist Percentage']:.1f}%)")
                
                # Summary statistics
                st.subheader("🌍 Geographic Summary")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Countries Analyzed", len(choropleth_data))
                
                with col2:
                    st.metric("Available Variables", len(all_map_variables))
                
                with col3:
                    total_global_users = choropleth_data['Total Users'].sum()
                    st.metric("Total Global Users", f"{total_global_users:,}")

            else:
                st.error("Could not generate choropleth data - insufficient country data available")


    elif analysis_option == "⏰ Listening Times":
        st.header("⏰ Listening Time Preferences")

        result = create_listening_time_analysis(df)
        if result:
            global_df, time_colors = result

            # Global listening time distribution
            fig_global = px.pie(
                global_df,
                values='Count',
                names='Time_Period',
                title='Global Music Listening Preferences by Time of Day',
                color='Time_Period',
                color_discrete_map=time_colors
            )

            fig_global.update_layout(height=500)
            st.plotly_chart(fig_global, use_container_width=True)

            # Listening time by generation
            if 'Age_Group' in df.columns:
                st.subheader("Listening Time by Generation")

                listening_time_col = 'Listening Time (Morning/Afternoon/Night)'
                gen_time_counts = df.groupby(['Age_Group', listening_time_col]).size().reset_index(name='Count')
                gen_totals = df.groupby('Age_Group').size().reset_index(name='Total')
                gen_time_counts = gen_time_counts.merge(gen_totals, on='Age_Group')
                gen_time_counts['Percentage'] = (gen_time_counts['Count'] / gen_time_counts['Total'] * 100).round(1)

                fig_gen_time = px.bar(
                    gen_time_counts,
                    x='Age_Group',
                    y='Percentage',
                    color=listening_time_col,
                    title='Listening Time Preferences by Generation',
                    color_discrete_map=time_colors,
                    barmode='group'
                )

                fig_gen_time.update_layout(height=500)
                st.plotly_chart(fig_gen_time, use_container_width=True)

            # Time insights
            st.subheader("Key Insights")
            most_popular = global_df.loc[global_df['Count'].idxmax()]
            least_popular = global_df.loc[global_df['Count'].idxmin()]

            st.markdown(f"""
            <div class="insight-box">
                <h4>🕐 Peak Listening Time</h4>
                <p><strong>{most_popular['Time_Period']}</strong> is the most popular listening time with
                <strong>{most_popular['Count']:,}</strong> users ({most_popular['Percentage']:.1f}%)</p>
            </div>

            <div class="insight-box">
                <h4>🕐 Quiet Hours</h4>
                <p><strong>{least_popular['Time_Period']}</strong> has the fewest listeners with
                <strong>{least_popular['Count']:,}</strong> users ({least_popular['Percentage']:.1f}%)</p>
            </div>
            """, unsafe_allow_html=True)

    elif analysis_option == "📈 Statistical Analysis":
        st.header("📈 Advanced Statistical Analysis")
        
        st.markdown("""
        <div class="insight-box">
            <strong>Statistical Testing Suite</strong><br>
            This section provides comprehensive statistical analysis including distribution testing, 
            hypothesis testing, and correlation analysis to validate data-driven insights.
        </div>
        """, unsafe_allow_html=True)

        # Tab structure for different analyses
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribution Analysis", "🧪 Hypothesis Testing", "🔗 Correlation Analysis", "📏 Confidence Intervals"])
        
        with tab1:
            st.subheader("📊 Distribution Analysis")
            
            # Select numerical column for analysis
            numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numerical_cols:
                selected_col = st.selectbox(
                    "Select variable for distribution analysis:",
                    numerical_cols,
                    help="Choose a numerical variable to analyze its distribution"
                )
                
                data = df[selected_col].dropna()
                
                if len(data) > 0:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Descriptive statistics
                        st.write("**Descriptive Statistics:**")
                        stats_df = pd.DataFrame({
                            'Statistic': ['Count', 'Mean', 'Median', 'Std Dev', 'Skewness', 'Kurtosis', 'Min', 'Max'],
                            'Value': [
                                f"{len(data)}",
                                f"{data.mean():.3f}",
                                f"{data.median():.3f}",
                                f"{data.std():.3f}",
                                f"{stats.skew(data):.3f}",
                                f"{stats.kurtosis(data):.3f}",
                                f"{data.min():.3f}",
                                f"{data.max():.3f}"
                            ]
                        })
                        st.dataframe(stats_df, use_container_width=True)
                    
                    with col2:
                        # Histogram with normal curve overlay
                        fig_hist = px.histogram(
                            df, x=selected_col,
                            title=f'Distribution of {selected_col}',
                            nbins=30,
                            marginal="box"
                        )
                        
                        # Add normal curve
                        x_range = np.linspace(data.min(), data.max(), 100)
                        normal_curve = stats.norm.pdf(x_range, data.mean(), data.std())
                        normal_curve = normal_curve * len(data) * (data.max() - data.min()) / 30  # Scale to histogram
                        
                        fig_hist.add_trace(go.Scatter(
                            x=x_range, y=normal_curve,
                            mode='lines', name='Normal Distribution',
                            line=dict(color='red', width=2)
                        ))
                        
                        st.plotly_chart(fig_hist, use_container_width=True)
                    
                    # Normality tests
                    st.write("**Normality Tests:**")
                    
                    try:
                        # Shapiro-Wilk test (for smaller samples)
                        if len(data) <= 5000:
                            shapiro_stat, shapiro_p = shapiro(data)
                            shapiro_result = "✅ Normal" if shapiro_p > 0.05 else "❌ Not Normal"
                            st.write(f"- **Shapiro-Wilk Test**: statistic={shapiro_stat:.4f}, p-value={shapiro_p:.4f} → {shapiro_result}")
                        
                        # D'Agostino's normality test
                        dagostino_stat, dagostino_p = normaltest(data)
                        dagostino_result = "✅ Normal" if dagostino_p > 0.05 else "❌ Not Normal"
                        st.write(f"- **D'Agostino Test**: statistic={dagostino_stat:.4f}, p-value={dagostino_p:.4f} → {dagostino_result}")
                        
                        # Anderson-Darling test
                        anderson_result = anderson(data, dist='norm')
                        anderson_normal = "✅ Normal" if anderson_result.statistic < anderson_result.critical_values[2] else "❌ Not Normal"
                        st.write(f"- **Anderson-Darling Test**: statistic={anderson_result.statistic:.4f} → {anderson_normal}")
                        
                    except Exception as e:
                        st.warning(f"Some normality tests could not be performed: {str(e)}")

        with tab2:
            st.subheader("🧪 Hypothesis Testing")
            
            # Test selection
            test_type = st.selectbox(
                "Select test type:",
                ["Age differences between generations", "Streaming behavior by platform", "Genre-Country independence"],
                help="Choose the type of hypothesis test to perform"
            )
            
            if test_type == "Age differences between generations":
                if 'Age' in df.columns and 'Age_Group' in df.columns:
                    st.write("**Hypothesis**: There are significant age differences between generations")
                    
                    gen_z = df[df['Age_Group'] == 'Gen Z (13-25)']['Age'].dropna()
                    millennials = df[df['Age_Group'] == 'Millennials (26-41)']['Age'].dropna()
                    gen_x = df[df['Age_Group'] == 'Gen X (42-60)']['Age'].dropna()
                    
                    if len(gen_z) > 0 and len(millennials) > 0 and len(gen_x) > 0:
                        # ANOVA test
                        f_stat, f_p = stats.f_oneway(gen_z, millennials, gen_x)
                        anova_result = "✅ Significant" if f_p < 0.05 else "❌ Not Significant"
                        
                        st.write(f"**One-way ANOVA**: F-statistic={f_stat:.4f}, p-value={f_p:.4f} → {anova_result}")
                        
                        # Kruskal-Wallis test (non-parametric)
                        kruskal_stat, kruskal_p = kruskal(gen_z, millennials, gen_x)
                        kruskal_result = "✅ Significant" if kruskal_p < 0.05 else "❌ Not Significant"
                        
                        st.write(f"**Kruskal-Wallis Test**: H-statistic={kruskal_stat:.4f}, p-value={kruskal_p:.4f} → {kruskal_result}")
                        
                        # Box plot for visualization
                        fig_box = px.box(df, x='Age_Group', y='Age', title='Age Distribution by Generation')
                        st.plotly_chart(fig_box, use_container_width=True)
                    
            elif test_type == "Streaming behavior by platform":
                streaming_cols = [col for col in df.columns if ('stream' in col.lower() or 'minute' in col.lower()) and df[col].dtype in ['int64', 'float64']]
                
                if streaming_cols and 'Streaming Platform' in df.columns:
                    selected_streaming_col = st.selectbox("Select streaming variable:", streaming_cols)
                    
                    platforms = df['Streaming Platform'].unique()[:3]  # Test first 3 platforms
                    platform_data = []
                    
                    for platform in platforms:
                        platform_values = df[df['Streaming Platform'] == platform][selected_streaming_col].dropna()
                        if len(platform_values) > 0:
                            platform_data.append(platform_values)
                    
                    if len(platform_data) >= 2:
                        st.write(f"**Hypothesis**: There are significant differences in {selected_streaming_col} between platforms")
                        
                        if len(platform_data) == 2:
                            # Two-sample t-test
                            t_stat, t_p = ttest_ind(platform_data[0], platform_data[1])
                            t_result = "✅ Significant" if t_p < 0.05 else "❌ Not Significant"
                            st.write(f"**Two-sample t-test**: t-statistic={t_stat:.4f}, p-value={t_p:.4f} → {t_result}")
                            
                            # Mann-Whitney U test
                            u_stat, u_p = mannwhitneyu(platform_data[0], platform_data[1])
                            u_result = "✅ Significant" if u_p < 0.05 else "❌ Not Significant"
                            st.write(f"**Mann-Whitney U Test**: U-statistic={u_stat:.4f}, p-value={u_p:.4f} → {u_result}")
                        
                        elif len(platform_data) >= 3:
                            # ANOVA for multiple platforms
                            f_stat, f_p = stats.f_oneway(*platform_data)
                            anova_result = "✅ Significant" if f_p < 0.05 else "❌ Not Significant"
                            st.write(f"**One-way ANOVA**: F-statistic={f_stat:.4f}, p-value={f_p:.4f} → {anova_result}")
                        
                        # Box plot for visualization
                        fig_box = px.box(df, x='Streaming Platform', y=selected_streaming_col, 
                                       title=f'{selected_streaming_col} by Platform')
                        st.plotly_chart(fig_box, use_container_width=True)
                        
            elif test_type == "Genre-Country independence":
                if 'Top Genre' in df.columns and 'Country' in df.columns:
                    st.write("**Hypothesis**: Genre preferences are independent of country")
                    
                    # Create contingency table
                    contingency_table = pd.crosstab(df['Country'], df['Top Genre'])
                    
                    # Chi-square test
                    chi2, chi2_p, dof, expected = chi2_contingency(contingency_table)
                    chi2_result = "✅ Dependent" if chi2_p < 0.05 else "❌ Independent"
                    
                    st.write(f"**Chi-square Test**: χ²={chi2:.4f}, p-value={chi2_p:.4f}, df={dof} → {chi2_result}")
                    
                    # Cramér's V (effect size)
                    n = contingency_table.sum().sum()
                    cramers_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))
                    
                    effect_size = "Small" if cramers_v < 0.1 else "Medium" if cramers_v < 0.3 else "Large"
                    st.write(f"**Cramér's V (Effect Size)**: {cramers_v:.4f} → {effect_size}")
                    
                    # Show contingency table
                    st.write("**Contingency Table:**")
                    st.dataframe(contingency_table)

        with tab3:
            st.subheader("🔗 Correlation Analysis")
            
            numerical_cols_list = [col for col in numerical_cols if col in df.columns][:6]  # First 6 numerical columns
            
            if len(numerical_cols_list) >= 2:
                col1, col2 = st.columns(2)
                
                with col1:
                    var1 = st.selectbox("Select first variable:", numerical_cols_list, key="corr_var1")
                with col2:
                    var2 = st.selectbox("Select second variable:", 
                                      [col for col in numerical_cols_list if col != var1], key="corr_var2")
                
                # Remove missing values
                data1 = df[var1].dropna()
                data2 = df[var2].dropna()
                common_idx = data1.index.intersection(data2.index)
                
                if len(common_idx) > 3:
                    x = df.loc[common_idx, var1]
                    y = df.loc[common_idx, var2]
                    
                    # Pearson correlation
                    pearson_r, pearson_p = stats.pearsonr(x, y)
                    pearson_result = "✅ Significant" if pearson_p < 0.05 else "❌ Not Significant"
                    
                    # Spearman correlation
                    spearman_r, spearman_p = stats.spearmanr(x, y)
                    spearman_result = "✅ Significant" if spearman_p < 0.05 else "❌ Not Significant"
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Correlation Results:**")
                        st.write(f"- **Pearson r**: {pearson_r:.4f}, p-value: {pearson_p:.4f} → {pearson_result}")
                        st.write(f"- **Spearman ρ**: {spearman_r:.4f}, p-value: {spearman_p:.4f} → {spearman_result}")
                        
                        # Interpretation
                        if abs(pearson_r) < 0.3:
                            strength = "Weak"
                        elif abs(pearson_r) < 0.7:
                            strength = "Moderate"
                        else:
                            strength = "Strong"
                        
                        direction = "Positive" if pearson_r > 0 else "Negative"
                        st.write(f"**Interpretation**: {strength} {direction} correlation")
                    
                    with col2:
                        # Scatter plot
                        fig_scatter = px.scatter(
                            x=x, y=y,
                            title=f'{var1} vs {var2}',
                            labels={'x': var1, 'y': var2},
                            trendline="ols"
                        )
                        st.plotly_chart(fig_scatter, use_container_width=True)

        with tab4:
            st.subheader("📏 Confidence Intervals")
            
            if numerical_cols:
                selected_ci_col = st.selectbox(
                    "Select variable for confidence interval:",
                    numerical_cols,
                    help="Choose a numerical variable to calculate confidence intervals"
                )
                
                confidence_level = st.slider(
                    "Confidence Level (%)",
                    min_value=90, max_value=99, value=95, step=1
                ) / 100
                
                data = df[selected_ci_col].dropna()
                
                if len(data) > 0:
                    mean = data.mean()
                    std_error = stats.sem(data)
                    degrees_freedom = len(data) - 1
                    confidence_interval = stats.t.interval(confidence_level, degrees_freedom, mean, std_error)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Confidence Interval Results:**")
                        st.write(f"- **Sample Size**: {len(data):,}")
                        st.write(f"- **Mean**: {mean:.4f}")
                        st.write(f"- **Standard Error**: {std_error:.4f}")
                        st.write(f"- **{confidence_level*100:.0f}% Confidence Interval**: ({confidence_interval[0]:.4f}, {confidence_interval[1]:.4f})")
                        
                        margin_of_error = confidence_interval[1] - mean
                        st.write(f"- **Margin of Error**: ±{margin_of_error:.4f}")
                    
                    with col2:
                        # Visualization of confidence interval
                        fig_ci = go.Figure()
                        
                        # Add mean line
                        fig_ci.add_hline(y=mean, line_dash="solid", line_color="blue", 
                                       annotation_text=f"Mean: {mean:.4f}")
                        
                        # Add confidence interval
                        fig_ci.add_hrect(y0=confidence_interval[0], y1=confidence_interval[1],
                                       fillcolor="lightblue", opacity=0.3,
                                       annotation_text=f"{confidence_level*100:.0f}% CI")
                        
                        fig_ci.update_layout(
                            title=f"Confidence Interval for {selected_ci_col}",
                            yaxis_title=selected_ci_col,
                            showlegend=False,
                            height=400
                        )
                        
                        st.plotly_chart(fig_ci, use_container_width=True)

    elif analysis_option == "🔍 Strategic Insights":
        st.header("🔍 Strategic Insights & Recommendations")

        # Key findings
        st.subheader("🎯 Key Findings")

        findings = [
            f"Dataset covers **{df.shape[0]:,} users** across **{df['Country'].nunique()} countries**",
            f"User age ranges from **{df['Age'].min()}-{df['Age'].max()} years** with average of **{df['Age'].mean():.1f} years**",
            f"**{df['Top Genre'].value_counts().index[0]}** is the most popular genre" if 'Top Genre' in df.columns else "Genre data available",
            f"Most users prefer listening during **{df['Listening Time (Morning/Afternoon/Night)'].value_counts().index[0]}**" if 'Listening Time (Morning/Afternoon/Night)' in df.columns else "Listening time preferences analyzed"
        ]

        for finding in findings:
            st.markdown(f"• {finding}")

        # Strategic recommendations
        st.subheader("💼 Strategic Recommendations")

        recommendations = {
            "🎯 User Acquisition": [
                "Target underrepresented age segments with tailored marketing campaigns",
                "Develop age-specific playlists and content curation",
                "Partner with platforms popular among target demographics"
            ],
            "🎵 Content Strategy": [
                "Invest in emerging and underrepresented music genres",
                "Create genre-specific discovery algorithms",
                "Support local and regional artists to diversify catalog"
            ],
            "📱 User Experience": [
                "Develop personalized recommendation systems",
                "Implement social features for music sharing",
                "Create interactive features like live listening parties"
            ],
            "💰 Revenue Optimization": [
                "Implement tiered subscription models for different user segments",
                "Develop premium features for heavy users",
                "Create artist partnership programs for exclusive content"
            ]
        }

        for category, items in recommendations.items():
            with st.expander(category):
                for item in items:
                    st.markdown(f"• {item}")

        # Implementation roadmap
        st.subheader("🗺️ Implementation Roadmap")

        roadmap = {
            "Phase 1 (0-3 months): Quick Wins": [
                "Implement basic user segmentation",
                "Launch targeted marketing campaigns",
                "Improve playlist curation algorithms"
            ],
            "Phase 2 (3-6 months): Core Features": [
                "Develop advanced recommendation system",
                "Launch social sharing features",
                "Implement tiered subscription model"
            ],
            "Phase 3 (6-12 months): Advanced Strategy": [
                "Expand into underserved markets",
                "Launch artist partnership program",
                "Develop AI-powered content discovery"
            ]
        }

        for phase, tasks in roadmap.items():
            with st.expander(phase):
                for i, task in enumerate(tasks, 1):
                    st.markdown(f"{i}. {task}")

    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;">🎵 Music Streaming Trends Dashboard | Powered by Streamlit</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()