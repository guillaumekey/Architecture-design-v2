"""
Logique des filtres et navigation dans l'interface (structure qui fonctionne)
"""

import streamlit as st
from utils.data_utils import get_url_statistics, filter_and_display_urls
from config.translations import get_text

def render_navigation_filters(directories_df, lang='fr'):
    """Affiche les filtres de navigation et retourne les sélections."""
    st.write(f"### {get_text('navigation_filters', lang)}")
    cols = st.columns(3)

    with cols[0]:
        categories = [get_text('all', lang)] + sorted(directories_df['dir_1'].unique())
        selected_category = st.selectbox(get_text('select_category', lang), categories)

    with cols[1]:
        subcategories = [get_text('all', lang)]
        if selected_category != get_text('all', lang):
            subcategories += sorted(
                directories_df[
                    directories_df['dir_1'] == selected_category
                ]['dir_2'].unique().tolist()
            )
        selected_subcategory = st.selectbox(get_text('select_subcategory', lang), subcategories)

    with cols[2]:
        subsubcategories = [get_text('all', lang)]
        if selected_subcategory != get_text('all', lang) and selected_category != get_text('all', lang):
            subsubcategories += sorted(
                directories_df[
                    (directories_df['dir_1'] == selected_category) &
                    (directories_df['dir_2'] == selected_subcategory)
                ]['dir_3'].unique().tolist()
            )
        selected_subsubcategory = st.selectbox(get_text('select_subsubcategory', lang), subsubcategories)

    # Convertir les sélections traduites vers les valeurs originales
    selected_category = selected_category if selected_category != get_text('all', lang) else 'Toutes'
    selected_subcategory = selected_subcategory if selected_subcategory != get_text('all', lang) else 'Toutes'
    selected_subsubcategory = selected_subsubcategory if selected_subsubcategory != get_text('all', lang) else 'Toutes'

    return selected_category, selected_subcategory, selected_subsubcategory


def render_statistics_metrics(directories_df, selected_category, selected_subcategory, selected_subsubcategory,
                              lang='fr'):
    """Affiche les métriques de statistiques."""
    st.markdown(f"### {get_text('url_statistics', lang)}")

    with st.container():
        metrics_cols = st.columns([1, 1, 1, 1])
        stats = get_url_statistics(directories_df, selected_category, selected_subcategory, selected_subsubcategory)

        metrics_cols[0].metric(
            label=get_text('total_urls', lang),
            value=stats['total'],
            help=get_text('total_urls_help', lang)
        )

        # CORRECTION: Utiliser la nouvelle traduction pour les catégories
        if stats['dir1'][0] != '-':
            if stats['dir1'][0] == 'Toutes':
                label = get_text('category_urls', lang)
            else:
                label = f"{get_text('category_urls', lang)} {stats['dir1'][0]}"
        else:
            label = f"URLs Dir_1"

        metrics_cols[1].metric(
            label=label,
            value=stats['dir1'][1],
            help=get_text('category_urls_help', lang)
        )

        if stats['dir2'][0] != '-':
            label = f"URLs {stats['dir2'][0]}"
        else:
            label = f"URLs Dir_2"

        metrics_cols[2].metric(
            label=label,
            value=stats['dir2'][1],
            help=get_text('subcategory_urls_help', lang)
        )

        if stats['dir3'][0] != '-':
            label = f"URLs {stats['dir3'][0]}"
        else:
            label = f"URLs Dir_3"

        metrics_cols[3].metric(
            label=label,
            value=stats['dir3'][1],
            help=get_text('subsubcategory_urls_help', lang)
        )

def render_filtered_dataframe(directories_df, selected_category, selected_subcategory, selected_subsubcategory, lang='fr'):
    """Affiche le tableau filtré des URLs."""
    filtered_df = filter_and_display_urls(directories_df, selected_category, selected_subcategory, selected_subsubcategory)

    st.dataframe(
        filtered_df,
        use_container_width=True,
        column_config={
            "dominio": st.column_config.TextColumn(get_text('domain', lang), width=150),
            "dir_1": st.column_config.TextColumn("Dir_1", width=100),
            "dir_2": st.column_config.TextColumn("Dir_2", width=100),
            "dir_3": st.column_config.TextColumn("Dir_3", width=100),
            "url": st.column_config.TextColumn("URL", width=None),
        }
    )

def render_performance_filters(urls_in_sitemap, lang='fr'):
    """Affiche les filtres pour les performances par niveau de directory."""
    col1, col2 = st.columns(2)

    with col1:
        dir_1_options = [get_text('all', lang)] + sorted(urls_in_sitemap['dir_1'].unique().tolist())
        selected_dir_1 = st.selectbox(get_text('filter_by_dir1', lang), dir_1_options, key='perf_dir_1')

    with col2:
        dir_2_options = [get_text('all', lang)]
        if selected_dir_1 != get_text('all', lang):
            dir_2_options += sorted(
                urls_in_sitemap[urls_in_sitemap['dir_1'] == selected_dir_1]['dir_2'].unique().tolist()
            )
        selected_dir_2 = st.selectbox(get_text('filter_by_dir2', lang), dir_2_options, key='perf_dir_2')

    # Convertir les sélections traduites vers les valeurs originales
    selected_dir_1 = selected_dir_1 if selected_dir_1 != get_text('all', lang) else 'Toutes'
    selected_dir_2 = selected_dir_2 if selected_dir_2 != get_text('all', lang) else 'Toutes'

    return selected_dir_1, selected_dir_2
