import streamlit as st
import advertools as adv
import pandas as pd
import plotly.express as px
from urllib.parse import urlparse
import datetime
import concurrent.futures

# Configuration de la page Streamlit
st.set_page_config(layout="wide", page_title="SEO Sitemap Analyzer")

# Initialisation des variables de session
if 'url_df' not in st.session_state:
    st.session_state.url_df = pd.DataFrame()
if 'directories_df' not in st.session_state:
    st.session_state.directories_df = pd.DataFrame()
if 'traffic_df' not in st.session_state:
    st.session_state.traffic_df = pd.DataFrame()
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'treemap_fig' not in st.session_state:
    st.session_state.treemap_fig = None


def fetch_sitemap(url):
    """Récupère le sitemap d'une URL donnée."""
    try:
        sitemap_df = adv.sitemap_to_df(url)
        return sitemap_df
    except Exception as e:
        st.error(f"Erreur lors de la récupération du sitemap {url}: {e}")
        return pd.DataFrame()


def get_sitemap_urls(url, custom_sitemap=''):
    """Récupère les URLs du sitemap, soit depuis robots.txt, soit depuis un sitemap personnalisé."""
    if custom_sitemap:
        return [custom_sitemap]
    try:
        robots_url = f"{url.rstrip('/')}/robots.txt"
        robots_df = adv.robotstxt_to_df(robots_url)
        sitemap_urls = robots_df[robots_df['directive'].str.contains('Sitemap', case=False)]['content'].tolist()
        if not sitemap_urls:
            sitemap_urls.append(f"{url.rstrip('/')}/sitemap.xml")
        return sitemap_urls
    except Exception as e:
        st.warning(f"Impossible de lire robots.txt, utilisation du sitemap par défaut: {e}")
        return [f"{url.rstrip('/')}/sitemap.xml"]


def get_url_statistics(selected_category='Toutes', selected_subcategory='Toutes', selected_subsubcategory='Toutes'):
    """Calcule les statistiques des URLs pour chaque niveau de catégorie."""
    total_urls = len(st.session_state.directories_df)

    if selected_category == 'Toutes':
        return {
            'total': total_urls,
            'dir1': ('-', '-'),
            'dir2': ('-', '-'),
            'dir3': ('-', '-')
        }

    dir1_df = st.session_state.directories_df[st.session_state.directories_df['dir_1'] == selected_category]
    dir1_count = len(dir1_df)

    if selected_subcategory == 'Toutes':
        return {
            'total': total_urls,
            'dir1': (selected_category, dir1_count),
            'dir2': ('-', '-'),
            'dir3': ('-', '-')
        }

    dir2_df = dir1_df[dir1_df['dir_2'] == selected_subcategory]
    dir2_count = len(dir2_df)

    if selected_subsubcategory == 'Toutes':
        return {
            'total': total_urls,
            'dir1': (selected_category, dir1_count),
            'dir2': (selected_subcategory, dir2_count),
            'dir3': ('-', '-')
        }

    dir3_df = dir2_df[dir2_df['dir_3'] == selected_subsubcategory]
    dir3_count = len(dir3_df)

    return {
        'total': total_urls,
        'dir1': (selected_category, dir1_count),
        'dir2': (selected_subcategory, dir2_count),
        'dir3': (selected_subsubcategory, dir3_count)
    }


def filter_and_display_urls(selected_category, selected_subcategory='Toutes', selected_subsubcategory='Toutes'):
    """Filtre les URLs en fonction des catégories sélectionnées."""
    filtered_df = st.session_state.directories_df[st.session_state.directories_df['dir_1'] == selected_category]

    if selected_subcategory != 'Toutes':
        filtered_df = filtered_df[filtered_df['dir_2'] == selected_subcategory]

    if selected_subsubcategory != 'Toutes':
        filtered_df = filtered_df[filtered_df['dir_3'] == selected_subsubcategory]

    return filtered_df


def clean_exclusions(exclusion_string):
    """Nettoie et prépare la liste des exclusions."""
    if not exclusion_string:
        return []
    return [item.strip() for item in exclusion_string.split(',') if item.strip()]


