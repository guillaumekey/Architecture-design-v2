"""
SEO Sitemap Analyzer - Application principale (structure modulaire qui fonctionne)
"""

import streamlit as st
import pandas as pd
import logging

# Configuration de la page Streamlit
st.set_page_config(layout="wide", page_title="SEO Sitemap Analyzer")

# Imports des modules locaux
from config.translations import get_text, get_available_languages, get_translated_dimension_options
from core.sitemap_analyzer import analyze_website
from core.semrush_processor import process_semrush_files
from core.data_merger import create_main_dataframe, create_directory_performance_summary
from visualizations.charts import plot_global_performance
from ui.components import (
    render_url_input, render_custom_sitemaps_section,
    render_analysis_options, render_semrush_section, render_exclusions_section, render_sidebar
)
from ui.filters import (
    render_navigation_filters, render_statistics_metrics, render_filtered_dataframe
)
from utils.data_utils import clean_exclusions


def render_language_selector():
    """Affiche le sélecteur de langue."""
    languages = get_available_languages()
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        selected_lang_display = st.selectbox(
            get_text('language_selector', st.session_state.selected_language),
            options=list(languages.values()),
            index=list(languages.keys()).index(st.session_state.selected_language)
        )

        # Récupérer le code de langue à partir de l'affichage
        selected_lang_code = [k for k, v in languages.items() if v == selected_lang_display][0]

        if selected_lang_code != st.session_state.selected_language:
            st.session_state.selected_language = selected_lang_code

            # CORRECTION: Régénérer le treemap si l'analyse est déjà faite
            if st.session_state.analysis_done and not st.session_state.directories_df.empty:
                import datetime
                import plotly.express as px

                # Récréer le treemap avec la nouvelle langue
                domain = st.session_state.directories_df['dominio'].iloc[
                    0] if 'dominio' in st.session_state.directories_df.columns else 'site'
                today = datetime.datetime.now(datetime.timezone.utc).strftime('%B %d, %Y')

                st.session_state.treemap_fig = px.treemap(
                    st.session_state.directories_df,
                    path=['dominio', 'dir_1', 'dir_2', 'dir_3'],
                    title=f'{domain} Categories Structure (date: {today})',
                    height=750
                )

                # Template et hover traduits avec la nouvelle langue
                st.session_state.treemap_fig.update_traces(
                    texttemplate=f"<b>%{{label}}</b><br>{get_text('pages', selected_lang_code)}: %{{value}}<br>%{{percentParent}} {get_text('of_parent', selected_lang_code)}<br>%{{percentRoot}} {get_text('of_total', selected_lang_code)}",
                    root_color="lightgrey",
                    hovertemplate=(
                        f"<b>%{{label}}</b><br>"
                        f"{get_text('label', selected_lang_code)}: %{{label}}<br>"
                        f"{get_text('count_label', selected_lang_code)}: %{{value}}<br>"
                        f"{get_text('parent_label', selected_lang_code)}: %{{parent}}<br>"
                        f"{get_text('id_label', selected_lang_code)}: %{{id}}"
                        "<extra></extra>"
                    )
                )

            st.rerun()

logger = logging.getLogger(__name__)

# Initialisation des variables de session (EXACTEMENT comme dans l'original)
if 'url_df' not in st.session_state:
    st.session_state.url_df = pd.DataFrame()
if 'directories_df' not in st.session_state:
    st.session_state.directories_df = pd.DataFrame()
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'treemap_fig' not in st.session_state:
    st.session_state.treemap_fig = None
if 'semrush_data' not in st.session_state:
    st.session_state.semrush_data = pd.DataFrame()
if 'num_semrush_files' not in st.session_state:
    st.session_state.num_semrush_files = 2
if 'num_custom_sitemaps' not in st.session_state:
    st.session_state.num_custom_sitemaps = 1
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'fr'

# Interface utilisateur (structure exacte de l'original avec modules)

# Sélecteur de langue
render_language_selector()
lang = st.session_state.selected_language

st.title(get_text('app_title', lang))

# Sidebar
render_sidebar(lang)

# Entrée URL
url = render_url_input(lang)

# Section des sitemaps personnalisés
custom_sitemaps = render_custom_sitemaps_section(lang)

# Options d'analyse
max_categories, show_single_items = render_analysis_options(lang)

# Section SEMrush
semrush_files, selected_markets = render_semrush_section(lang)

# Section des exclusions
exclude_dir1, exclude_dir2, exclude_dir3 = render_exclusions_section(lang)

