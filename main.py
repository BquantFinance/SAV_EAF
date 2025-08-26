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

# Custom CSS for better aesthetics
st.markdown("""
<style>
    /* Main color theme */
    :root {
        --primary-color: #1E3A8A;
        --secondary-color: #F59E0B;
        --success-color: #10B981;
        --danger-color: #EF4444;
        --neutral-color: #6B7280;
    }
    
    /* Custom metric cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: none;
    }
    
    div[data-testid="metric-container"] > div {
        color: white !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3a8a 0%, #312e81 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        background: linear-gradient(90deg, #1e3a8a 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    /* Dataframe styling */
    .dataframe {
        font-size: 12px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: bold;
        transition: transform 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: transparent;
        border-radius: 8px 8px 0px 0px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(90deg, #1e3a8a 0%, #7c3aed 100%);
        color: white;
        text-align: center;
        padding: 10px;
        z-index: 999;
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

st.sidebar.markdown("---")
st.sidebar.markdown("**Desarrollado por [@Gsnchez](https://twitter.com/Gsnchez)**")
st.sidebar.markdown("**[bquantfinance.com](https://bquantfinance.com)**")

# Page: Overview
if page == "🏠 Vista General":
    st.title("📊 Dashboard de Sociedades y Agencias de Valores y Empresas de Asesoramiento Financiero")
    st.markdown("### Análisis en Tiempo Real de Entidades Financieras Españolas")
    
    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Entidades",
            f"{len(df):,}",
            delta=f"SAV: {len(df[df['tipo_entidad'] == 'SAV'])}, EAF: {len(df[df['tipo_entidad'] == 'EAF'])}"
        )
    
    with col2:
        total_capital = df['capital_social_numeric'].sum()
        st.metric(
            "Capital Total",
            f"€{total_capital/1e9:.2f}MM",
            delta=f"Media: €{df['capital_social_numeric'].mean()/1e6:.2f}M"
        )
    
    with col3:
        intl_presence = df['has_international_presence'].sum()
        st.metric(
            "Presencia Internacional",
            f"{intl_presence}",
            delta=f"{(intl_presence/len(df)*100):.1f}% de entidades"
        )
    
    with col4:
        avg_services = df['total_services'].mean()
        st.metric(
            "Media Servicios",
            f"{avg_services:.1f}",
            delta=f"Máx: {df['total_services'].max()}"
        )
    
    with col5:
        audited = df['num_auditorias'].notna().sum()
        st.metric(
            "Entidades Auditadas",
            f"{audited}",
            delta=f"{(audited/len(df)*100):.1f}%"
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
            color_discrete_map={'SAV': '#667eea', 'EAF': '#764ba2'},
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=400)
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
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(height=400, showlegend=False)
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
            color_discrete_map={'SAV': '#667eea', 'EAF': '#764ba2'},
            log_y=True
        )
        fig_box.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        # Services heatmap
        services_data = df.groupby('tipo_entidad')[['num_servicios_inversion', 'num_servicios_auxiliares']].mean()
        fig_heat = go.Figure(data=go.Heatmap(
            z=services_data.values,
            x=['Servicios de Inversión', 'Servicios Auxiliares'],
            y=services_data.index,
            colorscale='Viridis',
            text=services_data.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 14},
            hoverongaps=False
        ))
        fig_heat.update_layout(
            title="Promedio de Servicios por Tipo de Entidad",
            height=400,
            xaxis_title="Tipo de Servicio",
            yaxis_title="Tipo de Entidad"
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
        color_discrete_map={'SAV': '#667eea', 'EAF': '#764ba2'}
    )
    fig_timeline.update_layout(height=300)
    st.plotly_chart(fig_timeline, use_container_width=True)

# Page: Entity Explorer
elif page == "🔍 Explorador de Entidades":
    st.title("🔍 Explorador de Entidades")
    st.markdown("Busque y filtre todas las entidades reguladas")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        entity_type = st.selectbox("Tipo de Entidad", ["Todas"] + list(df['tipo_entidad'].unique()))
    
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
    
    # Search box
    search_term = st.text_input("🔎 Buscar por nombre de entidad", placeholder="Ingrese el nombre de la entidad...")
    
    # Apply filters
    filtered_df = df.copy()
    
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
    
    if search_term:
        filtered_df = filtered_df[filtered_df['nombre'].str.contains(search_term, case=False, na=False)]
    
    # Results summary
    st.markdown(f"### Se encontraron {len(filtered_df)} entidades")
    
    # Display options
    col1, col2 = st.columns([3, 1])
    with col2:
        view_mode = st.radio("Modo de Vista", ["Tabla", "Tarjetas"], horizontal=True)
    
    if view_mode == "Tabla":
        # Table view
        display_columns = ['nombre', 'tipo_entidad', 'numero_registro', 'direccion_provincia', 
                          'capital_social', 'num_servicios_inversion', 'num_servicios_auxiliares',
                          'num_instrumentos', 'fogain']
        
        st.dataframe(
            filtered_df[display_columns].style.format({
                'capital_social': '€{}'
            }),
            use_container_width=True,
            height=600
        )
    else:
        # Cards view
        for idx, row in filtered_df.head(20).iterrows():
            with st.expander(f"🏢 {row['nombre']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Tipo:** {row['tipo_entidad']}")
                    st.markdown(f"**Nº Registro:** {row['numero_registro']}")
                    st.markdown(f"**Fecha Registro:** {row['fecha_registro']}")
                
                with col2:
                    st.markdown(f"**Capital Social:** €{row['capital_social']}")
                    st.markdown(f"**Provincia:** {row['direccion_provincia']}")
                    st.markdown(f"**FOGAIN:** {row['fogain']}")
                
                with col3:
                    st.markdown(f"**Servicios Inversión:** {row['num_servicios_inversion']}")
                    st.markdown(f"**Servicios Auxiliares:** {row['num_servicios_auxiliares']}")
                    st.markdown(f"**Instrumentos:** {row['num_instrumentos']}")
    
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
        
        colors = ['#667eea', '#764ba2', '#10B981', '#F59E0B']
        
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
                    range=[0, 100]
                )),
            showlegend=True,
            title="Comparación de Servicios e Instrumentos",
            height=500
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
            fig_capital.update_layout(showlegend=False, height=400)
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
                color_discrete_map={'Servicios de Inversión': '#667eea', 'Servicios Auxiliares': '#764ba2'}
            )
            fig_services.update_layout(height=400)
            st.plotly_chart(fig_services, use_container_width=True)
        
        # Detailed comparison table
        st.markdown("### Comparación Detallada")
        
        comparison_fields = ['nombre', 'tipo_entidad', 'capital_social', 'direccion_provincia',
                            'num_servicios_inversion', 'num_servicios_auxiliares', 'num_instrumentos',
                            'fogain', 'num_auditorias', 'tipos_clientes']
        
        comparison_table = compare_df[comparison_fields].T
        comparison_table.columns = [name[:30] + '...' if len(name) > 30 else name for name in entities]
        
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
        color_continuous_scale='Viridis'
    )
    fig_map.update_layout(height=500)
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
            color_continuous_scale='Viridis',
            hover_data=['Capital Total', 'Presencia Internacional']
        )
        fig_top.update_layout(height=400)
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
            hole=0.4
        )
        fig_capital.update_traces(textposition='inside', textinfo='percent+label')
        fig_capital.update_layout(height=400)
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
        color_continuous_scale='Viridis',
        text=intl_by_type['percentage'].round(1)
    )
    fig_intl.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_intl.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_intl, use_container_width=True)

# Page: Services Analysis
elif page == "💼 Análisis de Servicios":
    st.title("💼 Análisis de Servicios")
    st.markdown("Análisis profundo de servicios de inversión y auxiliares")
    
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Investment services histogram
        fig_inv = px.histogram(
            df,
            x='num_servicios_inversion',
            title="Distribución de Servicios de Inversión",
            labels={'num_servicios_inversion': 'Número de Servicios de Inversión', 'count': 'Número de Entidades'},
            color_discrete_sequence=['#667eea'],
            nbins=15
        )
        fig_inv.update_layout(height=400)
        st.plotly_chart(fig_inv, use_container_width=True)
    
    with col2:
        # Auxiliary services histogram
        fig_aux = px.histogram(
            df,
            x='num_servicios_auxiliares',
            title="Distribución de Servicios Auxiliares",
            labels={'num_servicios_auxiliares': 'Número de Servicios Auxiliares', 'count': 'Número de Entidades'},
            color_discrete_sequence=['#764ba2'],
            nbins=15
        )
        fig_aux.update_layout(height=400)
        st.plotly_chart(fig_aux, use_container_width=True)
    
    # Services correlation
    st.markdown("### Análisis de Correlación de Servicios")
    
    # Create correlation matrix
    services_corr = df[['num_servicios_inversion', 'num_servicios_auxiliares', 
                        'num_instrumentos', 'capital_social_numeric', 'years_operating']].corr()
    
    fig_corr = px.imshow(
        services_corr,
        title="Matriz de Correlación de Servicios",
        labels=dict(x="Variable", y="Variable", color="Correlación"),
        x=['Servicios Inversión', 'Servicios Auxiliares', 'Instrumentos', 'Capital Social', 'Años Operando'],
        y=['Servicios Inversión', 'Servicios Auxiliares', 'Instrumentos', 'Capital Social', 'Años Operando'],
        color_continuous_scale='RdBu',
        aspect="auto",
        text_auto='.2f'
    )
    fig_corr.update_layout(height=500)
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Instruments analysis
    st.markdown("### 📈 Cobertura de Instrumentos Financieros")
    
    # Instrument distribution
    instrument_ranges = pd.cut(df['num_instrumentos'], bins=[0, 3, 6, 9, 15], 
                               labels=['1-3', '4-6', '7-9', '10+'])
    instrument_dist = instrument_ranges.value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_inst = px.pie(
            values=instrument_dist.values,
            names=instrument_dist.index,
            title="Distribución de Rango de Instrumentos",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig_inst.update_traces(textposition='inside', textinfo='percent+label')
        fig_inst.update_layout(height=400)
        st.plotly_chart(fig_inst, use_container_width=True)
    
    with col2:
        # Instruments by entity type
        inst_by_type = df.groupby('tipo_entidad')['num_instrumentos'].agg(['mean', 'std', 'max'])
        inst_by_type = inst_by_type.reset_index()
        
        fig_inst_type = go.Figure()
        fig_inst_type.add_trace(go.Bar(name='Media', x=inst_by_type['tipo_entidad'], y=inst_by_type['mean'],
                                       marker_color='#667eea'))
        fig_inst_type.add_trace(go.Bar(name='Máximo', x=inst_by_type['tipo_entidad'], y=inst_by_type['max'],
                                       marker_color='#764ba2'))
        fig_inst_type.update_layout(
            title="Instrumentos por Tipo de Entidad",
            xaxis_title="Tipo de Entidad",
            yaxis_title="Número de Instrumentos",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig_inst_type, use_container_width=True)
    
    # Top entities by services
    st.markdown("### 🏆 Principales Proveedores de Servicios")
    
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
        color_discrete_map={'num_servicios_inversion': '#667eea', 'num_servicios_auxiliares': '#764ba2'}
    )
    fig_top_services.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_top_services, use_container_width=True)

# Page: Financial Health
elif page == "💰 Salud Financiera":
    st.title("💰 Dashboard de Salud Financiera")
    st.markdown("Análisis de distribución de capital y cumplimiento de auditorías")
    
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
    
    # Capital distribution
    col1, col2 = st.columns(2)
    
    with col1:
        # Log scale distribution
        fig_dist = px.histogram(
            df,
            x='capital_social_numeric',
            title="Distribución de Capital Social (Escala Log)",
            labels={'capital_social_numeric': 'Capital Social (€)', 'count': 'Número de Entidades'},
            color='tipo_entidad',
            color_discrete_map={'SAV': '#667eea', 'EAF': '#764ba2'},
            marginal="box",
            log_x=True,
            nbins=50
        )
        fig_dist.update_layout(height=500)
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        # Violin plot by entity type
        fig_violin = px.violin(
            df,
            y='capital_social_numeric',
            x='tipo_entidad',
            title="Distribución de Capital por Tipo de Entidad",
            labels={'capital_social_numeric': 'Capital Social (€)', 'tipo_entidad': 'Tipo de Entidad'},
            color='tipo_entidad',
            color_discrete_map={'SAV': '#667eea', 'EAF': '#764ba2'},
            box=True,
            log_y=True
        )
        fig_violin.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_violin, use_container_width=True)
    
    # Capital concentration
    st.markdown("### 📊 Análisis de Concentración de Capital")
    
    # Calculate capital concentration (Lorenz curve / Gini coefficient style)
    df_sorted = df.sort_values('capital_social_numeric')
    df_sorted['cumulative_entities'] = np.arange(1, len(df_sorted) + 1) / len(df_sorted) * 100
    df_sorted['cumulative_capital'] = df_sorted['capital_social_numeric'].cumsum() / df_sorted['capital_social_numeric'].sum() * 100
    
    fig_lorenz = go.Figure()
    fig_lorenz.add_trace(go.Scatter(
        x=df_sorted['cumulative_entities'],
        y=df_sorted['cumulative_capital'],
        mode='lines',
        name='Distribución Real',
        line=dict(color='#667eea', width=3)
    ))
    fig_lorenz.add_trace(go.Scatter(
        x=[0, 100],
        y=[0, 100],
        mode='lines',
        name='Igualdad Perfecta',
        line=dict(color='gray', width=2, dash='dash')
    ))
    fig_lorenz.update_layout(
        title="Curva de Concentración de Capital",
        xaxis_title="% Acumulativo de Entidades",
        yaxis_title="% Acumulativo de Capital",
        height=400,
        showlegend=True
    )
    st.plotly_chart(fig_lorenz, use_container_width=True)
    
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
            color_continuous_scale='Viridis',
            text=audit_by_type['mean'].round(1)
        )
        fig_audit.update_traces(texttemplate='%{text}', textposition='outside')
        fig_audit.update_layout(showlegend=False, height=400)
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
            color_continuous_scale='Viridis'
        )
        fig_auditors.update_layout(height=400, showlegend=False)
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
            color_discrete_sequence=['#667eea', '#764ba2', '#10B981']
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=400)
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
            color_continuous_scale='Viridis'
        )
        fig_combo.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_combo, use_container_width=True)
    
    # Client segmentation by services
    st.markdown("### Oferta de Servicios por Tipo de Cliente")
    
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
        colorscale='Viridis',
        text=segment_df[['Media Servicios Inversión', 'Media Servicios Auxiliares', 'Media Instrumentos']].values.round(2),
        texttemplate='%{text}',
        textfont={"size": 14},
        hoverongaps=False
    ))
    fig_heat.update_layout(
        title="Promedio de Servicios por Segmento de Cliente",
        height=400
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
        color_continuous_scale='Viridis',
        text='Cantidad'
    )
    fig_spec.update_traces(texttemplate='%{text}', textposition='outside')
    fig_spec.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_spec, use_container_width=True)
    
    # Relationship between capital and client types
    st.markdown("### Distribución de Capital por Segmento de Cliente")
    
    fig_box = go.Figure()
    
    for segment, column, color in [('Minoristas', 'serves_retail', '#667eea'),
                                   ('Profesionales', 'serves_professional', '#764ba2'),
                                   ('Contrapartes Elegibles', 'serves_eligible', '#10B981')]:
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
        height=400
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
    <div style='text-align: center; color: #666;'>
        <p>📊 Dashboard de Análisis de Sociedades y Agencias de Valores y Empresas de Asesoramiento Financiero</p>
        <p>Última Actualización: Agosto 2025</p>
        <p><strong>Desarrollado por <a href="https://twitter.com/Gsnchez" target="_blank">@Gsnchez</a> | <a href="https://bquantfinance.com" target="_blank">bquantfinance.com</a></strong></p>
    </div>
    """,
    unsafe_allow_html=True
)
