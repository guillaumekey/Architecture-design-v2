import streamlit as st
import advertools as adv
import pandas as pd
import plotly.express as px
from urllib.parse import urlparse
import datetime
import concurrent.futures
import logging
import requests
import time
import cloudscraper

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
if 'num_custom_sitemaps' not in st.session_state:
    st.session_state.num_custom_sitemaps = 1


def prepare_semrush_data(df):
    """Agrège les données SEMrush par URL, marché et type de position."""
    if df.empty:
        return pd.DataFrame()

    logger.info("Préparation des données SEMrush")

    # Grouper par URL, marché et type de position
    grouped = df.groupby(['URL', 'market', 'Position Type']).agg({
        'Traffic': 'sum',
        'Search Volume': 'sum',
        'Keyword': 'count'  # Compte le nombre de mots clés (lignes) par URL
    }).reset_index()

    # Renommer la colonne pour plus de clarté
    grouped = grouped.rename(columns={'Keyword': 'Number of Keywords'})

    logger.info(f"Données préparées : {len(grouped)} lignes")
    return grouped


def create_main_dataframe(sitemap_df, semrush_df):
    """Crée le dataframe principal avec jointure sitemap et SEMrush."""
    logger.info("Création du main dataframe")

    # Préparation des données SEMrush
    semrush_prepared = prepare_semrush_data(semrush_df)

    if semrush_prepared.empty:
        logger.warning("Pas de données SEMrush disponibles")
        return pd.DataFrame(), pd.DataFrame()

    # Jointure avec les données du sitemap
    main_df = sitemap_df.merge(
        semrush_prepared,
        left_on='url',
        right_on='URL',
        how='right'  # Pour garder toutes les URLs de SEMrush
    )

    # Identification des URLs non présentes dans le sitemap
    urls_not_in_sitemap = main_df[main_df['dominio'].isna()].copy()
    urls_in_sitemap = main_df[main_df['dominio'].notna()].copy()

    logger.info(f"URLs trouvées dans SEMrush mais pas dans le sitemap : {len(urls_not_in_sitemap)}")

    return urls_in_sitemap, urls_not_in_sitemap


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