def analyze_website(url, custom_sitemap='', max_categories=-1, show_single_items=False, exclusions=None):
    """Analyse un site web à partir de son sitemap avec gestion des exclusions par niveau."""
    if exclusions is None:
        exclusions = {'dir_1': [], 'dir_2': [], 'dir_3': []}

    domain = urlparse(url).netloc.replace('www.', '').split(".")[0]

    with st.spinner('Récupération des sitemaps...'):
        sitemap_urls = get_sitemap_urls(url, custom_sitemap)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            sitemaps = list(executor.map(fetch_sitemap, sitemap_urls))

        urls_df = pd.concat(sitemaps, ignore_index=True)

    if urls_df.empty:
        st.error("Aucune URL trouvée dans le sitemap")
        return None

    with st.spinner('Analyse des URLs...'):
        st.session_state.url_df = adv.url_to_df(urls_df['loc'].dropna().tolist())
        st.session_state.url_df['dominio'] = domain

        # Préparation des données pour les trois niveaux
        for dir_col in ['dir_1', 'dir_2', 'dir_3']:
            if dir_col not in st.session_state.url_df.columns:
                st.session_state.url_df[dir_col] = ""
            st.session_state.url_df[dir_col] = st.session_state.url_df[dir_col].replace('', 'no directory').astype(str)

        # Application des exclusions niveau par niveau
        exclude_mask = pd.Series(False, index=st.session_state.url_df.index)
        for dir_level, exclusion_list in exclusions.items():
            if exclusion_list:
                exclude_mask = exclude_mask | st.session_state.url_df[dir_level].isin(exclusion_list)

        if exclude_mask.any():
            st.session_state.url_df = st.session_state.url_df[~exclude_mask]

        # Gestion des catégories
        top_categories = st.session_state.url_df['dir_1'].value_counts()

        if not show_single_items:
            small_categories = top_categories[top_categories <= 1].index
            st.session_state.url_df.loc[
                st.session_state.url_df['dir_1'].isin(small_categories), 'dir_1'] = 'no directory'

        top_categories = st.session_state.url_df['dir_1'].value_counts()

        if max_categories > 0:
            top_categories = top_categories.head(max_categories)

        st.session_state.directories_df = st.session_state.url_df[
            st.session_state.url_df['dir_1'].isin(top_categories.index)
        ][['dominio', 'dir_1', 'dir_2', 'dir_3', 'url']]

        # Mise à jour des données de trafic
        if not st.session_state.traffic_df.empty:
            st.session_state.directories_df = st.session_state.directories_df.merge(
                st.session_state.traffic_df, on='url', how='left')
            for col in ['clicks', 'impressions', 'ctr', 'position']:
                st.session_state.directories_df[col] = st.session_state.directories_df[col].fillna(0)

        # Création du treemap
        today = datetime.datetime.utcnow().strftime('%B %d, %Y')
        st.session_state.treemap_fig = px.treemap(
            st.session_state.directories_df,
            path=['dominio', 'dir_1', 'dir_2', 'dir_3'],
            title=f'{domain} Categories Structure (date: {today})',
            height=750
        )

        st.session_state.treemap_fig.update_traces(
            texttemplate="<b>%{label}</b><br>Pages: %{value}<br>%{percentParent} of parent<br>%{percentRoot} of total",
            root_color="lightgrey"
        )

        st.session_state.analysis_done = True
        return True


# Interface utilisateur
st.title("📊 SEO Sitemap Analyzer")

# Entrée URL
col1, col2 = st.columns(2)
with col1:
    url = st.text_input("Entrez l'URL du site à analyser:")
with col2:
    custom_sitemap = st.text_input("URL du sitemap personnalisé (optionnel):")

# Options d'analyse
max_categories = st.number_input("Nombre max de catégories", -1, 100, -1)
show_single_items = st.checkbox("Afficher les catégories à 1 élément")

# Section des exclusions
st.subheader("Configuration des exclusions")
col1, col2, col3 = st.columns(3)

with col1:
    exclude_dir1 = st.text_input(
        "Exclusions niveau 1 (dir_1)",
        help="Catégories à exclure au niveau 1 (séparées par des virgules)"
    )

with col2:
    exclude_dir2 = st.text_input(
        "Exclusions niveau 2 (dir_2)",
        help="Catégories à exclure au niveau 2 (séparées par des virgules)"
    )