# Bouton d'analyse
if st.button(get_text('analyze_button', lang)):
    if url:
        # Traitement des fichiers SEMrush
        logger.info("Début du traitement global")
        semrush_df = process_semrush_files(semrush_files, selected_markets)
        if not semrush_df.empty:
            st.session_state.semrush_data = semrush_df
            logger.info(f"Données SEMrush traitées: {len(semrush_df)} lignes")

        exclusions = {
            'dir_1': clean_exclusions(exclude_dir1),
            'dir_2': clean_exclusions(exclude_dir2),
            'dir_3': clean_exclusions(exclude_dir3)
        }

        # Affichage des exclusions actives
        active_exclusions = {level: terms for level, terms in exclusions.items() if terms}
        if active_exclusions:
            logger.info(f"Exclusions actives: {active_exclusions}")
            st.info(f"{get_text('active_exclusions', lang)}")
            for level, terms in active_exclusions.items():
                st.write(f"- {level}: {', '.join(terms)}")

        analyze_website(url, custom_sitemaps, max_categories, show_single_items, exclusions)
    else:
        logger.error("URL non fournie")
        st.error(get_text('enter_valid_url', lang))

# Affichage des résultats
if st.session_state.analysis_done:
    # Treemap
    st.plotly_chart(st.session_state.treemap_fig, use_container_width=True)

    # Filtres de navigation
    selected_category, selected_subcategory, selected_subsubcategory = render_navigation_filters(
        st.session_state.directories_df, lang
    )

    # Statistiques
    render_statistics_metrics(
        st.session_state.directories_df,
        selected_category,
        selected_subcategory,
        selected_subsubcategory,
        lang
    )

    # Tableau filtré
    render_filtered_dataframe(
        st.session_state.directories_df,
        selected_category,
        selected_subcategory,
        selected_subsubcategory,
        lang
    )