def create_directory_performance_summary(sitemap_df, semrush_df, dir_1_filter=None, dir_2_filter=None):
    """Crée un résumé des performances par niveau de directory."""
    logger.info("Création du résumé des performances par directory")

    summary_dfs = []

    # Analyse niveau 1 (toujours affiché)
    if dir_1_filter is None:
        # Compter d'abord le nombre total d'URLs depuis le sitemap
        sitemap_counts = sitemap_df.groupby('dir_1')['url'].count().reset_index()

        # Calculer les métriques SEMrush par URL unique
        semrush_metrics = semrush_df.groupby(['dir_1', 'url']).agg({
            'Traffic': 'sum',
            'Number of Keywords': 'sum',
            'Search Volume': 'sum'
        }).reset_index().groupby('dir_1').sum().drop('url', axis=1).reset_index()

        # Joindre les deux ensembles de données
        dir_1_summary = sitemap_counts.merge(
            semrush_metrics,
            on='dir_1',
            how='left'
        ).fillna(0)

        dir_1_summary['Niveau'] = 'Dir_1'
        dir_1_summary = dir_1_summary.rename(columns={
            'dir_1': 'Directory',
            'url': 'Nombre URLs',
            'Traffic': 'Traffic Total',
            'Number of Keywords': 'Total Mots-clés',
            'Search Volume': 'Volume Total'
        })
        summary_dfs.append(dir_1_summary)

    # Analyse niveau 2 (si dir_1 est filtré et dir_2 n'est pas filtré)
    if dir_1_filter is not None and dir_2_filter is None:
        filtered_sitemap = sitemap_df[sitemap_df['dir_1'] == dir_1_filter]
        filtered_semrush = semrush_df[semrush_df['dir_1'] == dir_1_filter]

        sitemap_counts = filtered_sitemap.groupby('dir_2')['url'].count().reset_index()

        semrush_metrics = filtered_semrush.groupby(['dir_2', 'url']).agg({
            'Traffic': 'sum',
            'Number of Keywords': 'sum',
            'Search Volume': 'sum'
        }).reset_index().groupby('dir_2').sum().drop('url', axis=1).reset_index()

        dir_2_summary = sitemap_counts.merge(
            semrush_metrics,
            on='dir_2',
            how='left'
        ).fillna(0)

        dir_2_summary['Niveau'] = 'Dir_2'
        dir_2_summary = dir_2_summary.rename(columns={
            'dir_2': 'Directory',
            'url': 'Nombre URLs',
            'Traffic': 'Traffic Total',
            'Number of Keywords': 'Total Mots-clés',
            'Search Volume': 'Volume Total'
        })
        summary_dfs.append(dir_2_summary)

    # Analyse niveau 3 (si dir_1 et dir_2 sont filtrés)
    if dir_1_filter is not None and dir_2_filter is not None:
        filtered_sitemap = sitemap_df[
            (sitemap_df['dir_1'] == dir_1_filter) &
            (sitemap_df['dir_2'] == dir_2_filter)
        ]
        filtered_semrush = semrush_df[
            (semrush_df['dir_1'] == dir_1_filter) &
            (semrush_df['dir_2'] == dir_2_filter)
        ]

        sitemap_counts = filtered_sitemap.groupby('dir_3')['url'].count().reset_index()

        semrush_metrics = filtered_semrush.groupby(['dir_3', 'url']).agg({
            'Traffic': 'sum',
            'Number of Keywords': 'sum',
            'Search Volume': 'sum'
        }).reset_index().groupby('dir_3').sum().drop('url', axis=1).reset_index()

        dir_3_summary = sitemap_counts.merge(
            semrush_metrics,
            on='dir_3',
            how='left'
        ).fillna(0)

        dir_3_summary['Niveau'] = 'Dir_3'
        dir_3_summary = dir_3_summary.rename(columns={
            'dir_3': 'Directory',
            'url': 'Nombre URLs',
            'Traffic': 'Traffic Total',
            'Number of Keywords': 'Total Mots-clés',
            'Search Volume': 'Volume Total'
        })
        summary_dfs.append(dir_3_summary)

    result = pd.concat(summary_dfs, ignore_index=True)
    return result.sort_values(by='Traffic Total', ascending=False).reset_index(drop=True)

def fetch_sitemap(url):
    """Récupère et parse le sitemap d'une URL donnée."""
    try:
        logger.info(f"Tentative de récupération du sitemap: {url}")

        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        })

        if response.status_code != 200:
            logger.error(f"Impossible de récupérer le sitemap (status code: {response.status_code})")
            return pd.DataFrame()

        content_type = response.headers.get('Content-Type', '').lower()
        if 'xml' not in content_type:
            logger.warning(f"Le contenu récupéré n'est pas du XML (type: {content_type})")
            return pd.DataFrame()

        # Utiliser advertools pour convertir en DataFrame
        try:
            sitemap_df = adv.sitemap_to_df(url)
            if sitemap_df.empty:
                logger.warning("Aucune URL trouvée dans le sitemap fourni.")
            else:
                logger.info(f"Sitemap récupéré avec succès - {len(sitemap_df)} URLs trouvées.")
            return sitemap_df
        except Exception as e:
            logger.error(f"Erreur lors de la conversion du sitemap en DataFrame : {e}")
            return pd.DataFrame()

    except Exception as e:
        logger.error(f"Erreur lors de la récupération du sitemap {url} : {e}")
        return pd.DataFrame()