with col3:
    exclude_dir3 = st.text_input(
        "Exclusions niveau 3 (dir_3)",
        help="Catégories à exclure au niveau 3 (séparées par des virgules)"
    )

# Upload de fichiers
gsc_file = st.file_uploader("Importer données Google Search Console (CSV)", type=['csv'])

# Traitement des fichiers uploadés
if gsc_file:
    st.session_state.traffic_df = pd.read_csv(gsc_file)
    st.session_state.traffic_df.columns = ['url', 'clicks', 'impressions', 'ctr', 'position']

# Bouton d'analyse
if st.button("Analyser le site"):
    if url:
        exclusions = {
            'dir_1': clean_exclusions(exclude_dir1),
            'dir_2': clean_exclusions(exclude_dir2),
            'dir_3': clean_exclusions(exclude_dir3)
        }

        # Affichage des exclusions actives
        active_exclusions = {level: terms for level, terms in exclusions.items() if terms}
        if active_exclusions:
            st.info("Exclusions actives:")
            for level, terms in active_exclusions.items():
                st.write(f"- {level}: {', '.join(terms)}")

        analyze_website(url, custom_sitemap, max_categories, show_single_items, exclusions)
    else:
        st.error("Veuillez entrer une URL valide")

# Affichage des résultats
if st.session_state.analysis_done:
    # Treemap
    st.plotly_chart(st.session_state.treemap_fig, use_container_width=True)

    # Filtres et statistiques
    with st.container():
        # Sélection des catégories
        col1, col2, col3 = st.columns(3)

        with col1:
            categories = sorted(st.session_state.directories_df['dir_1'].unique())
            selected_category = st.selectbox("Sélectionner une catégorie", categories)

        with col2:
            subcategories = ['Toutes'] + sorted(
                st.session_state.directories_df[
                    st.session_state.directories_df['dir_1'] == selected_category
                    ]['dir_2'].unique().tolist()
            )
            selected_subcategory = st.selectbox("Sélectionner une sous-catégorie", subcategories)

        with col3:
            subsubcategories = ['Toutes']
            if selected_subcategory != 'Toutes':
                subsubcategories += sorted(
                    st.session_state.directories_df[
                        (st.session_state.directories_df['dir_1'] == selected_category) &
                        (st.session_state.directories_df['dir_2'] == selected_subcategory)
                        ]['dir_3'].unique().tolist()
                )
            selected_subsubcategory = st.selectbox("Sélectionner une sous-sous-catégorie", subsubcategories)

        # Statistiques
        stats = get_url_statistics(selected_category, selected_subcategory, selected_subsubcategory)

        st.markdown("### Statistiques des URLs")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("URLs Totales", stats['total'])

        with col2:
            label = f"URLs {stats['dir1'][0]}" if stats['dir1'][0] != '-' else "URLs Dir_1"
            value = stats['dir1'][1]
            st.metric(label, value)

        with col3:
            label = f"URLs {stats['dir2'][0]}" if stats['dir2'][0] != '-' else "URLs Dir_2"
            value = stats['dir2'][1]
            st.metric(label, value)

        with col4:
            label = f"URLs {stats['dir3'][0]}" if stats['dir3'][0] != '-' else "URLs Dir_3"
            value = stats['dir3'][1]
            st.metric(label, value)

        # Tableau des URLs
        if selected_category:
            filtered_df = filter_and_display_urls(selected_category, selected_subcategory, selected_subsubcategory)
            st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    st.sidebar.markdown("""
    ### À propos
    Cette application analyse la structure des URLs d'un site web à partir de son sitemap.

    #### Fonctionnalités :
    - Analyse de sitemap
    - Visualisation treemap
    - Filtrage par niveau
    - Exclusion par niveau
    - Intégration GSC
    
    #### Guide d'usage des filtres :
    
    **Nombre max de catégories :**  
    Limite le nombre de catégories dir_1 à afficher dans l'analyse.  
    Les catégories sont classées par ordre décroissant du nombre d'URLs.  
    `-1` = afficher toutes les catégories.
    
    **Configuration des exclusions :**  
    ⚠️ Important : Pour de meilleurs résultats, évitez d'utiliser des termes d'exclusion différents sur plusieurs niveaux de directory (dir_1, dir_2, dir_3).
    """)ggg