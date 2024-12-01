import streamlit as st
import advertools as adv
import pandas as pd
import plotly.express as px
from urllib.parse import urlparse
import datetime
import concurrent.futures
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration de la page Streamlit
st.set_page_config(layout="wide", page_title="SEO Sitemap Analyzer")

# Initialisation des variables de session
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


def process_semrush_files(files, markets):
    """Traite les fichiers SEMrush uploadés et les combine en un seul DataFrame."""
    logger.info("Début du traitement des fichiers SEMrush")
    dfs = []
    for i, (file, market) in enumerate(zip(files, markets)):
        if file is not None:
            try:
                logger.info(f"Traitement du fichier SEMrush {i + 1} pour le marché {market}")
                df = pd.read_csv(file, sep=';')
                df['market'] = market.lower()
                dfs.append(df)
                logger.info(f"Fichier SEMrush {i + 1} traité avec succès - {len(df)} lignes")
            except Exception as e:
                logger.error(f"Erreur lors de la lecture du fichier SEMrush {i + 1}: {e}")
                st.error(f"Erreur lors de la lecture du fichier SEMrush : {e}")

    if dfs:
        result_df = pd.concat(dfs, ignore_index=True)
        logger.info(f"Total des données SEMrush combinées: {len(result_df)} lignes")
        return result_df
    return pd.DataFrame()


def fetch_sitemap(url):
    """Récupère le sitemap d'une URL donnée."""
    try:
        logger.info(f"Récupération du sitemap: {url}")
        sitemap_df = adv.sitemap_to_df(url)
        logger.info(f"Sitemap récupéré avec succès - {len(sitemap_df)} URLs trouvées")
        return sitemap_df
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du sitemap {url}: {e}")
        st.error(f"Erreur lors de la récupération du sitemap {url}: {e}")
        return pd.DataFrame()


def get_sitemap_urls(url, custom_sitemap=''):
    """Récupère les URLs du sitemap, soit depuis robots.txt, soit depuis un sitemap personnalisé."""
    logger.info("Début de la récupération des URLs du sitemap")
    if custom_sitemap:
        logger.info(f"Utilisation du sitemap personnalisé: {custom_sitemap}")
        return [custom_sitemap]
    try:
        robots_url = f"{url.rstrip('/')}/robots.txt"
        logger.info(f"Tentative de lecture du robots.txt: {robots_url}")
        robots_df = adv.robotstxt_to_df(robots_url)
        sitemap_urls = robots_df[robots_df['directive'].str.contains('Sitemap', case=False)]['content'].tolist()
        if not sitemap_urls:
            default_sitemap = f"{url.rstrip('/')}/sitemap.xml"
            logger.info(f"Aucun sitemap trouvé dans robots.txt, utilisation par défaut: {default_sitemap}")
            sitemap_urls.append(default_sitemap)
        else:
            logger.info(f"Sitemaps trouvés dans robots.txt: {sitemap_urls}")
        return sitemap_urls
    except Exception as e:
        logger.warning(f"Impossible de lire robots.txt: {e}")
        default_sitemap = f"{url.rstrip('/')}/sitemap.xml"
        logger.info(f"Utilisation du sitemap par défaut: {default_sitemap}")
        st.warning(f"Impossible de lire robots.txt, utilisation du sitemap par défaut: {e}")
        return [default_sitemap]