def get_sitemap_urls(url, custom_sitemaps=None):
    """
    Récupère les URLs du sitemap, soit depuis robots.txt, soit depuis les sitemaps personnalisés.

    Args:
        url (str): L'URL de base du site à analyser.
        custom_sitemaps (list): Liste d'URLs de sitemaps fournis manuellement.

    Returns:
        tuple: Liste des URLs des sitemaps et un message sur l'origine des sitemaps.
    """
    logger.info("Début de la récupération des URLs du sitemap.")

    # Si des sitemaps personnalisés sont fournis, on les utilise directement
    if custom_sitemaps and any(custom_sitemaps):
        logger.info(f"Utilisation des sitemaps personnalisés : {custom_sitemaps}")
        return [sitemap for sitemap in custom_sitemaps if sitemap], "Sitemap fourni manuellement utilisé."

    try:
        # Construction de l'URL du robots.txt
        robots_url = f"{url.rstrip('/')}/robots.txt"
        logger.info(f"Tentative de lecture du robots.txt à : {robots_url}")

        # Utilisation d'advertools pour analyser le fichier robots.txt
        robots_df = adv.robotstxt_to_df(robots_url)

        # Filtrage pour récupérer les directives de type Sitemap
        sitemap_urls = robots_df[robots_df['directive'].str.contains('sitemap', case=False)]['content'].tolist()

        if sitemap_urls:
            logger.info(f"Sitemaps trouvés dans robots.txt : {sitemap_urls}")
            return sitemap_urls, "Sitemaps récupérés depuis robots.txt."
        else:
            logger.warning("Aucun sitemap trouvé dans le robots.txt, fallback vers /sitemap.xml")
            fallback_sitemap = [f"{url.rstrip('/')}/sitemap.xml"]
            return fallback_sitemap, "Aucun sitemap trouvé dans robots.txt. Utilisation du fallback /sitemap.xml."

    except Exception as e:
        # En cas d'erreur avec le robots.txt, fallback vers le sitemap par défaut
        logger.warning(f"Erreur lors de la lecture du robots.txt : {e}. Utilisation du fallback.")
        default_sitemap = [f"{url.rstrip('/')}/sitemap.xml"]
        return default_sitemap, "Erreur lors de la lecture du robots.txt. Utilisation du fallback /sitemap.xml."



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

def analyze_website(url, custom_sitemaps=None, max_categories=-1, show_single_items=False, exclusions=None):
    """Analyse un site web à partir de son sitemap avec gestion des exclusions par niveau."""
    logger.info(f"Début de l'analyse du site: {url}")
    if exclusions is None:
        exclusions = {'dir_1': [], 'dir_2': [], 'dir_3': []}

    domain = urlparse(url).netloc.replace('www.', '').split(".")[0]
    logger.info(f"Domaine extrait: {domain}")

    with st.spinner('Récupération des sitemaps...'):
        sitemap_urls, sitemap_message = get_sitemap_urls(url, custom_sitemaps)
        logger.info(f"Sitemaps à analyser : {sitemap_urls}")
        st.info(f"🔍 {sitemap_message}")  # Affichage du message

        # Headers avec Googlebot user-agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

        # Vérification des sitemaps avant traitement
        for sitemap_url in sitemap_urls:
            try:
                response = requests.get(sitemap_url, headers=headers)
                if response.status_code != 200:
                    st.error(f"Impossible d'accéder au sitemap {sitemap_url} - Status code: {response.status_code}")
                    continue

                content_type = response.headers.get('content-type', '')
                if 'xml' not in content_type.lower():
                    st.warning(
                        f"Le sitemap {sitemap_url} n'est peut-être pas au format XML (Content-Type: {content_type})")

                logger.info(f"Contenu du sitemap {sitemap_url}: {response.text[:200]}...")
            except Exception as e:
                st.error(f"Erreur lors de l'accès au sitemap {sitemap_url}: {e}")
                continue

        with concurrent.futures.ThreadPoolExecutor() as executor:
            sitemaps = list(executor.map(fetch_sitemap, sitemap_urls))

        urls_df = pd.concat(sitemaps, ignore_index=True)
        logger.info(f"Total des URLs trouvées: {len(urls_df)}")

    if urls_df.empty:
        logger.error("Aucune URL trouvée dans le sitemap")
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

# Section des sitemaps personnalisés
st.subheader("Sitemaps personnalisés (optionnel)")

custom_sitemaps = []
for i in range(st.session_state.num_custom_sitemaps):
    custom_sitemap = st.text_input(f"URL du sitemap #{i + 1}", key=f"custom_sitemap_{i}")
    if custom_sitemap:
        custom_sitemaps.append(custom_sitemap)