# Section SEMrush (si des données sont disponibles)
if not st.session_state.semrush_data.empty:
    st.markdown(f"### {get_text('semrush_statistics', lang)}")

    # CORRECTION: Traduction des en-têtes de colonnes SEMrush
    semrush_display_df = st.session_state.semrush_data.copy()
    column_translations = {
        'Keyword': get_text('keyword', lang),
        'Position': get_text('position', lang),
        'Previous position': get_text('previous_position', lang),
        'Search Volume': get_text('search_volume', lang),
        'Keyword Difficulty': get_text('keyword_difficulty', lang),
        'CPC': get_text('cpc', lang),
        'URL': get_text('url', lang),
        'Traffic': get_text('traffic', lang),
        'Traffic (%)': get_text('traffic_percent', lang),
        'Traffic Cost': get_text('traffic_cost', lang)
    }

    # Renommer les colonnes si elles existent
    for old_name, new_name in column_translations.items():
        if old_name in semrush_display_df.columns:
            semrush_display_df = semrush_display_df.rename(columns={old_name: new_name})

    st.dataframe(semrush_display_df, use_container_width=True)

    # Création et affichage du main dataframe
    st.markdown(f"### {get_text('semrush_url_statistics', lang)}")
    urls_in_sitemap, urls_not_in_sitemap = create_main_dataframe(
        st.session_state.directories_df,
        st.session_state.semrush_data
    )

    if not urls_in_sitemap.empty:
        # CORRECTION: Traduction des colonnes du tableau principal
        display_columns = {
            'url': get_text('url', lang),
            'dir_1': 'Dir_1',
            'dir_2': 'Dir_2',
            'dir_3': 'Dir_3',
            'Traffic': get_text('traffic', lang),
            'Number of Keywords': get_text('number_of_keywords', lang),
            'market': get_text('market', lang),
            'Search Volume': get_text('search_volume', lang),
            'Position Type': get_text('position_type', lang)
        }

        urls_display_df = urls_in_sitemap[list(display_columns.keys())].copy()
        urls_display_df = urls_display_df.rename(columns=display_columns)

        st.dataframe(urls_display_df, use_container_width=True)

    # URLs non présentes dans le sitemap
    if not urls_not_in_sitemap.empty:
        st.markdown(f"### {get_text('urls_not_in_sitemap', lang)}")

        # CORRECTION: Traduction des colonnes pour URLs non trouvées
        missing_columns = {
            'URL': get_text('url', lang),
            'Traffic': get_text('traffic', lang),
            'Number of Keywords': get_text('number_of_keywords', lang),
            'Search Volume': get_text('search_volume', lang),
            'Position Type': get_text('position_type', lang),
            'market': get_text('market', lang)
        }

        missing_display_df = urls_not_in_sitemap[list(missing_columns.keys())].copy()
        missing_display_df = missing_display_df.rename(columns=missing_columns)

        st.dataframe(missing_display_df, use_container_width=True)

    # Résumé des performances par niveau de directory
    st.markdown(f"### {get_text('results_by_page_level', lang)}")

    # Filtres pour les niveaux de directory
    perf_col1, perf_col2 = st.columns(2)
    with perf_col1:
        dir_1_options = [get_text('all', lang)] + sorted(urls_in_sitemap['dir_1'].unique().tolist())
        selected_dir_1 = st.selectbox(get_text('filter_by_dir1', lang), dir_1_options, key='perf_dir_1')

    with perf_col2:
        dir_2_options = [get_text('all', lang)]
        if selected_dir_1 != get_text('all', lang):
            dir_2_options += sorted(
                urls_in_sitemap[urls_in_sitemap['dir_1'] == selected_dir_1]['dir_2'].unique().tolist()
            )
        selected_dir_2 = st.selectbox(get_text('filter_by_dir2', lang), dir_2_options, key='perf_dir_2')

    # Convertir les sélections traduites vers les valeurs originales
    selected_dir_1 = selected_dir_1 if selected_dir_1 != get_text('all', lang) else 'Toutes'
    selected_dir_2 = selected_dir_2 if selected_dir_2 != get_text('all', lang) else 'Toutes'

    # Création et affichage du tableau de résumé
    dir_1_filter = selected_dir_1 if selected_dir_1 != 'Toutes' else None
    dir_2_filter = selected_dir_2 if selected_dir_2 != 'Toutes' else None

    performance_summary = create_directory_performance_summary(
        st.session_state.directories_df,
        urls_in_sitemap,
        dir_1_filter,
        dir_2_filter
    )

    # CORRECTION: Traduction complète du tableau de performance
    performance_display_df = performance_summary.copy()
    performance_translations = {
        'Directory': get_text('directory', lang),
        'Niveau': get_text('level', lang),
        'Nombre URLs': get_text('url_count', lang),
        'Traffic Total': get_text('total_traffic', lang),
        'Total Mots-clés': get_text('total_keywords', lang),
        'Volume Total': get_text('total_volume', lang)
    }
    performance_display_df = performance_display_df.rename(columns=performance_translations)

    # Affichage du tableau principal
    st.dataframe(
        performance_display_df,
        use_container_width=True,
        column_config={
            get_text('directory', lang): st.column_config.TextColumn(get_text('directory', lang), width=150),
            get_text('level', lang): st.column_config.TextColumn(get_text('level', lang), width=100),
            get_text('url_count', lang): st.column_config.NumberColumn(get_text('url_count', lang), width=120),
            get_text('total_traffic', lang): st.column_config.NumberColumn(get_text('total_traffic', lang), width=120),
            get_text('total_keywords', lang): st.column_config.NumberColumn(get_text('total_keywords', lang),
                                                                            width=120),
            get_text('total_volume', lang): st.column_config.NumberColumn(get_text('total_volume', lang), width=120)
        }
    )

    # Totaux
    total_cols = st.columns(4)
    total_cols[0].metric(
        label=get_text('total_url_count', lang),
        value=f"{performance_summary['Nombre URLs'].sum():,}"
    )
    total_cols[1].metric(
        label=get_text('total_traffic_sum', lang),
        value=f"{performance_summary['Traffic Total'].sum():,}"
    )
    total_cols[2].metric(
        label=get_text('total_keywords_metric', lang),
        value=f"{performance_summary['Total Mots-clés'].sum():,}"
    )
    total_cols[3].metric(
        label=get_text('total_volume_sum', lang),
        value=f"{performance_summary['Volume Total'].sum():,}"
    )

    # Scatter Plot avec traductions complètes
    st.markdown(f"### {get_text('global_performance', lang)}")
    st.markdown(f"### {get_text('configure_scatter', lang)}")

    scatter_col1, scatter_col2, scatter_col3 = st.columns(3)

    # CORRECTION: Utilisation des options traduites pour le scatter plot
    dimension_options = get_translated_dimension_options(lang)

    with scatter_col1:
        x_dimension_display = st.selectbox(
            get_text('x_axis', lang),
            options=list(dimension_options.keys()),
            index=0
        )
        x_dimension = dimension_options[x_dimension_display]

    with scatter_col2:
        y_dimension_display = st.selectbox(
            get_text('y_axis', lang),
            options=list(dimension_options.keys()),
            index=1
        )
        y_dimension = dimension_options[y_dimension_display]

    with scatter_col3:
        size_dimension_display = st.selectbox(
            get_text('bubble_size', lang),
            options=list(dimension_options.keys()),
            index=2
        )
        size_dimension = dimension_options[size_dimension_display]

    plot_global_performance(performance_summary, x_dimension, y_dimension, size_dimension, lang)