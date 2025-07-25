"""
Processeur de données SEMrush
"""

import pandas as pd
import logging
import streamlit as st

logger = logging.getLogger(__name__)

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