def get_url_statistics(selected_category='Toutes', selected_subcategory='Toutes', selected_subsubcategory='Toutes'):
    """Calcule les statistiques des URLs pour chaque niveau de catégorie."""
    logger.info(
        f"Calcul des statistiques - Catégorie: {selected_category}, Sous-catégorie: {selected_subcategory}, Sous-sous-catégorie: {selected_subsubcategory}")
    total_urls = len(st.session_state.directories_df)

    if selected_category == 'Toutes':
        logger.info(f"Statistiques globales - Total URLs: {total_urls}")
        return {
            'total': total_urls,
            'dir1': ('Toutes', total_urls),
            'dir2': ('-', '-'),
            'dir3': ('-', '-')
        }

    dir1_df = st.session_state.directories_df[st.session_state.directories_df['dir_1'] == selected_category]
    dir1_count = len(dir1_df)
    logger.info(f"URLs pour la catégorie {selected_category}: {dir1_count}")

    if selected_subcategory == 'Toutes':
        return {
            'total': total_urls,
            'dir1': (selected_category, dir1_count),
            'dir2': ('-', '-'),
            'dir3': ('-', '-')
        }

    dir2_df = dir1_df[dir1_df['dir_2'] == selected_subcategory]
    dir2_count = len(dir2_df)
    logger.info(f"URLs pour la sous-catégorie {selected_subcategory}: {dir2_count}")

    if selected_subsubcategory == 'Toutes':
        return {
            'total': total_urls,
            'dir1': (selected_category, dir1_count),
            'dir2': (selected_subcategory, dir2_count),
            'dir3': ('-', '-')
        }

    dir3_df = dir2_df[dir2_df['dir_3'] == selected_subsubcategory]
    dir3_count = len(dir3_df)
    logger.info(f"URLs pour la sous-sous-catégorie {selected_subsubcategory}: {dir3_count}")

    return {
        'total': total_urls,
        'dir1': (selected_category, dir1_count),
        'dir2': (selected_subcategory, dir2_count),
        'dir3': (selected_subsubcategory, dir3_count)
    }


def filter_and_display_urls(selected_category, selected_subcategory='Toutes', selected_subsubcategory='Toutes'):
    """Filtre les URLs en fonction des catégories sélectionnées."""
    logger.info(
        f"Application des filtres - Catégorie: {selected_category}, Sous-catégorie: {selected_subcategory}, Sous-sous-catégorie: {selected_subsubcategory}")
    if selected_category == 'Toutes':
        logger.info("Retour de toutes les URLs sans filtre")
        return st.session_state.directories_df

    filtered_df = st.session_state.directories_df[st.session_state.directories_df['dir_1'] == selected_category]
    logger.info(f"URLs après filtre dir_1: {len(filtered_df)}")

    if selected_subcategory != 'Toutes':
        filtered_df = filtered_df[filtered_df['dir_2'] == selected_subcategory]
        logger.info(f"URLs après filtre dir_2: {len(filtered_df)}")

    if selected_subsubcategory != 'Toutes':
        filtered_df = filtered_df[filtered_df['dir_3'] == selected_subsubcategory]
        logger.info(f"URLs après filtre dir_3: {len(filtered_df)}")

    return filtered_df


def clean_exclusions(exclusion_string):
    """Nettoie et prépare la liste des exclusions."""
    logger.info(f"Nettoyage des exclusions: {exclusion_string}")
    if not exclusion_string:
        return []
    cleaned = [item.strip() for item in exclusion_string.split(',') if item.strip()]
    logger.info(f"Exclusions nettoyées: {cleaned}")
    return cleaned


