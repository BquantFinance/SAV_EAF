import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import json

# Page Configuration
st.set_page_config(
    page_title="Dashboard de Análisis Financiero",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics - Professional Dark Theme
st.markdown("""
<style>
    /* Main color theme - Sophisticated Dark */
    :root {
        --primary-color: #60A5FA;  /* Light blue */
        --secondary-color: #34D399;  /* Emerald green */
        --accent-color: #FBBF24;  /* Amber */
        --danger-color: #F87171;  /* Light red */
        --background-dark: #0F172A;  /* Deep navy */
        --background-card: #1E293B;  /* Slate 800 */
        --background-hover: #334155;  /* Slate 700 */
        --border-color: #334155;  /* Slate 700 */
        --text-primary: #F1F5F9;  /* Slate 100 */
        --text-secondary: #CBD5E1;  /* Slate 300 */
        --text-muted: #94A3B8;  /* Slate 400 */
    }
    
    /* Main app background */
    .stApp {
        background-color: #0F172A;
    }
    
    /* All text should be light */
    .stMarkdown, .stText {
        color: #F1F5F9 !important;
    }
    
    /* Custom metric cards - Dark with good contrast */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border: 1px solid #475569;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.4);
        border-color: #60A5FA;
    }
    
    div[data-testid="metric-container"] label {
        color: #94A3B8 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    div[data-testid="metric-container"] > div > div {
        color: #F1F5F9 !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
    }
    
    /* Green delta for positive metrics */
    [data-testid="stMetricDelta"] {
        color: #34D399 !important;
    }
    
    [data-testid="stMetricDelta"] svg {
        fill: #34D399;
    }
    
    /* Headers - Bright and clear */
    h1 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        font-size: 2.25rem !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        color: #F1F5F9 !important;
        font-weight: 600 !important;
        font-size: 1.75rem !important;
        margin-top: 2rem !important;
        border-bottom: 2px solid #334155;
        padding-bottom: 0.5rem;
    }
    
    h3 {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        margin-top: 1.5rem !important;
    }
    
    h4 {
        color: #CBD5E1 !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar styling - Dark gradient */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border-right: 1px solid #334155;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #CBD5E1 !important;
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #F1F5F9 !important;
    }
    
    /* Main content area */
    .main {
        background-color: #0F172A;
        color: #F1F5F9;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: #1E293B !important;
        color: #F1F5F9 !important;
        font-size: 13px;
        border: 1px solid #334155 !important;
    }
    
    .dataframe thead {
        background-color: #334155 !important;
        color: #F1F5F9 !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #334155 !important;
    }
    
    /* Button styling - Bright blue */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #60A5FA 0%, #93C5FD 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1E293B;
        padding: 4px;
        border-radius: 8px;
        border: 1px solid #334155;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: transparent;
        border-radius: 6px;
        color: #94A3B8;
        font-weight: 500;
        font-size: 14px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #CBD5E1;
        background-color: #334155;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%);
        color: white !important;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #1E293B;
        border: 1px solid #475569;
        color: #F1F5F9;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #60A5FA;
    }
    
    .stSelectbox label {
        color: #CBD5E1 !important;
    }
    
    /* Text input styling */
    .stTextInput > div > div {
        background-color: #1E293B;
        border: 1px solid #475569;
        color: #F1F5F9;
    }
    
    .stTextInput > div > div:focus-within {
        border-color: #60A5FA;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.2);
    }
    
    .stTextInput label {
        color: #CBD5E1 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        font-weight: 500;
        color: #E2E8F0 !important;
        padding: 12px;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #334155;
        border-color: #60A5FA;
    }
    
    .streamlit-expanderContent {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-top: none;
        color: #F1F5F9;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #1E3A8A;
        border: 1px solid #3B82F6;
        border-radius: 8px;
        color: #DBEAFE;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #34D399 100%);
        color: white;
        box-shadow: 0 4px 6px rgba(52, 211, 153, 0.3);
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #34D399 0%, #6EE7B7 100%);
        box-shadow: 0 6px 12px rgba(52, 211, 153, 0.4);
    }
    
    /* Radio buttons */
    [data-testid="stRadio"] label {
        color: #CBD5E1 !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background-color: #60A5FA;
    }
    
    .stSlider label {
        color: #CBD5E1 !important;
    }
    
    /* Multiselect */
    .stMultiSelect > div {
        background-color: #1E293B;
        border: 1px solid #475569;
        color: #F1F5F9;
    }
    
    .stMultiSelect label {
        color: #CBD5E1 !important;
    }
    
    /* Plotly charts - ensure they're readable */
    .js-plotly-plot {
        background-color: transparent !important;
    }
    
    /* Column gaps */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Make all p tags light */
    p {
        color: #E2E8F0;
    }
    
    /* Ensure code blocks are visible */
    code {
        background-color: #334155;
        color: #60A5FA;
        padding: 2px 4px;
        border-radius: 4px;
    }
    
    /* Make sure all text in markdown is visible */
    .markdown-text-container {
        color: #F1F5F9 !important;
    }
    
    /* Footer text */
    div[data-testid="stMarkdownContainer"] p {
        color: #CBD5E1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load Data Function
@st.cache_data
def load_data():
    """Cargar y preprocesar los datos"""
    df = pd.read_csv('cnmv_entities_complete.csv')
    
    # Parse capital social to numeric
    df['capital_social_numeric'] = df['capital_social'].str.replace('.', '').str.replace(',', '.').astype(float)
    
    # Parse dates
    df['fecha_extraccion'] = pd.to_datetime(df['fecha_extraccion'])
    df['fecha_registro'] = pd.to_datetime(df['fecha_registro'], format='%d/%m/%Y', errors='coerce')
    
    # Create derived columns
    df['years_operating'] = (datetime.now() - df['fecha_registro']).dt.days / 365.25
    df['total_services'] = df['num_servicios_inversion'].fillna(0) + df['num_servicios_auxiliares'].fillna(0)
    df['has_international_presence'] = ((df['num_libre_prestacion_eee'] > 0) | 
                                        (df['num_sucursales_eee'] > 0) | 
                                        (df['num_libre_prestacion_fuera_eee'] > 0) | 
                                        (df['num_sucursales_fuera_eee'] > 0))
    
    return df

# Load data
try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ Por favor, cargue el archivo 'cnmv_entities_complete.csv' para continuar")
    st.stop()

# Sidebar Navigation
st.sidebar.title("🏦 Análisis de Entidades")
st.sidebar.markdown("**Sociedades y Agencias de Valores**")
st.sidebar.markdown("**Empresas de Asesoramiento Financiero**")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "Navegación",
    ["🏠 Vista General", "🔍 Explorador de Entidades", "📊 Análisis Comparativo", 
     "🗺️ Inteligencia Geográfica", "💼 Análisis de Servicios", 
     "💰 Salud Financiera", "👥 Segmentación de Clientes"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Estadísticas Rápidas")
st.sidebar.metric("Total Entidades", len(df))
st.sidebar.metric("Entidades SAV", len(df[df['tipo_entidad'] == 'SAV']))
st.sidebar.metric("Entidades EAF", len(df[df['tipo_entidad'] == 'EAF']))

# Add most common instruments
st.sidebar.markdown("### 🎯 Instrumentos Más Comunes")
common_instruments = {
    'a': df['instrumentos_activos'].str.contains('a', na=False).sum(),
    'b': df['instrumentos_activos'].str.contains('b', na=False).sum(),
    'c': df['instrumentos_activos'].str.contains('c', na=False).sum()
}
for code, count in sorted(common_instruments.items(), key=lambda x: x[1], reverse=True):
    inst_names = {'a': 'Valores negociables', 'b': 'Mercado monetario', 'c': 'Fondos inversión'}
    st.sidebar.markdown(f"<small style='color: #CBD5E1;'><code style='color: #60A5FA;'>{code}</code> {inst_names[code]}: {count}</small>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**Desarrollado por [@Gsnchez](https://twitter.com/Gsnchez)**")
st.sidebar.markdown("**[bquantfinance.com](https://bquantfinance.com)**")

# Page: Overview
if page == "🏠 Vista General":
    st.title("📊 Dashboard de Sociedades y Agencias de Valores y Empresas de Asesoramiento Financiero")
    st.markdown("### Análisis en Tiempo Real de Entidades Financieras Españolas")
    
    # Quick explanation box with instrument info
    with st.expander("ℹ️ Acerca de este dashboard", expanded=False):
        st.markdown("""
        <div style='color: #F1F5F9;'>
        <p>Este dashboard analiza <strong style='color: #60A5FA;'>197 entidades financieras reguladas</strong> en España:</p>
        <ul style='color: #CBD5E1;'>
            <li><strong style='color: #60A5FA;'>SAV (Sociedades y Agencias de Valores):</strong> 101 entidades</li>
            <li><strong style='color: #34D399;'>EAF (Empresas de Asesoramiento Financiero):</strong> 96 entidades</li>
        </ul>
        
        <p style='margin-top: 1rem;'><strong style='color: #FBBF24;'>Instrumentos Financieros (a-k):</strong></p>
        <div style='background: #0F172A; padding: 0.5rem; border-radius: 6px; font-size: 12px;'>
            <code style='color: #60A5FA;'>a:</code> Valores negociables |
            <code style='color: #60A5FA;'>b:</code> Mercado monetario |
            <code style='color: #60A5FA;'>c:</code> Fondos inversión |
            <code style='color: #60A5FA;'>d:</code> Derivados valores |
            <code style='color: #60A5FA;'>e:</code> Derivados materias primas (efectivo) |
            <code style='color: #60A5FA;'>f:</code> Derivados materias primas (físico) |
            <code style='color: #60A5FA;'>g:</code> Otros derivados |
            <code style='color: #60A5FA;'>h:</code> Derivados crédito |
            <code style='color: #60A5FA;'>i:</code> CFDs |
            <code style='color: #60A5FA;'>j:</code> Derivados clima |
            <code style='color: #60A5FA;'>k:</code> Derechos emisión
        </div>
        
        <p style='margin-top: 1rem; color: #94A3B8;'>Todos los datos son comparables gracias a la estandarización regulatoria (MiFID II y RD 814/2023).</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_entities = len(df)
        st.metric(
            "Total Entidades",
            f"{total_entities:,}",
            delta=f"SAV: {len(df[df['tipo_entidad'] == 'SAV'])}, EAF: {len(df[df['tipo_entidad'] == 'EAF'])}",
            help="Número total de entidades reguladas"
        )
    
    with col2:
        total_capital = df['capital_social_numeric'].sum()
        st.metric(
            "Capital Total",
            f"€{total_capital/1e9:.2f}MM",
            delta=f"Media: €{df['capital_social_numeric'].mean()/1e6:.2f}M",
            help="Suma del capital social de todas las entidades"
        )
    
    with col3:
        intl_presence = df['has_international_presence'].sum()
        st.metric(
            "Presencia Internacional",
            f"{intl_presence}",
            delta=f"{(intl_presence/len(df)*100):.1f}% de entidades",
            help="Entidades con operaciones fuera de España"
        )
    
    with col4:
        avg_services = df['total_services'].mean()
        st.metric(
            "Media Servicios",
            f"{avg_services:.1f}",
            delta=f"Máx: {df['total_services'].max()}",
            help="Promedio de servicios totales por entidad"
        )
    
    with col5:
        audited = df['num_auditorias'].notna().sum()
        st.metric(
            "Entidades Auditadas",
            f"{audited}",
            delta=f"{(audited/len(df)*100):.1f}%",
            help="Entidades con auditorías registradas"
        )
    
    st.markdown("---")
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        # Entity type distribution
        fig_pie = px.pie(
            values=df['tipo_entidad'].value_counts().values,
            names=df['tipo_entidad'].value_counts().index,
            title="Distribución por Tipo de Entidad",
            color_discrete_map={'SAV': '#60A5FA', 'EAF': '#34D399'},
            hole=0.4
        )
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(size=14, color='white')
        )
        fig_pie.update_layout(
            height=400,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#1E293B',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            showlegend=True,
            legend=dict(font=dict(color='#CBD5E1'))
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Top provinces bar chart
        province_counts = df['direccion_provincia'].value_counts().head(10)
        fig_bar = px.bar(
            x=province_counts.values,
            y=province_counts.index,
            orientation='h',
            title="Top 10 Provincias por Número de Entidades",
            labels={'x': 'Número de Entidades', 'y': 'Provincia'},
            color=province_counts.values,
            color_continuous_scale=[[0, '#1E293B'], [0.5, '#60A5FA'], [1, '#93C5FD']]
        )
        fig_bar.update_layout(
            height=400,
            showlegend=False,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            coloraxis_colorbar=dict(
                title_font_color='#CBD5E1',
                tickfont_color='#CBD5E1'
            )
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Charts row 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Capital social distribution
        fig_box = px.box(
            df,
            x='tipo_entidad',
            y='capital_social_numeric',
            title="Distribución de Capital Social por Tipo de Entidad",
            labels={'capital_social_numeric': 'Capital Social (€)', 'tipo_entidad': 'Tipo de Entidad'},
            color='tipo_entidad',
            color_discrete_map={'SAV': '#60A5FA', 'EAF': '#34D399'},
            log_y=True
        )
        fig_box.update_layout(
            height=400,
            showlegend=False,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            yaxis=dict(gridcolor='#334155', zerolinecolor='#334155')
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        # Services heatmap
        services_data = df.groupby('tipo_entidad')[['num_servicios_inversion', 'num_servicios_auxiliares']].mean()
        fig_heat = go.Figure(data=go.Heatmap(
            z=services_data.values,
            x=['Servicios de Inversión', 'Servicios Auxiliares'],
            y=services_data.index,
            colorscale=[[0, '#0F172A'], [0.5, '#60A5FA'], [1, '#93C5FD']],
            text=services_data.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 14, "color": "white"},
            hoverongaps=False
        ))
        fig_heat.update_layout(
            title="Promedio de Servicios por Tipo de Entidad",
            height=400,
            xaxis_title="Tipo de Servicio",
            yaxis_title="Tipo de Entidad",
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            xaxis=dict(gridcolor='#334155'),
            yaxis=dict(gridcolor='#334155')
        )
        st.plotly_chart(fig_heat, use_container_width=True)
    
    # Recent registrations timeline
    st.markdown("### 📅 Línea Temporal de Registros")
    df_timeline = df[df['fecha_registro'].notna()].copy()
    df_timeline['year'] = df_timeline['fecha_registro'].dt.year
    yearly_registrations = df_timeline.groupby(['year', 'tipo_entidad']).size().reset_index(name='count')
    
    fig_timeline = px.area(
        yearly_registrations[yearly_registrations['year'] >= 1985],
        x='year',
        y='count',
        color='tipo_entidad',
        title="Registros de Entidades a lo Largo del Tiempo",
        labels={'count': 'Número de Registros', 'year': 'Año'},
        color_discrete_map={'SAV': '#60A5FA', 'EAF': '#34D399'}
    )
    fig_timeline.update_layout(
        height=300,
        paper_bgcolor='#1E293B',
        plot_bgcolor='#0F172A',
        font=dict(color='#F1F5F9', size=12),
        title_font=dict(size=16, color='#F1F5F9'),
        xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
        yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
        legend=dict(
            font=dict(color='#CBD5E1'),
            bgcolor='#1E293B',
            bordercolor='#334155',
            borderwidth=1
        )
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

# Page: Entity Explorer
elif page == "🔍 Explorador de Entidades":
    st.title("🔍 Explorador de Entidades")
    st.markdown("Busque y filtre todas las entidades reguladas")
    
    # Filters - First row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        entity_type = st.selectbox("Tipo de Entidad", ["Todas", "SAV", "EAF"])
    
    with col2:
        province = st.selectbox("Provincia", ["Todas"] + sorted(df['direccion_provincia'].dropna().unique()))
    
    with col3:
        capital_range = st.slider(
            "Rango de Capital Social (€)",
            min_value=0,
            max_value=int(df['capital_social_numeric'].max()),
            value=(0, int(df['capital_social_numeric'].max())),
            format="€%d"
        )
    
    with col4:
        intl_presence = st.selectbox("Presencia Internacional", ["Todas", "Sí", "No"])
    
    # Second row of filters - Instruments
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Create instrument filter options
        instrument_options = {
            'Todos': None,
            'a - Valores negociables': 'a',
            'b - Mercado monetario': 'b',
            'c - Fondos inversión': 'c',
            'd - Derivados valores': 'd',
            'e - Derivados mat. primas (efectivo)': 'e',
            'f - Derivados mat. primas (físico)': 'f',
            'g - Otros derivados': 'g',
            'h - Derivados crédito': 'h',
            'i - CFDs': 'i',
            'j - Derivados clima': 'j',
            'k - Derechos emisión': 'k'
        }
        instrument_filter = st.selectbox("Filtrar por Instrumento", list(instrument_options.keys()))
    
    with col2:
        # Number of instruments range
        num_instruments_range = st.slider(
            "Número de Instrumentos",
            min_value=0,
            max_value=int(df['num_instrumentos'].max()),
            value=(0, int(df['num_instrumentos'].max()))
        )
    
    # Search box
    search_term = st.text_input("🔎 Buscar por nombre de entidad", placeholder="Ingrese el nombre de la entidad...")
    
    # Apply filters
    filtered_df = df.copy()
    
    # Fix entity type filter
    if entity_type != "Todas":
        filtered_df = filtered_df[filtered_df['tipo_entidad'] == entity_type]
    
    if province != "Todas":
        filtered_df = filtered_df[filtered_df['direccion_provincia'] == province]
    
    filtered_df = filtered_df[
        (filtered_df['capital_social_numeric'] >= capital_range[0]) &
        (filtered_df['capital_social_numeric'] <= capital_range[1])
    ]
    
    if intl_presence == "Sí":
        filtered_df = filtered_df[filtered_df['has_international_presence'] == True]
    elif intl_presence == "No":
        filtered_df = filtered_df[filtered_df['has_international_presence'] == False]
    
    # Apply instrument filter
    if instrument_filter != 'Todos':
        selected_instrument = instrument_options[instrument_filter]
        filtered_df = filtered_df[filtered_df['instrumentos_activos'].str.contains(selected_instrument, na=False)]
    
    # Apply number of instruments filter
    filtered_df = filtered_df[
        (filtered_df['num_instrumentos'] >= num_instruments_range[0]) &
        (filtered_df['num_instrumentos'] <= num_instruments_range[1])
    ]
    
    if search_term:
        filtered_df = filtered_df[filtered_df['nombre'].str.contains(search_term, case=False, na=False)]
    
    # Results summary
    st.markdown(f"### Se encontraron {len(filtered_df)} entidades")
    
    # Display options
    col1, col2 = st.columns([3, 1])
    with col2:
        view_mode = st.radio("Modo de Vista", ["Tabla", "Tarjetas"], horizontal=True)
    
    if view_mode == "Tabla":
        # Table view with instrument codes reference
        st.markdown("""
        <div style='background: #1E293B; padding: 0.5rem; border-radius: 6px; margin-bottom: 1rem;'>
            <span style='color: #FBBF24; font-weight: bold;'>📌 Códigos de Instrumentos:</span>
            <span style='color: #CBD5E1; font-size: 12px;'>
            a: Valores negociables | b: Mercado monetario | c: Fondos | d: Derivados valores | e: Derivados materias primas (efectivo) | 
            f: Derivados materias primas (físico) | g: Otros derivados | h: Derivados crédito | i: CFDs | j: Derivados clima | k: Derechos emisión
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        display_columns = ['nombre', 'tipo_entidad', 'numero_registro', 'direccion_provincia', 
                          'capital_social', 'num_servicios_inversion', 'num_servicios_auxiliares',
                          'num_instrumentos', 'instrumentos_activos', 'fogain']
        
        st.dataframe(
            filtered_df[display_columns].style.format({
                'capital_social': '€{}'
            }),
            use_container_width=True,
            height=600
        )
    else:
        # Cards view
        st.markdown("""
        <div style='background: #1E293B; padding: 0.5rem; border-radius: 6px; margin-bottom: 1rem;'>
            <span style='color: #FBBF24; font-weight: bold;'>📌 Códigos de Instrumentos:</span>
            <span style='color: #CBD5E1; font-size: 12px;'>
            a: Valores negociables | b: Mercado monetario | c: Fondos | d: Derivados valores | e: Derivados materias primas | 
            f: Derivados físicos | g: Otros derivados | h: Derivados crédito | i: CFDs | j: Derivados clima | k: Derechos emisión
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        for idx, row in filtered_df.head(20).iterrows():
            with st.expander(f"🏢 {row['nombre']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Tipo:** {row['tipo_entidad']}")
                    st.markdown(f"**Nº Registro:** {row['numero_registro']}")
                    st.markdown(f"**Fecha Registro:** {row['fecha_registro']}")
                    st.markdown(f"**FOGAIN:** {row['fogain']}")
                
                with col2:
                    st.markdown(f"**Capital Social:** €{row['capital_social']}")
                    st.markdown(f"**Provincia:** {row['direccion_provincia']}")
                    st.markdown(f"**Servicios Inversión:** {row['num_servicios_inversion']}")
                    st.markdown(f"**Servicios Auxiliares:** {row['num_servicios_auxiliares']}")
                
                with col3:
                    st.markdown(f"**Total Instrumentos:** {row['num_instrumentos']}")
                    st.markdown(f"**Instrumentos Activos:**")
                    if pd.notna(row['instrumentos_activos']):
                        st.markdown(f"<code style='background: #0F172A; color: #60A5FA; padding: 2px 4px; border-radius: 4px;'>{row['instrumentos_activos']}</code>", unsafe_allow_html=True)
                    else:
                        st.markdown("*No especificado*")
    
    # Export functionality
    if st.button("📥 Exportar Datos Filtrados"):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name=f"entidades_filtradas_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Page: Comparative Analysis
elif page == "📊 Análisis Comparativo":
    st.title("📊 Análisis Comparativo")
    st.markdown("Compare múltiples entidades lado a lado")
    
    # Entity selection
    entities = st.multiselect(
        "Seleccione entidades para comparar (máximo 4)",
        options=df['nombre'].tolist(),
        max_selections=4
    )
    
    if len(entities) >= 2:
        compare_df = df[df['nombre'].isin(entities)]
        
        # Comparison metrics
        st.markdown("### Comparación de Métricas Clave")
        
        metrics_data = []
        for _, entity in compare_df.iterrows():
            metrics_data.append({
                'Entidad': entity['nombre'][:30] + '...' if len(entity['nombre']) > 30 else entity['nombre'],
                'Capital Social': entity['capital_social_numeric'],
                'Servicios de Inversión': entity['num_servicios_inversion'],
                'Servicios Auxiliares': entity['num_servicios_auxiliares'],
                'Total Instrumentos': entity['num_instrumentos'],
                'Años Operando': entity['years_operating']
            })
        
        metrics_df = pd.DataFrame(metrics_data)
        
        # Radar chart
        categories = ['Servicios de Inversión', 'Servicios Auxiliares', 'Total Instrumentos']
        
        fig = go.Figure()
        
        colors = ['#60A5FA', '#34D399', '#FBBF24', '#F87171']
        
        for idx, entity_name in enumerate(metrics_df['Entidad']):
            entity_data = metrics_df[metrics_df['Entidad'] == entity_name]
            
            # Normalize values for radar chart
            values = []
            for cat in categories:
                max_val = metrics_df[cat].max()
                if max_val > 0:
                    values.append(entity_data[cat].values[0] / max_val * 100)
                else:
                    values.append(0)
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=entity_name,
                marker=dict(color=colors[idx])
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor='#334155',
                    linecolor='#334155'
                ),
                bgcolor='#0F172A'
            ),
            showlegend=True,
            title="Comparación de Servicios e Instrumentos",
            height=500,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            legend=dict(
                font=dict(color='#CBD5E1'),
                bgcolor='#1E293B',
                bordercolor='#334155',
                borderwidth=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Bar comparison
        col1, col2 = st.columns(2)
        
        with col1:
            fig_capital = px.bar(
                metrics_df,
                x='Entidad',
                y='Capital Social',
                title="Comparación de Capital Social",
                color='Entidad',
                color_discrete_sequence=colors
            )
            fig_capital = px.bar(
                metrics_df,
                x='Entidad',
                y='Capital Social',
                title="Comparación de Capital Social",
                color='Entidad',
                color_discrete_sequence=['#60A5FA', '#34D399', '#FBBF24', '#F87171']
            )
            fig_capital.update_layout(
                showlegend=False,
                height=400,
                paper_bgcolor='#1E293B',
                plot_bgcolor='#0F172A',
                font=dict(color='#F1F5F9', size=12),
                title_font=dict(size=16, color='#F1F5F9'),
                xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
                yaxis=dict(gridcolor='#334155', zerolinecolor='#334155')
            )
            st.plotly_chart(fig_capital, use_container_width=True)
        
        with col2:
            services_comparison = metrics_df.melt(
                id_vars=['Entidad'],
                value_vars=['Servicios de Inversión', 'Servicios Auxiliares'],
                var_name='Tipo de Servicio',
                value_name='Cantidad'
            )
            
            fig_services = px.bar(
                services_comparison,
                x='Entidad',
                y='Cantidad',
                color='Tipo de Servicio',
                title="Comparación de Servicios",
                barmode='group',
                color_discrete_map={'Servicios de Inversión': '#60A5FA', 'Servicios Auxiliares': '#34D399'}
            )
            fig_services.update_layout(
                height=400,
                paper_bgcolor='#1E293B',
                plot_bgcolor='#0F172A',
                font=dict(color='#F1F5F9', size=12),
                title_font=dict(size=16, color='#F1F5F9'),
                xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
                yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
                legend=dict(
                    font=dict(color='#CBD5E1'),
                    bgcolor='#1E293B',
                    bordercolor='#334155',
                    borderwidth=1
                )
            )
            st.plotly_chart(fig_services, use_container_width=True)
        
        # Detailed comparison table with better formatting
        st.markdown("### Comparación Detallada")
        
        # Add explanation with instrument reference
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1E3A8A 0%, #1E293B 100%); border: 1px solid #3B82F6; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;'>
            <p style='color: #DBEAFE; margin: 0; margin-bottom: 0.5rem;'>
            <strong style='color: #93C5FD;'>💡 Tip:</strong> Los servicios e instrumentos son directamente comparables entre entidades.
            </p>
            <p style='color: #CBD5E1; margin: 0; font-size: 12px;'>
            <strong>Instrumentos:</strong> a: Valores | b: Mercado monetario | c: Fondos | d: Derivados valores | e-f: Derivados materias primas | 
            g: Otros derivados | h: Derivados crédito | i: CFDs | j: Derivados clima | k: Derechos emisión
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        comparison_fields = ['nombre', 'tipo_entidad', 'capital_social', 'direccion_provincia',
                            'num_servicios_inversion', 'num_servicios_auxiliares', 'num_instrumentos',
                            'instrumentos_activos', 'fogain', 'num_auditorias', 'tipos_clientes']
        
        comparison_table = compare_df[comparison_fields].T
        comparison_table.columns = [name[:30] + '...' if len(name) > 30 else name for name in entities]
        comparison_table.index = ['Nombre', 'Tipo', 'Capital Social', 'Provincia', 
                                 'Servicios Inversión', 'Servicios Auxiliares', 'Nº Instrumentos',
                                 'Instrumentos Activos', 'FOGAIN', 'Auditorías', 'Tipos Cliente']
        
        st.dataframe(comparison_table, use_container_width=True)
        
    else:
        st.info("👆 Por favor seleccione al menos 2 entidades para comparar")

# Page: Geographic Intelligence
elif page == "🗺️ Inteligencia Geográfica":
    st.title("🗺️ Inteligencia Geográfica")
    st.markdown("Analice la distribución geográfica de las entidades")
    
    # Province analysis
    province_stats = df.groupby('direccion_provincia').agg({
        'id': 'count',
        'capital_social_numeric': 'sum',
        'num_servicios_inversion': 'mean',
        'has_international_presence': 'sum'
    }).reset_index()
    province_stats.columns = ['Provincia', 'Número de Entidades', 'Capital Total', 'Media Servicios Inversión', 'Presencia Internacional']
    
    # Map visualization (using plotly choropleth with Spanish provinces)
    fig_map = px.treemap(
        province_stats,
        path=['Provincia'],
        values='Número de Entidades',
        color='Capital Total',
        hover_data=['Media Servicios Inversión', 'Presencia Internacional'],
        title="Distribución de Entidades por Provincia",
        color_continuous_scale=[[0, '#0F172A'], [0.5, '#60A5FA'], [1, '#93C5FD']]
    )
    fig_map.update_layout(
        height=500,
        paper_bgcolor='#1E293B',
        plot_bgcolor='#0F172A',
        font=dict(color='#F1F5F9', size=12),
        title_font=dict(size=16, color='#F1F5F9')
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Province details
    col1, col2 = st.columns(2)
    
    with col1:
        # Top provinces by entity count
        top_provinces = province_stats.nlargest(10, 'Número de Entidades')
        fig_top = px.bar(
            top_provinces,
            x='Número de Entidades',
            y='Provincia',
            orientation='h',
            title="Top 10 Provincias por Número de Entidades",
            color='Capital Total',
            color_continuous_scale=[[0, '#0F172A'], [0.5, '#60A5FA'], [1, '#93C5FD']],
            hover_data=['Capital Total', 'Presencia Internacional']
        )
        fig_top.update_layout(
            height=400,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            coloraxis_colorbar=dict(
                title_font_color='#CBD5E1',
                tickfont_color='#CBD5E1'
            )
        )
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        # Capital concentration
        province_stats['Capital %'] = (province_stats['Capital Total'] / province_stats['Capital Total'].sum() * 100)
        top_capital = province_stats.nlargest(10, 'Capital Total')
        
        fig_capital = px.pie(
            top_capital,
            values='Capital Total',
            names='Provincia',
            title="Distribución de Capital por Provincia (Top 10)",
            hole=0.4,
            color_discrete_sequence=['#60A5FA', '#34D399', '#FBBF24', '#F87171', '#93C5FD', '#6EE7B7', '#FDE68A', '#FCA5A5', '#BFDBFE', '#A7F3D0']
        )
        fig_capital.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(color='white')
        )
        fig_capital.update_layout(
            height=400,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#1E293B',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            legend=dict(font=dict(color='#CBD5E1'))
        )
        st.plotly_chart(fig_capital, use_container_width=True)
    
    # International presence
    st.markdown("### 🌍 Análisis de Presencia Internacional")
    
    intl_stats = df[df['has_international_presence'] == True]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        eee_entities = df[df['num_libre_prestacion_eee'] > 0]
        st.metric("Presencia EEE", len(eee_entities), f"{len(eee_entities)/len(df)*100:.1f}%")
    
    with col2:
        non_eee_entities = df[df['num_libre_prestacion_fuera_eee'] > 0]
        st.metric("Presencia Fuera EEE", len(non_eee_entities), f"{len(non_eee_entities)/len(df)*100:.1f}%")
    
    with col3:
        branches_entities = df[df['num_sucursales_espana'] > 0]
        st.metric("Con Sucursales en España", len(branches_entities), f"{len(branches_entities)/len(df)*100:.1f}%")
    
    # International presence by entity type
    intl_by_type = df.groupby('tipo_entidad')['has_international_presence'].agg(['sum', 'count'])
    intl_by_type['percentage'] = intl_by_type['sum'] / intl_by_type['count'] * 100
    
    fig_intl = px.bar(
        x=intl_by_type.index,
        y=intl_by_type['percentage'],
        title="Presencia Internacional por Tipo de Entidad",
        labels={'x': 'Tipo de Entidad', 'y': 'Porcentaje con Presencia Internacional'},
        color=intl_by_type['percentage'],
        color_continuous_scale=[[0, '#0F172A'], [0.5, '#60A5FA'], [1, '#93C5FD']],
        text=intl_by_type['percentage'].round(1)
    )
    fig_intl.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_intl.update_layout(
        showlegend=False,
        height=400,
        paper_bgcolor='#1E293B',
        plot_bgcolor='#0F172A',
        font=dict(color='#F1F5F9', size=12),
        title_font=dict(size=16, color='#F1F5F9'),
        xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
        yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
        coloraxis_colorbar=dict(
            title_font_color='#CBD5E1',
            tickfont_color='#CBD5E1'
        )
    )
    st.plotly_chart(fig_intl, use_container_width=True)

# Page: Services Analysis
elif page == "💼 Análisis de Servicios":
    st.title("💼 Análisis de Servicios")
    st.markdown("Análisis profundo de servicios de inversión y auxiliares")
    
    # Explanation of comparability
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1E3A8A 0%, #1E293B 100%); border: 1px solid #3B82F6; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;'>
        <p style='color: #DBEAFE; margin: 0;'>
        <strong style='color: #93C5FD;'>ℹ️ Nota sobre la comparabilidad:</strong> Todos los servicios están estandarizados según la normativa MiFID II y el RD 814/2023, 
        lo que permite comparaciones objetivas entre todas las entidades reguladas, independientemente de su tipo (SAV o EAF).
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overall service statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_inv_services = df['num_servicios_inversion'].mean()
        st.metric("Media Servicios Inversión", f"{avg_inv_services:.2f}")
    
    with col2:
        avg_aux_services = df['num_servicios_auxiliares'].mean()
        st.metric("Media Servicios Auxiliares", f"{avg_aux_services:.2f}")
    
    with col3:
        max_services = df['total_services'].max()
        st.metric("Máx Servicios Totales", int(max_services))
    
    with col4:
        full_service = len(df[df['total_services'] >= 10])
        st.metric("Entidades Full Service", full_service)
    
    # Service distribution
    st.markdown("### Análisis de Distribución de Servicios")
    
    # Add service type definitions
    with st.expander("📚 Tipos de Servicios según MiFID II", expanded=False):
        col1_def, col2_def = st.columns(2)
        
        with col1_def:
            st.markdown("""
            **Servicios de Inversión:**
            1. Recepción y transmisión de órdenes
            2. Ejecución de órdenes
            3. Negociación por cuenta propia
            4. Gestión de carteras
            5. Asesoramiento en materia de inversión
            6. Aseguramiento de instrumentos
            7. Colocación de instrumentos
            """)
        
        with col2_def:
            st.markdown("""
            **Servicios Auxiliares:**
            1. Custodia y administración
            2. Concesión de créditos/préstamos
            3. Asesoramiento a empresas
            4. Servicios de cambio de divisas
            5. Investigación y análisis financiero
            6. Servicios relacionados con aseguramiento
            """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Investment services histogram
        fig_inv = px.histogram(
            df,
            x='num_servicios_inversion',
            title="Distribución de Servicios de Inversión",
            labels={'num_servicios_inversion': 'Número de Servicios de Inversión', 'count': 'Número de Entidades'},
            color_discrete_sequence=['#60A5FA'],
            nbins=15
        )
        fig_inv.update_layout(
            height=400,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            bargap=0.1
        )
        st.plotly_chart(fig_inv, use_container_width=True)
    
    with col2:
        # Auxiliary services histogram
        fig_aux = px.histogram(
            df,
            x='num_servicios_auxiliares',
            title="Distribución de Servicios Auxiliares",
            labels={'num_servicios_auxiliares': 'Número de Servicios Auxiliares', 'count': 'Número de Entidades'},
            color_discrete_sequence=['#34D399'],
            nbins=15
        )
        fig_aux.update_layout(
            height=400,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            bargap=0.1
        )
        st.plotly_chart(fig_aux, use_container_width=True)
    
    # Services comparison framework
    st.markdown("### 🔄 Comparabilidad de Servicios entre Entidades")
    
    with st.expander("ℹ️ Información sobre la comparabilidad de servicios", expanded=False):
        st.info("""
        **¿Por qué son comparables los servicios?**
        
        Todas las entidades reguladas (SAV y EAF) deben declarar sus servicios según el mismo marco regulatorio:
        
        1. **Servicios de Inversión:** Definidos por MiFID II y el RD 814/2023
        2. **Servicios Auxiliares:** Complementarios a la actividad principal
        3. **Instrumentos Financieros:** Categorizados de forma estándar (a-k)
        
        Esto permite una comparación objetiva entre entidades del mismo tipo y diferentes tipos.
        """)
    
    # Create a comparison matrix
    col1, col2 = st.columns(2)
    
    with col1:
        # Services by entity type comparison
        services_by_type = df.groupby('tipo_entidad').agg({
            'num_servicios_inversion': ['mean', 'median', 'std'],
            'num_servicios_auxiliares': ['mean', 'median', 'std'],
            'num_instrumentos': ['mean', 'median', 'std']
        }).round(2)
        
        st.markdown("#### Estadísticas por Tipo de Entidad")
        st.dataframe(services_by_type, use_container_width=True)
    
    with col2:
        # Service coverage comparison
        service_coverage = pd.DataFrame({
            'Servicio': ['Servicios de Inversión', 'Servicios Auxiliares', 'Instrumentos'],
            'SAV (promedio)': [
                df[df['tipo_entidad'] == 'SAV']['num_servicios_inversion'].mean(),
                df[df['tipo_entidad'] == 'SAV']['num_servicios_auxiliares'].mean(),
                df[df['tipo_entidad'] == 'SAV']['num_instrumentos'].mean()
            ],
            'EAF (promedio)': [
                df[df['tipo_entidad'] == 'EAF']['num_servicios_inversion'].mean(),
                df[df['tipo_entidad'] == 'EAF']['num_servicios_auxiliares'].mean(),
                df[df['tipo_entidad'] == 'EAF']['num_instrumentos'].mean()
            ]
        })
        
        fig_comparison = px.bar(
            service_coverage.melt(id_vars='Servicio', var_name='Tipo', value_name='Promedio'),
            x='Servicio',
            y='Promedio',
            color='Tipo',
            title="Comparación Promedio SAV vs EAF",
            barmode='group',
            color_discrete_map={'SAV (promedio)': '#60A5FA', 'EAF (promedio)': '#34D399'}
        )
        fig_comparison.update_layout(
            height=400,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            legend=dict(
                font=dict(color='#CBD5E1'),
                bgcolor='#1E293B',
                bordercolor='#334155',
                borderwidth=1
            )
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Services correlation with better explanation
    st.markdown("### 📊 Análisis de Correlación de Servicios")
    
    # Create correlation matrix
    services_corr = df[['num_servicios_inversion', 'num_servicios_auxiliares', 
                        'num_instrumentos', 'capital_social_numeric', 'years_operating']].corr()
    
    fig_corr = px.imshow(
        services_corr,
        title="Matriz de Correlación de Servicios",
        labels=dict(x="Variable", y="Variable", color="Correlación"),
        x=['Servicios Inversión', 'Servicios Auxiliares', 'Instrumentos', 'Capital Social', 'Años Operando'],
        y=['Servicios Inversión', 'Servicios Auxiliares', 'Instrumentos', 'Capital Social', 'Años Operando'],
        color_continuous_scale='RdBu_r',
        aspect="auto",
        text_auto='.2f'
    )
    fig_corr.update_layout(
        height=500,
        paper_bgcolor='#1E293B',
        plot_bgcolor='#0F172A',
        font=dict(color='#F1F5F9', size=12),
        title_font=dict(size=16, color='#F1F5F9'),
        xaxis=dict(gridcolor='#334155'),
        yaxis=dict(gridcolor='#334155')
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Instruments analysis with definitions
    st.markdown("### 📈 Cobertura de Instrumentos Financieros")
    
    # Create two columns for instrument reference
    col_ref1, col_ref2 = st.columns(2)
    
    with col_ref1:
        # Add comprehensive instrument reference table
        with st.expander("📚 **Referencia de Instrumentos Financieros (RD 814/2023)**", expanded=True):
            st.markdown("""
            <div style='background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #334155;'>
            <table style='width: 100%; color: #F1F5F9; font-size: 13px;'>
            <tr style='border-bottom: 2px solid #60A5FA;'>
                <th style='text-align: left; padding: 8px; color: #60A5FA;'>Código</th>
                <th style='text-align: left; padding: 8px; color: #60A5FA;'>Instrumento Financiero</th>
            </tr>
            <tr style='border-bottom: 1px solid #334155;'>
                <td style='padding: 8px; color: #FBBF24; font-weight: bold;'>a</td>
                <td style='padding: 8px;'>Valores negociables (acciones, bonos, obligaciones)</td>
            </tr>
            <tr style='border-bottom: 1px solid #334155;'>
                <td style='padding: 8px; color: #FBBF24; font-weight: bold;'>b</td>
                <td style='padding: 8px;'>Instrumentos del mercado monetario</td>
            </tr>
            <tr style='border-bottom: 1px solid #334155;'>
                <td style='padding: 8px; color: #FBBF24; font-weight: bold;'>c</td>
                <td style='padding: 8px;'>Participaciones en IIC (fondos de inversión)</td>
            </tr>
            <tr style='border-bottom: 1px solid #334155;'>
                <td style='padding: 8px; color: #FBBF24; font-weight: bold;'>d</td>
                <td style='padding: 8px;'>Derivados sobre valores/divisas</td>
            </tr>
            <tr style='border-bottom: 1px solid #334155;'>
                <td style='padding: 8px; color: #FBBF24; font-weight: bold;'>e</td>
                <td style='padding: 8px;'>Derivados sobre materias primas (efectivo)</td>
            </tr>
            <tr style='border-bottom: 1px solid #334155;'>
                <td style='padding: 8px; color: #FBBF24; font-weight: bold;'>f</td>
                <td style='padding: 8px;'>Derivados sobre materias primas (físico)</td>
            </tr>
            </table>
            </div>
            """, unsafe_allow_html=True)
    
    with col_ref2:
        with st.expander("📚 **Continuación - Instrumentos Complejos**", expanded=True):
            st.markdown("""
            <div style='background: #0F172A; padding: 1rem; border-radius: 8px; border: 1px solid #334155;'>
            <table style='width: 100%; color: #F1F5F9; font-size: 13px;'>
            <tr style='border-bottom: 2px solid #60A5FA;'>
                <th style='text-align: left; padding: 8px; color: #60A5FA;'>Código</th>
                <th style='text-align: left; padding: 8px; color: #60A5FA;'>Instrumento Financiero</th>
            </tr>
            <tr style='border-bottom: 1px solid #334155;'>
                <td style='padding: 8px; color: #FBBF24; font-weight: bold;'>g</td>
                <td style='padding: 8px;'>Otros derivados sobre materias primas</td>
            </tr>
            <tr style='border-bottom: 1px solid #334155;'>
                <td style='padding: 8px; color: #FBBF24; font-weight: bold;'>h</td>
                <td style='padding: 8px;'>Derivados de transferencia de riesgo de crédito</td>
            </tr>
            <tr style='border-bottom: 1px solid #334155;'>
                <td style='padding: 8px; color: #FBBF24; font-weight: bold;'>i</td>
                <td style='padding: 8px;'>Contratos financieros por diferencias (CFDs)</td>
            </tr>
            <tr style='border-bottom: 1px solid #334155;'>
                <td style='padding: 8px; color: #FBBF24; font-weight: bold;'>j</td>
                <td style='padding: 8px;'>Derivados sobre clima/inflación/estadísticas</td>
            </tr>
            <tr style='border-bottom: 1px solid #334155;'>
                <td style='padding: 8px; color: #FBBF24; font-weight: bold;'>k</td>
                <td style='padding: 8px;'>Derechos de emisión de gases efecto invernadero</td>
            </tr>
            </table>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Add analysis of which instruments are most common
    st.markdown("### 📊 Análisis de Instrumentos Ofrecidos")
    
    # Count entities by specific instruments
    instrument_coverage = {}
    instruments_map = {
        'a': 'Valores negociables',
        'b': 'Mercado monetario', 
        'c': 'Fondos inversión',
        'd': 'Derivados valores/divisas',
        'e': 'Derivados materias primas (efectivo)',
        'f': 'Derivados materias primas (físico)',
        'g': 'Otros derivados materias primas',
        'h': 'Derivados de crédito',
        'i': 'CFDs',
        'j': 'Derivados clima/inflación',
        'k': 'Derechos emisión'
    }
    
    for inst_code, inst_name in instruments_map.items():
        count = df['instrumentos_activos'].str.contains(inst_code, na=False).sum()
        instrument_coverage[inst_name] = count
    
    # Create bar chart of instrument coverage
    inst_df = pd.DataFrame(list(instrument_coverage.items()), columns=['Instrumento', 'Entidades'])
    inst_df = inst_df.sort_values('Entidades', ascending=True)
    
    fig_inst_coverage = px.bar(
        inst_df,
        x='Entidades',
        y='Instrumento',
        orientation='h',
        title="Número de Entidades por Tipo de Instrumento",
        color='Entidades',
        color_continuous_scale=[[0, '#0F172A'], [0.5, '#60A5FA'], [1, '#93C5FD']],
        text='Entidades'
    )
    fig_inst_coverage.update_traces(texttemplate='%{text}', textposition='outside')
    fig_inst_coverage.update_layout(
        height=500,
        paper_bgcolor='#1E293B',
        plot_bgcolor='#0F172A',
        font=dict(color='#F1F5F9', size=12),
        title_font=dict(size=16, color='#F1F5F9'),
        xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
        yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
        showlegend=False,
        coloraxis_colorbar=dict(
            title_font_color='#CBD5E1',
            tickfont_color='#CBD5E1'
        )
    )
    st.plotly_chart(fig_inst_coverage, use_container_width=True)
    
    # Instrument distribution by ranges
    instrument_ranges = pd.cut(df['num_instrumentos'], bins=[0, 3, 6, 9, 15], 
                               labels=['Básico (1-3)', 'Intermedio (4-6)', 'Avanzado (7-9)', 'Completo (10+)'])
    instrument_dist = instrument_ranges.value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_inst = px.pie(
            values=instrument_dist.values,
            names=instrument_dist.index,
            title="Categorías de Cobertura de Instrumentos",
            hole=0.4,
            color_discrete_sequence=['#60A5FA', '#34D399', '#FBBF24', '#F87171']
        )
        fig_inst.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(size=12, color='white')
        )
        fig_inst.update_layout(
            height=400,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#1E293B',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            legend=dict(font=dict(color='#CBD5E1'))
        )
        st.plotly_chart(fig_inst, use_container_width=True)
    
    with col2:
        # Instruments by entity type
        inst_by_type = df.groupby('tipo_entidad')['num_instrumentos'].agg(['mean', 'std', 'max'])
        inst_by_type = inst_by_type.reset_index()
        
        fig_inst_type = go.Figure()
        fig_inst_type.add_trace(go.Bar(name='Media', x=inst_by_type['tipo_entidad'], y=inst_by_type['mean'],
                                       marker_color='#60A5FA'))
        fig_inst_type.add_trace(go.Bar(name='Máximo', x=inst_by_type['tipo_entidad'], y=inst_by_type['max'],
                                       marker_color='#34D399'))
        fig_inst_type.update_layout(
            title="Instrumentos por Tipo de Entidad",
            xaxis_title="Tipo de Entidad",
            yaxis_title="Número de Instrumentos",
            barmode='group',
            height=400,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            legend=dict(
                font=dict(color='#CBD5E1'),
                bgcolor='#1E293B',
                bordercolor='#334155',
                borderwidth=1
            )
        )
        st.plotly_chart(fig_inst_type, use_container_width=True)
    
    # Top entities by services with detailed breakdown
    st.markdown("### 🏆 Principales Proveedores de Servicios")
    
    # Add tabs for different views
    tab1, tab2, tab3 = st.tabs(["Top 10 por Servicios Totales", "Matriz de Servicios", "Distribución Detallada"])
    
    with tab1:
        top_service_entities = df.nlargest(10, 'total_services')[['nombre', 'tipo_entidad', 
                                                                   'num_servicios_inversion', 
                                                                   'num_servicios_auxiliares', 
                                                                   'total_services']]
        
        fig_top_services = px.bar(
            top_service_entities,
            x='nombre',
            y=['num_servicios_inversion', 'num_servicios_auxiliares'],
            title="Top 10 Entidades por Servicios Totales",
            labels={'value': 'Número de Servicios', 'nombre': 'Entidad'},
            color_discrete_map={'num_servicios_inversion': '#60A5FA', 'num_servicios_auxiliares': '#34D399'}
        )
        fig_top_services.update_layout(
            height=400,
            xaxis_tickangle=-45,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            legend_title_text='Tipo de Servicio',
            xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='#CBD5E1'),
                bgcolor='#1E293B',
                bordercolor='#334155',
                borderwidth=1
            )
        )
        st.plotly_chart(fig_top_services, use_container_width=True)
    
    with tab2:
        st.markdown("#### Matriz de Cobertura de Servicios e Instrumentos")
        
        # Create a sample matrix for top entities
        sample_entities = df.nlargest(15, 'total_services')[['nombre', 'num_servicios_inversion', 
                                                              'num_servicios_auxiliares', 'num_instrumentos']]
        sample_entities['nombre'] = sample_entities['nombre'].str[:40] + '...'
        
        # Create heatmap
        fig_matrix = px.imshow(
            sample_entities[['num_servicios_inversion', 'num_servicios_auxiliares', 'num_instrumentos']].values,
            labels=dict(x="Tipo de Servicio", y="Entidad", color="Cantidad"),
            x=['Servicios Inversión', 'Servicios Auxiliares', 'Instrumentos'],
            y=sample_entities['nombre'],
            color_continuous_scale=[[0, '#0F172A'], [0.5, '#60A5FA'], [1, '#93C5FD']],
            text_auto=True,
            aspect="auto"
        )
        fig_matrix.update_layout(
            height=600,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            xaxis=dict(gridcolor='#334155'),
            yaxis=dict(gridcolor='#334155'),
            coloraxis_colorbar=dict(
                title_font_color='#CBD5E1',
                tickfont_color='#CBD5E1'
            )
        )
        st.plotly_chart(fig_matrix, use_container_width=True)
    
    with tab3:
        # Service distribution by ranges
        st.markdown("#### Distribución de Entidades por Rango de Servicios")
        
        # Create service range categories
        df['service_category'] = pd.cut(df['total_services'], 
                                       bins=[0, 5, 10, 15, 20],
                                       labels=['Básico (0-5)', 'Intermedio (6-10)', 
                                              'Avanzado (11-15)', 'Completo (16+)'])
        
        category_counts = df['service_category'].value_counts()
        
        fig_dist = px.bar(
            x=category_counts.index,
            y=category_counts.values,
            title="Categorización de Entidades por Servicios Ofrecidos",
            labels={'x': 'Categoría de Servicios', 'y': 'Número de Entidades'},
            color=category_counts.values,
            color_continuous_scale=[[0, '#0F172A'], [0.5, '#60A5FA'], [1, '#93C5FD']],
            text=category_counts.values
        )
        fig_dist.update_traces(texttemplate='%{text}', textposition='outside')
        fig_dist.update_layout(
            showlegend=False,
            height=400,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            coloraxis_colorbar=dict(
                title_font_color='#CBD5E1',
                tickfont_color='#CBD5E1'
            )
        )
        st.plotly_chart(fig_dist, use_container_width=True)

# Page: Financial Health
elif page == "💰 Salud Financiera":
    st.title("💰 Dashboard de Salud Financiera")
    st.markdown("Análisis de distribución de capital y cumplimiento de auditorías")
    
    # Add explanatory section
    with st.expander("📖 Guía de interpretación de métricas", expanded=False):
        st.markdown("""
        **¿Cómo interpretar estos indicadores?**
        
        - **Capital Social:** Recursos propios de la entidad que garantizan su solvencia
        - **Concentración de Capital:** Indica si el mercado está dominado por pocas entidades grandes
        - **Auditorías:** Verificación independiente de la información financiera
        - **Distribución:** Muestra la equidad o desigualdad en el tamaño de las entidades
        """)
    
    # Capital social analysis
    st.markdown("### 💵 Análisis de Capital Social")
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_capital = df['capital_social_numeric'].sum()
        st.metric("Capital Total", f"€{total_capital/1e9:.2f}MM")
    
    with col2:
        avg_capital = df['capital_social_numeric'].mean()
        st.metric("Capital Promedio", f"€{avg_capital/1e6:.2f}M")
    
    with col3:
        median_capital = df['capital_social_numeric'].median()
        st.metric("Capital Mediano", f"€{median_capital/1e6:.2f}M")
    
    with col4:
        max_capital = df['capital_social_numeric'].max()
        st.metric("Capital Máximo", f"€{max_capital/1e6:.2f}M")
    
    # Top entities by capital
    st.markdown("### 📊 Ranking de Entidades por Capital Social")
    
    # Get top 20 entities by capital
    top_entities = df.nlargest(20, 'capital_social_numeric')[['nombre', 'tipo_entidad', 'capital_social_numeric', 'direccion_provincia']]
    
    # Create a more intuitive bar chart
    fig_top_capital = px.bar(
        top_entities,
        x='capital_social_numeric',
        y='nombre',
        orientation='h',
        title="Top 20 Entidades por Capital Social",
        labels={'capital_social_numeric': 'Capital Social (€)', 'nombre': 'Entidad'},
        color='tipo_entidad',
        color_discrete_map={'SAV': '#60A5FA', 'EAF': '#34D399'},
        hover_data=['capital_social_numeric', 'direccion_provincia']
    )
    fig_top_capital.update_layout(
        height=600,
        xaxis_tickformat='€,.0f',
        paper_bgcolor='#1E293B',
        plot_bgcolor='#0F172A',
        font=dict(color='#F1F5F9', size=12),
        title_font=dict(size=16, color='#F1F5F9'),
        showlegend=True,
        yaxis={'categoryorder':'total ascending'},
        xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
        legend=dict(
            font=dict(color='#CBD5E1'),
            bgcolor='#1E293B',
            bordercolor='#334155',
            borderwidth=1
        )
    )
    fig_top_capital.update_traces(texttemplate='€%{x:,.0f}', textposition='inside', textfont=dict(color='white'))
    st.plotly_chart(fig_top_capital, use_container_width=True)
    
    # Capital concentration metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top10_capital = df.nlargest(10, 'capital_social_numeric')['capital_social_numeric'].sum()
        total_capital = df['capital_social_numeric'].sum()
        concentration = (top10_capital / total_capital) * 100
        st.metric("Concentración Top 10", f"{concentration:.1f}%", 
                 help="Porcentaje del capital total que poseen las 10 mayores entidades")
    
    with col2:
        top20_capital = df.nlargest(20, 'capital_social_numeric')['capital_social_numeric'].sum()
        concentration20 = (top20_capital / total_capital) * 100
        st.metric("Concentración Top 20", f"{concentration20:.1f}%",
                 help="Porcentaje del capital total que poseen las 20 mayores entidades")
    
    with col3:
        bottom50_count = len(df.nsmallest(int(len(df)/2), 'capital_social_numeric'))
        bottom50_capital = df.nsmallest(int(len(df)/2), 'capital_social_numeric')['capital_social_numeric'].sum()
        bottom50_pct = (bottom50_capital / total_capital) * 100
        st.metric("Capital del 50% menor", f"{bottom50_pct:.1f}%",
                 help="Porcentaje del capital total que posee la mitad más pequeña de entidades")
    
    # Audit compliance
    st.markdown("### 🔍 Cumplimiento de Auditorías")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        audited = df['num_auditorias'].notna().sum()
        st.metric("Entidades Auditadas", audited, f"{audited/len(df)*100:.1f}%")
    
    with col2:
        avg_audits = df['num_auditorias'].mean()
        st.metric("Media Auditorías por Entidad", f"{avg_audits:.1f}")
    
    with col3:
        recent_audits = len(df[df['ultimo_ejercicio_auditado'] >= 2023])
        st.metric("Auditorías Recientes (2023+)", recent_audits)
    
    # Audit analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Audits by entity type
        audit_by_type = df.groupby('tipo_entidad')['num_auditorias'].agg(['mean', 'count', 'sum'])
        fig_audit = px.bar(
            x=audit_by_type.index,
            y=audit_by_type['mean'],
            title="Promedio de Auditorías por Tipo de Entidad",
            labels={'x': 'Tipo de Entidad', 'y': 'Promedio de Auditorías'},
            color=audit_by_type['mean'],
            color_continuous_scale=[[0, '#0F172A'], [0.5, '#60A5FA'], [1, '#93C5FD']],
            text=audit_by_type['mean'].round(1)
        )
        fig_audit.update_traces(texttemplate='%{text}', textposition='outside')
        fig_audit.update_layout(
            showlegend=False,
            height=400,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            coloraxis_colorbar=dict(
                title_font_color='#CBD5E1',
                tickfont_color='#CBD5E1'
            )
        )
        st.plotly_chart(fig_audit, use_container_width=True)
    
    with col2:
        # Top auditors
        auditors = []
        for auditor_list in df['auditores_unicos'].dropna():
            if isinstance(auditor_list, str):
                auditors.extend([a.strip() for a in auditor_list.split(';')])
        
        auditor_counts = pd.Series(auditors).value_counts().head(10)
        fig_auditors = px.bar(
            y=auditor_counts.index,
            x=auditor_counts.values,
            orientation='h',
            title="Top 10 Firmas Auditoras",
            labels={'x': 'Número de Entidades Auditadas', 'y': 'Auditor'},
            color=auditor_counts.values,
            color_continuous_scale=[[0, '#0F172A'], [0.5, '#60A5FA'], [1, '#93C5FD']]
        )
        fig_auditors.update_layout(
            height=400,
            showlegend=False,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            coloraxis_colorbar=dict(
                title_font_color='#CBD5E1',
                tickfont_color='#CBD5E1'
            )
        )
        st.plotly_chart(fig_auditors, use_container_width=True)

# Page: Client Segmentation
elif page == "👥 Segmentación de Clientes":
    st.title("👥 Análisis de Segmentación de Clientes")
    st.markdown("Comprensión de tipos de clientes y especializaciones de entidades")
    
    # Client type overview
    client_types = {
        'Minoristas': df['tipos_clientes'].str.contains('Minoristas', na=False).sum(),
        'Profesionales': df['tipos_clientes'].str.contains('Profesionales', na=False).sum(),
        'Contrapartes elegibles': df['tipos_clientes'].str.contains('Contrapartes elegibles', na=False).sum()
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Atienden Minoristas", client_types['Minoristas'], 
                 f"{client_types['Minoristas']/len(df)*100:.1f}%")
    
    with col2:
        st.metric("Atienden Profesionales", client_types['Profesionales'],
                 f"{client_types['Profesionales']/len(df)*100:.1f}%")
    
    with col3:
        st.metric("Atienden Contrapartes Elegibles", client_types['Contrapartes elegibles'],
                 f"{client_types['Contrapartes elegibles']/len(df)*100:.1f}%")
    
    # Client type distribution
    st.markdown("### Cobertura por Tipo de Cliente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart of client types
        fig_pie = px.pie(
            values=list(client_types.values()),
            names=list(client_types.keys()),
            title="Distribución por Tipo de Cliente (Entidades que Atienden Cada Tipo)",
            hole=0.4,
            color_discrete_sequence=['#60A5FA', '#34D399', '#FBBF24']
        )
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(size=12, color='white')
        )
        fig_pie.update_layout(
            height=400,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#1E293B',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            legend=dict(font=dict(color='#CBD5E1'))
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Client combinations
        client_combinations = df['tipos_clientes'].value_counts().head(7)
        fig_combo = px.bar(
            x=client_combinations.values,
            y=client_combinations.index,
            orientation='h',
            title="Combinaciones de Tipos de Cliente",
            labels={'x': 'Número de Entidades', 'y': 'Tipos de Cliente'},
            color=client_combinations.values,
            color_continuous_scale=[[0, '#0F172A'], [0.5, '#60A5FA'], [1, '#93C5FD']]
        )
        fig_combo.update_layout(
            height=400,
            showlegend=False,
            paper_bgcolor='#1E293B',
            plot_bgcolor='#0F172A',
            font=dict(color='#F1F5F9', size=12),
            title_font=dict(size=16, color='#F1F5F9'),
            xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
            coloraxis_colorbar=dict(
                title_font_color='#CBD5E1',
                tickfont_color='#CBD5E1'
            )
        )
        st.plotly_chart(fig_combo, use_container_width=True)
    
    # Client segmentation by services - Simplified
    st.markdown("### Oferta de Servicios por Tipo de Cliente")
    
    # Add explanation
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1E3A8A 0%, #1E293B 100%); border: 1px solid #3B82F6; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;'>
        <p style='color: #DBEAFE; margin: 0; margin-bottom: 0.5rem;'>
        <strong style='color: #93C5FD;'>💡 Tipos de clientes según MiFID II:</strong>
        </p>
        <ul style='color: #DBEAFE; margin: 0; padding-left: 1.5rem;'>
            <li><strong>Minoristas:</strong> Inversores particulares con mayor protección regulatoria</li>
            <li><strong>Profesionales:</strong> Inversores con experiencia y conocimiento del mercado</li>
            <li><strong>Contrapartes Elegibles:</strong> Instituciones financieras y grandes corporaciones</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Prepare data for analysis
    df['serves_retail'] = df['tipos_clientes'].str.contains('Minoristas', na=False)
    df['serves_professional'] = df['tipos_clientes'].str.contains('Profesionales', na=False)
    df['serves_eligible'] = df['tipos_clientes'].str.contains('Contrapartes elegibles', na=False)
    
    # Services by client segment
    segment_services = []
    for segment, column in [('Minoristas', 'serves_retail'), 
                           ('Profesionales', 'serves_professional'), 
                           ('Contrapartes Elegibles', 'serves_eligible')]:
        segment_data = df[df[column] == True]
        segment_services.append({
            'Segmento': segment,
            'Media Servicios Inversión': segment_data['num_servicios_inversion'].mean(),
            'Media Servicios Auxiliares': segment_data['num_servicios_auxiliares'].mean(),
            'Media Instrumentos': segment_data['num_instrumentos'].mean(),
            'Capital Medio (€M)': segment_data['capital_social_numeric'].mean() / 1e6
        })
    
    segment_df = pd.DataFrame(segment_services)
    
    # Heatmap of services by segment
    fig_heat = go.Figure(data=go.Heatmap(
        z=segment_df[['Media Servicios Inversión', 'Media Servicios Auxiliares', 'Media Instrumentos']].values,
        x=['Servicios Inversión', 'Servicios Auxiliares', 'Instrumentos'],
        y=segment_df['Segmento'],
        colorscale=[[0, '#0F172A'], [0.5, '#60A5FA'], [1, '#93C5FD']],
        text=segment_df[['Media Servicios Inversión', 'Media Servicios Auxiliares', 'Media Instrumentos']].values.round(2),
        texttemplate='%{text}',
        textfont={"size": 14, "color": "white"},
        hoverongaps=False
    ))
    fig_heat.update_layout(
        title="Promedio de Servicios por Segmento de Cliente",
        height=400,
        paper_bgcolor='#1E293B',
        plot_bgcolor='#0F172A',
        font=dict(color='#F1F5F9', size=12),
        title_font=dict(size=16, color='#F1F5F9'),
        xaxis=dict(gridcolor='#334155'),
        yaxis=dict(gridcolor='#334155')
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    
    # Entity specialization
    st.markdown("### Análisis de Especialización de Entidades")
    
    # Identify specialized entities
    retail_only = df[(df['serves_retail'] == True) & 
                    (df['serves_professional'] == False) & 
                    (df['serves_eligible'] == False)]
    
    professional_only = df[(df['serves_retail'] == False) & 
                          (df['serves_professional'] == True) & 
                          (df['serves_eligible'] == False)]
    
    full_service = df[(df['serves_retail'] == True) & 
                     (df['serves_professional'] == True) & 
                     (df['serves_eligible'] == True)]
    
    specialization_data = {
        'Especialización': ['Solo Minoristas', 'Solo Profesionales', 'Servicio Completo', 'Otros'],
        'Cantidad': [len(retail_only), len(professional_only), len(full_service), 
                    len(df) - len(retail_only) - len(professional_only) - len(full_service)]
    }
    
    fig_spec = px.bar(
        specialization_data,
        x='Especialización',
        y='Cantidad',
        title="Distribución de Especialización de Entidades",
        color='Cantidad',
        color_continuous_scale=[[0, '#0F172A'], [0.5, '#60A5FA'], [1, '#93C5FD']],
        text='Cantidad'
    )
    fig_spec.update_traces(texttemplate='%{text}', textposition='outside')
    fig_spec.update_layout(
        showlegend=False,
        height=400,
        paper_bgcolor='#1E293B',
        plot_bgcolor='#0F172A',
        font=dict(color='#F1F5F9', size=12),
        title_font=dict(size=16, color='#F1F5F9'),
        xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
        yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
        coloraxis_colorbar=dict(
            title_font_color='#CBD5E1',
            tickfont_color='#CBD5E1'
        )
    )
    st.plotly_chart(fig_spec, use_container_width=True)
    
    # Relationship between capital and client types
    st.markdown("### Distribución de Capital por Segmento de Cliente")
    
    fig_box = go.Figure()
    
    for segment, column, color in [('Minoristas', 'serves_retail', '#60A5FA'),
                                   ('Profesionales', 'serves_professional', '#34D399'),
                                   ('Contrapartes Elegibles', 'serves_eligible', '#FBBF24')]:
        segment_data = df[df[column] == True]['capital_social_numeric']
        fig_box.add_trace(go.Box(
            y=segment_data,
            name=segment,
            marker_color=color
        ))
    
    fig_box.update_layout(
        title="Distribución de Capital Social por Tipo de Cliente Atendido",
        yaxis_title="Capital Social (€)",
        yaxis_type="log",
        height=400,
        paper_bgcolor='#1E293B',
        plot_bgcolor='#0F172A',
        font=dict(color='#F1F5F9', size=12),
        title_font=dict(size=16, color='#F1F5F9'),
        xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
        yaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
        legend=dict(
            font=dict(color='#CBD5E1'),
            bgcolor='#1E293B',
            bordercolor='#334155',
            borderwidth=1
        )
    )
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Top entities by client segment
    st.markdown("### Top Entidades por Segmento de Cliente")
    
    tab1, tab2, tab3 = st.tabs(["Especialistas Minoristas", "Enfoque Profesional", "Servicio Completo"])
    
    with tab1:
        retail_top = df[df['serves_retail'] == True].nlargest(10, 'capital_social_numeric')[
            ['nombre', 'capital_social', 'num_servicios_inversion', 'num_instrumentos']
        ]
        st.dataframe(retail_top, use_container_width=True)
    
    with tab2:
        professional_top = df[df['serves_professional'] == True].nlargest(10, 'capital_social_numeric')[
            ['nombre', 'capital_social', 'num_servicios_inversion', 'num_instrumentos']
        ]
        st.dataframe(professional_top, use_container_width=True)
    
    with tab3:
        full_service_top = full_service.nlargest(10, 'capital_social_numeric')[
            ['nombre', 'capital_social', 'num_servicios_inversion', 'num_instrumentos']
        ]
        st.dataframe(full_service_top, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0; color: #CBD5E1; background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-radius: 12px; margin-top: 2rem;'>
        <p style='font-size: 16px; margin-bottom: 1rem; color: #E2E8F0;'>📊 Dashboard de Análisis de Sociedades y Agencias de Valores y Empresas de Asesoramiento Financiero</p>
        <p style='color: #94A3B8;'>Última Actualización: Agosto 2025</p>
        <p style='margin-top: 1rem;'><strong>Desarrollado por <a href="https://twitter.com/Gsnchez" target="_blank" style="color: #60A5FA; text-decoration: none;">@Gsnchez</a> | <a href="https://bquantfinance.com" target="_blank" style="color: #60A5FA; text-decoration: none;">bquantfinance.com</a></strong></p>
    </div>
    """,
    unsafe_allow_html=True
)