if st.session_state.num_custom_sitemaps < 5:  # Limite à 5 sitemaps max
    if st.button("+ Ajouter un sitemap"):
        st.session_state.num_custom_sitemaps += 1
        st.rerun()

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
        file = st.file_uploader(f"Fichier SEMrush #{i + 1}", type=['csv'], key=f"semrush_file_{i}")
        semrush_files.append(file)
    with col2:
        market = st.selectbox("Marché", markets, key=f"market_{i}")
        selected_markets.append(market)

if st.session_state.num_semrush_files < 6:
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

        analyze_website(url, custom_sitemaps, max_categories, show_single_items, exclusions)
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
    st.dataframe(st.session_state.semrush_data, use_container_width=True)

    # Création et affichage du main dataframe
    st.markdown("### Statistiques URLs SEM Rush")
    urls_in_sitemap, urls_not_in_sitemap = create_main_dataframe(
        st.session_state.directories_df,
        st.session_state.semrush_data
    )

    if not urls_in_sitemap.empty:
        st.dataframe(
            urls_in_sitemap[[
                'url', 'dir_1', 'dir_2', 'dir_3', 'Traffic',
                'Number of Keywords', 'market', 'Search Volume',
                'Position Type'
            ]],
            use_container_width=True
        )

    # Affichage des URLs non présentes dans le sitemap
    if not urls_not_in_sitemap.empty:
        st.markdown("### URLs présentes dans SEMrush mais absentes du sitemap")
        st.dataframe(
            urls_not_in_sitemap[[
                'URL', 'Traffic', 'Number of Keywords',
                'Search Volume', 'Position Type', 'market'
            ]],
            use_container_width=True
        )

    # Résumé des performances par niveau de directory
    st.markdown("### Résultats par niveau de page")

    # Filtres pour les niveaux de directory
    col1, col2 = st.columns(2)
    with col1:
        dir_1_options = ['Toutes'] + sorted(urls_in_sitemap['dir_1'].unique().tolist())
        selected_dir_1 = st.selectbox("Filtrer par Dir_1", dir_1_options, key='perf_dir_1')

    with col2:
        dir_2_options = ['Toutes']
        if selected_dir_1 != 'Toutes':
            dir_2_options += sorted(
                urls_in_sitemap[urls_in_sitemap['dir_1'] == selected_dir_1]['dir_2'].unique().tolist()
            )
        selected_dir_2 = st.selectbox("Filtrer par Dir_2", dir_2_options, key='perf_dir_2')

    # Création et affichage du tableau de résumé
    dir_1_filter = selected_dir_1 if selected_dir_1 != 'Toutes' else None
    dir_2_filter = selected_dir_2 if selected_dir_2 != 'Toutes' else None

    performance_summary = create_directory_performance_summary(
        st.session_state.directories_df,  # Données du sitemap
        urls_in_sitemap,  # Données SEMrush
        dir_1_filter,
        dir_2_filter
    )
    # Affichage du tableau principal
    st.dataframe(
        performance_summary,
        use_container_width=True,
        column_config={
            "Directory": st.column_config.TextColumn("Directory", width=150),
            "Niveau": st.column_config.TextColumn("Niveau", width=100),
            "Nombre URLs": st.column_config.NumberColumn("Nombre URLs", width=120),
            "Traffic Total": st.column_config.NumberColumn("Traffic Total", width=120),
            "Total Mots-clés": st.column_config.NumberColumn("Total Mots-clés", width=120),
            "Volume Total": st.column_config.NumberColumn("Volume Total", width=120)
        }
    )

    # Calcul et affichage des totaux
    cols = st.columns(4)
    cols[0].metric(
        label="Total nombre d'URLs",
        value=f"{performance_summary['Nombre URLs'].sum():,}"
    )
    cols[1].metric(
        label="Total traffic",
        value=f"{performance_summary['Traffic Total'].sum():,}"
    )
    cols[2].metric(
        label="Total mots clés",
        value=f"{performance_summary['Total Mots-clés'].sum():,}"
    )
    cols[3].metric(
        label="Total volume",
        value=f"{performance_summary['Volume Total'].sum():,}"
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