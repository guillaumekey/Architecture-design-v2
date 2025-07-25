"""
Processeur d'URLs - Traitement et catégorisation des URLs
"""

import advertools as adv
import pandas as pd
import logging
import streamlit as st
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def prepare_url_directories(url_df, domain):
    """Prépare les colonnes de répertoires pour les URLs."""
    url_df['dominio'] = domain

    # Préparation des données pour les trois niveaux
    for dir_col in ['dir_1', 'dir_2', 'dir_3']:
        if dir_col not in url_df.columns:
            url_df[dir_col] = ""
        url_df[dir_col] = url_df[dir_col].replace('', 'no directory').astype(str)
        logger.info(f"Traitement du niveau {dir_col} terminé")

    return url_df


def apply_exclusions(url_df, exclusions):
    """Applique les exclusions niveau par niveau."""
    exclude_mask = pd.Series(False, index=url_df.index)

    for dir_level, exclusion_list in exclusions.items():
        if exclusion_list:
            logger.info(f"Application des exclusions pour {dir_level}: {exclusion_list}")
            exclude_mask = exclude_mask | url_df[dir_level].isin(exclusion_list)

    if exclude_mask.any():
        excluded_count = exclude_mask.sum()
        logger.info(f"Nombre d'URLs exclues: {excluded_count}")
        url_df = url_df[~exclude_mask]

    return url_df


def filter_categories(url_df, max_categories, show_single_items):
    """Filtre et limite les catégories selon les paramètres."""
    # Gestion des catégories
    top_categories = url_df['dir_1'].value_counts()
    logger.info(f"Catégories trouvées: {len(top_categories)}")

    if not show_single_items:
        small_categories = top_categories[top_categories <= 1].index
        logger.info(f"Catégories avec une seule URL: {len(small_categories)}")
        url_df.loc[url_df['dir_1'].isin(small_categories), 'dir_1'] = 'no directory'

    top_categories = url_df['dir_1'].value_counts()

    if max_categories > 0:
        logger.info(f"Limitation aux {max_categories} premières catégories")
        top_categories = top_categories.head(max_categories)

    return url_df, top_categories


def create_final_dataframes(url_df, top_categories):
    """Crée les DataFrames finaux pour l'affichage."""
    # Création du DataFrame final
    directories_df = url_df[url_df['dir_1'].isin(top_categories.index)][['dominio', 'dir_1', 'dir_2', 'dir_3', 'url']]

    return url_df, directories_df


def process_urls(url, urls_df, max_categories, show_single_items, exclusions):
    """Traite toutes les URLs récupérées depuis les sitemaps."""
    domain = urlparse(url).netloc.replace('www.', '').split(".")[0]
    logger.info(f"Domaine extrait: {domain}")

    # Conversion des URLs avec advertools
    url_df = adv.url_to_df(urls_df['loc'].dropna().tolist())

    # Préparation des répertoires
    url_df = prepare_url_directories(url_df, domain)

    # Application des exclusions
    url_df = apply_exclusions(url_df, exclusions)

    # Filtrage des catégories
    url_df, top_categories = filter_categories(url_df, max_categories, show_single_items)

    # Création des DataFrames finaux
    url_df, directories_df = create_final_dataframes(url_df, top_categories)

    # Mise à jour du session state
    st.session_state.url_df = url_df
    st.session_state.directories_df = directories_df

    logger.info("Traitement des URLs terminé avec succès")
    return True