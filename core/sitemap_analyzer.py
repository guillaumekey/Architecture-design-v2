"""
Analyseur de sitemaps - Logique de récupération et parsing des sitemaps
"""

import advertools as adv
import pandas as pd
import requests
import logging
import concurrent.futures
import streamlit as st
from urllib.parse import urlparse
from config.settings import DEFAULT_HEADERS
from config.translations import get_text
from visualizations.treemap import create_treemap

logger = logging.getLogger(__name__)

def fetch_sitemap(url):
    """Récupère et parse le sitemap d'une URL donnée."""
    try:
        logger.info(f"Tentative de récupération du sitemap: {url}")

        response = requests.get(url, timeout=30, headers=DEFAULT_HEADERS)

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
    """
    logger.info("Début de la récupération des URLs du sitemap.")

    # Si des sitemaps personnalisés sont fournis, on les utilise directement
    if custom_sitemaps and any(custom_sitemaps):
        logger.info(f"Utilisation des sitemaps personnalisés : {custom_sitemaps}")
        return [sitemap for sitemap in custom_sitemaps if sitemap], get_text('sitemap_manual', st.session_state.selected_language)

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
            return sitemap_urls, get_text('sitemap_robots', st.session_state.selected_language)
        else:
            logger.warning("Aucun sitemap trouvé dans le robots.txt, fallback vers /sitemap.xml")
            fallback_sitemap = [f"{url.rstrip('/')}/sitemap.xml"]
            return fallback_sitemap, get_text('sitemap_fallback', st.session_state.selected_language)

    except Exception as e:
        # En cas d'erreur avec le robots.txt, fallback vers le sitemap par défaut
        logger.warning(f"Erreur lors de la lecture du robots.txt : {e}. Utilisation du fallback.")
        default_sitemap = [f"{url.rstrip('/')}/sitemap.xml"]
        return default_sitemap, get_text('sitemap_error', st.session_state.selected_language)

def fetch_and_parse_sitemaps(sitemap_urls):
    """Récupère et parse tous les sitemaps."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        sitemaps = list(executor.map(fetch_sitemap, sitemap_urls))

    urls_df = pd.concat(sitemaps, ignore_index=True)
    logger.info(f"Total des URLs trouvées: {len(urls_df)}")
    return urls_df

def analyze_website(url, custom_sitemaps=None, max_categories=-1, show_single_items=False, exclusions=None):
    """Point d'entrée principal pour l'analyse d'un site web."""
    from core.url_processor import process_urls

    logger.info(f"Début de l'analyse du site: {url}")
    if exclusions is None:
        exclusions = {'dir_1': [], 'dir_2': [], 'dir_3': []}

    # Récupération des sitemaps
    with st.spinner(get_text('analysis_in_progress', st.session_state.selected_language)):
        sitemap_urls, sitemap_message = get_sitemap_urls(url, custom_sitemaps)
        logger.info(f"Sitemaps à analyser : {sitemap_urls}")
        st.info(f"🔍 {sitemap_message}")

        # Récupération des URLs
        urls_df = fetch_and_parse_sitemaps(sitemap_urls)

    if urls_df.empty:
        logger.error("Aucune URL trouvée dans le sitemap")
        st.error("Aucune URL trouvée dans le sitemap")
        return None

    # Traitement des URLs
    with st.spinner(get_text('analysis_in_progress', st.session_state.selected_language)):
        success = process_urls(url, urls_df, max_categories, show_single_items, exclusions)

        if success:
            # Création du treemap
            import datetime
            import plotly.express as px

            domain = urlparse(url).netloc.replace('www.', '').split(".")[0]
            today = datetime.datetime.now(datetime.timezone.utc).strftime('%B %d, %Y')
            logger.info("Création du treemap")

            lang = st.session_state.get('selected_language', 'fr')

            st.session_state.treemap_fig = px.treemap(
                st.session_state.directories_df,
                path=['dominio', 'dir_1', 'dir_2', 'dir_3'],
                title=f'{domain} Categories Structure (date: {today})',
                height=750
            )

            # CORRECTION: Template et hover traduits
            st.session_state.treemap_fig.update_traces(
                texttemplate=f"<b>%{{label}}</b><br>{get_text('pages', lang)}: %{{value}}<br>%{{percentParent}} {get_text('of_parent', lang)}<br>%{{percentRoot}} {get_text('of_total', lang)}",
                root_color="lightgrey",
                hovertemplate=(
                    f"<b>%{{label}}</b><br>"
                    f"{get_text('label', lang)}: %{{label}}<br>"
                    f"{get_text('count_label', lang)}: %{{value}}<br>"
                    f"{get_text('parent_label', lang)}: %{{parent}}<br>"
                    f"{get_text('id_label', lang)}: %{{id}}"
                    "<extra></extra>"
                )
            )

            st.session_state.analysis_done = True
            logger.info("Analyse terminée avec succès")
            return True

    return False