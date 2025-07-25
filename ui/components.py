"""
Composants UI réutilisables
"""

import streamlit as st
from config.settings import MARKETS
from config.translations import get_text


def render_url_input(lang='fr'):
    """Affiche le champ de saisie de l'URL."""
    col1, col2 = st.columns(2)
    with col1:
        url = st.text_input(get_text('url_input', lang))
    return url


def render_custom_sitemaps_section(lang='fr'):
    """Affiche la section des sitemaps personnalisés."""
    st.subheader(get_text('custom_sitemaps_title', lang))

    custom_sitemaps = []
    for i in range(st.session_state.get('num_custom_sitemaps', 1)):
        custom_sitemap = st.text_input(f"{get_text('sitemap_url', lang)} #{i + 1}", key=f"custom_sitemap_{i}")
        if custom_sitemap:
            custom_sitemaps.append(custom_sitemap)

    if st.session_state.get('num_custom_sitemaps', 1) < 5:  # Limite à 5 sitemaps max
        if st.button(get_text('add_sitemap', lang)):
            st.session_state['num_custom_sitemaps'] = st.session_state.get('num_custom_sitemaps', 1) + 1
            st.rerun()

    return custom_sitemaps


def render_analysis_options(lang='fr'):
    """Affiche les options d'analyse."""
    max_categories = st.number_input(get_text('max_categories', lang), -1, 100, -1)
    show_single_items = st.checkbox(get_text('show_single_items', lang))
    return max_categories, show_single_items


def render_semrush_section(lang='fr'):
    """Affiche la section SEMrush."""
    st.header(get_text('semrush_title', lang))

    semrush_files = []
    selected_markets = []

    for i in range(st.session_state.get('num_semrush_files', 2)):
        col1, col2 = st.columns([3, 1])
        with col1:
            file = st.file_uploader(f"{get_text('semrush_file', lang)} #{i + 1}", type=['csv'], key=f"semrush_file_{i}")
            semrush_files.append(file)
        with col2:
            market = st.selectbox(get_text('market', lang), MARKETS, key=f"market_{i}")
            selected_markets.append(market)

    if st.session_state.get('num_semrush_files', 2) < 6:
        if st.button(get_text('add_file', lang), key="add_semrush_file_btn"):
            st.session_state['num_semrush_files'] = st.session_state.get('num_semrush_files', 2) + 1
            st.rerun()

    return semrush_files, selected_markets


def render_exclusions_section(lang='fr'):
    """Affiche la section des exclusions."""
    st.subheader(get_text('exclusions_title', lang))
    col1, col2, col3 = st.columns(3)

    with col1:
        exclude_dir1 = st.text_input(
            get_text('exclusions_dir1', lang),
            help=get_text('exclusions_help1', lang)
        )

    with col2:
        exclude_dir2 = st.text_input(
            get_text('exclusions_dir2', lang),
            help=get_text('exclusions_help2', lang)
        )

    with col3:
        exclude_dir3 = st.text_input(
            get_text('exclusions_dir3', lang),
            help=get_text('exclusions_help3', lang)
        )

    return exclude_dir1, exclude_dir2, exclude_dir3


def render_sidebar(lang='fr'):
    """Affiche la sidebar avec les informations."""
    st.sidebar.markdown(f"""
    ### {get_text('about', lang)}
    {get_text('about_description', lang)}

    #### {get_text('features', lang)}
    - {get_text('feature_sitemap', lang)}
    - {get_text('feature_treemap', lang)}
    - {get_text('feature_filtering', lang)}
    - {get_text('feature_exclusion', lang)}
    - {get_text('feature_semrush', lang)}

    #### {get_text('usage_guide', lang)}

    **{get_text('max_categories', lang)} :**  
    {get_text('max_categories_help', lang)}

    **{get_text('exclusions_config', lang)} :**  
    {get_text('exclusions_warning', lang)}
    """)