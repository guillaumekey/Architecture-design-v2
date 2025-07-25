"""
Logique de jointure et agrégation des données sitemap et SEMrush
"""

import pandas as pd
import logging
from core.semrush_processor import prepare_semrush_data

logger = logging.getLogger(__name__)

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