def analyze_website(url, custom_sitemap='', max_categories=-1, show_single_items=False, exclusions=None):
    """Analyse un site web à partir de son sitemap avec gestion des exclusions par niveau."""
    logger.info(f"Début de l'analyse du site: {url}")
    if exclusions is None:
        exclusions = {'dir_1': [], 'dir_2': [], 'dir_3': []}

    domain = urlparse(url).netloc.replace('www.', '').split(".")[0]
    logger.info(f"Domaine extrait: {domain}")

    with st.spinner('Récupération des sitemaps...'):
        sitemap_urls = get_sitemap_urls(url, custom_sitemap)
        logger.info(f"Sitemaps à analyser: {sitemap_urls}")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            sitemaps = list(executor.map(fetch_sitemap, sitemap_urls))

        urls_df = pd.concat(sitemaps, ignore_index=True)
        logger.info(f"Total des URLs trouvées: {len(urls_df)}")

    if urls_df.empty:
        logger.error("Aucune URL trouvée dans le sitemap")
        st.error("Aucune URL trouvée dans le sitemap")
        return None

    with st.spinner('Analyse des URLs...'):
        logger.info("Début de l'analyse détaillée des URLs")
        st.session_state.url_df = adv.url_to_df(urls_df['loc'].dropna().tolist())
        st.session_state.url_df['dominio'] = domain

        # Préparation des données pour les trois niveaux
        for dir_col in ['dir_1', 'dir_2', 'dir_3']:
            if dir_col not in st.session_state.url_df.columns:
                st.session_state.url_df[dir_col] = ""
            st.session_state.url_df[dir_col] = st.session_state.url_df[dir_col].replace('', 'no directory').astype(str)
            logger.info(f"Traitement du niveau {dir_col} terminé")

        # Application des exclusions niveau par niveau
        exclude_mask = pd.Series(False, index=st.session_state.url_df.index)
        for dir_level, exclusion_list in exclusions.items():
            if exclusion_list:
                logger.info(f"Application des exclusions pour {dir_level}: {exclusion_list}")
                exclude_mask = exclude_mask | st.session_state.url_df[dir_level].isin(exclusion_list)

        if exclude_mask.any():
            excluded_count = exclude_mask.sum()
            logger.info(f"Nombre d'URLs exclues: {excluded_count}")
            st.session_state.url_df = st.session_state.url_df[~exclude_mask]

        # Gestion des catégories
        top_categories = st.session_state.url_df['dir_1'].value_counts()
        logger.info(f"Catégories trouvées: {len(top_categories)}")

        if not show_single_items:
            small_categories = top_categories[top_categories <= 1].index
            logger.info(f"Catégories avec une seule URL: {len(small_categories)}")
            st.session_state.url_df.loc[
                st.session_state.url_df['dir_1'].isin(small_categories), 'dir_1'] = 'no directory'

        top_categories = st.session_state.url_df['dir_1'].value_counts()

        if max_categories > 0:
            logger.info(f"Limitation aux {max_categories} premières catégories")
            top_categories = top_categories.head(max_categories)

        # Création du DataFrame final
        st.session_state.directories_df = st.session_state.url_df[
            st.session_state.url_df['dir_1'].isin(top_categories.index)
        ][['dominio', 'dir_1', 'dir_2', 'dir_3', 'url']]
        logger.info(f"DataFrame final créé avec {len(st.session_state.directories_df)} URLs")

        # Création du treemap
        today = datetime.datetime.utcnow().strftime('%B %d, %Y')
        logger.info("Création du treemap")
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
        logger.info("Analyse terminée avec succès")
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

# Section SEMrush
st.header("Ajout de données SEM RUSH")
markets = ['fr', 'it', 'es', 'uk', 'us', 'pt', 'nl', 'de', 'ca', 'br', 'be']
semrush_files = []
selected_markets = []

for i in range(st.session_state.num_semrush_files):
    col1, col2 = st.columns([3, 1])
    with col1:
        file = st.file_uploader(f"Fichier SEMrush #{i+1}", type=['csv'], key=f"semrush_file_{i}")
        semrush_files.append(file)
    with col2:
        market = st.selectbox("Marché", markets, key=f"market_{i}")
        selected_markets.append(market)

if st.session_state.num_semrush_files < 6:
    # Ajout d'une clé unique pour le bouton
    if st.button("+ Ajouter un fichier", key="add_semrush_file_btn"):
        st.session_state.num_semrush_files += 1
        st.rerun()

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

    # Bouton d'analyse
    if st.button("Analyser le site"):
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
                st.info("Exclusions actives:")
                for level, terms in active_exclusions.items():
                    st.write(f"- {level}: {', '.join(terms)}")

            analyze_website(url, custom_sitemap, max_categories, show_single_items, exclusions)
        else:
            logger.error("URL non fournie")
            st.error("Veuillez entrer une URL valide")

    # Affichage des résultats
    if st.session_state.analysis_done:
        # Treemap
        st.plotly_chart(st.session_state.treemap_fig, use_container_width=True)

        # Filtres dans un conteneur horizontal
        st.write("### Filtres de navigation")
        cols = st.columns(3)
        with cols[0]:
            categories = ['Toutes'] + sorted(st.session_state.directories_df['dir_1'].unique())
            selected_category = st.selectbox("Sélectionner une catégorie", categories)

        with cols[1]:
            subcategories = ['Toutes']
            if selected_category != 'Toutes':
                subcategories += sorted(
                    st.session_state.directories_df[
                        st.session_state.directories_df['dir_1'] == selected_category
                        ]['dir_2'].unique().tolist()
                )
            selected_subcategory = st.selectbox("Sélectionner une sous-catégorie", subcategories)

        with cols[2]:
            subsubcategories = ['Toutes']
            if selected_subcategory != 'Toutes' and selected_category != 'Toutes':
                subsubcategories += sorted(
                    st.session_state.directories_df[
                        (st.session_state.directories_df['dir_1'] == selected_category) &
                        (st.session_state.directories_df['dir_2'] == selected_subcategory)
                        ]['dir_3'].unique().tolist()
                )
            selected_subsubcategory = st.selectbox("Sélectionner une sous-sous-catégorie", subsubcategories)

        # Statistiques en dehors des colonnes
        st.markdown("### Statistiques des URLs")
        # Création d'un conteneur pour les métriques
        with st.container():
            # Utilisation d'une grille de colonnes égales
            metrics_cols = st.columns([1, 1, 1, 1])
            stats = get_url_statistics(selected_category, selected_subcategory, selected_subsubcategory)

            # Application des métriques de manière centrée
            metrics_cols[0].metric(
                label="URLs Totales",
                value=stats['total'],
                help="Nombre total d'URLs dans le sitemap"
            )

            metrics_cols[1].metric(
                label=f"URLs {stats['dir1'][0]}" if stats['dir1'][0] != '-' else "URLs Dir_1",
                value=stats['dir1'][1],
                help="Nombre d'URLs dans la catégorie sélectionnée"
            )

            metrics_cols[2].metric(
                label=f"URLs {stats['dir2'][0]}" if stats['dir2'][0] != '-' else "URLs Dir_2",
                value=stats['dir2'][1],
                help="Nombre d'URLs dans la sous-catégorie sélectionnée"
            )

            metrics_cols[3].metric(
                label=f"URLs {stats['dir3'][0]}" if stats['dir3'][0] != '-' else "URLs Dir_3",
                value=stats['dir3'][1],
                help="Nombre d'URLs dans la sous-sous-catégorie sélectionnée"
            )

        # Tableau en pleine largeur
        filtered_df = filter_and_display_urls(selected_category, selected_subcategory, selected_subsubcategory)
        st.dataframe(
            filtered_df,
            use_container_width=True,
            column_config={
                "dominio": st.column_config.TextColumn("Domaine", width=150),
                "dir_1": st.column_config.TextColumn("Dir_1", width=100),
                "dir_2": st.column_config.TextColumn("Dir_2", width=100),
                "dir_3": st.column_config.TextColumn("Dir_3", width=100),
                "url": st.column_config.TextColumn("URL", width=None),
            }
        )

        # Données SEMrush en pleine largeur également
        if not st.session_state.semrush_data.empty:
            st.markdown("### Statistiques SEM Rush")
            st.dataframe(
                st.session_state.semrush_data,
                use_container_width=True,
                column_config={
                    "market": st.column_config.TextColumn("Marché", width=80),
                    "Keyword": st.column_config.TextColumn("Mot-clé", width=200),
                    "Position": st.column_config.NumberColumn("Position", width=80),
                    "Search Volume": st.column_config.NumberColumn("Volume", width=100),
                    "URL": st.column_config.TextColumn("URL", width=None),
                    "Traffic": st.column_config.NumberColumn("Trafic", width=100),
                    "Traffic (%)": st.column_config.NumberColumn("Trafic %", width=100),
                    "Traffic Cost": st.column_config.NumberColumn("Coût trafic", width=120),
                    "Keyword Difficulty": st.column_config.NumberColumn("Difficulté", width=100)
                }
            )

    if __name__ == "__main__":
        st.sidebar.markdown("""
        ### À propos
        Cette application analyse la structure des URLs d'un site web à partir de son sitemap.

        #### Fonctionnalités :
        - Analyse de sitemap
        - Visualisation treemap
        - Filtrage par niveau
        - Exclusion par niveau
        - Analyse SEMrush multi-marchés

        #### Guide d'usage des filtres :

        **Nombre max de catégories :**  
        Limite le nombre de catégories dir_1 à afficher dans l'analyse.  
        Les catégories sont classées par ordre décroissant du nombre d'URLs.  
        `-1` = afficher toutes les catégories.

        **Configuration des exclusions :**  
        ⚠️ Important : Pour de meilleurs résultats, évitez d'utiliser des termes d'exclusion différents sur plusieurs niveaux de directory (dir_1, dir_2, dir_3).
        """)