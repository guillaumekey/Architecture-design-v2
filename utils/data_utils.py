"""
Utilitaires pour la manipulation de données
"""

import logging

logger = logging.getLogger(__name__)

def clean_exclusions(exclusion_string):
    """Nettoie et prépare la liste des exclusions."""
    logger.info(f"Nettoyage des exclusions: {exclusion_string}")
    if not exclusion_string:
        return []
    cleaned = [item.strip() for item in exclusion_string.split(',') if item.strip()]
    logger.info(f"Exclusions nettoyées: {cleaned}")
    return cleaned

def get_url_statistics(directories_df, selected_category='Toutes', selected_subcategory='Toutes', selected_subsubcategory='Toutes'):
    """Calcule les statistiques des URLs pour chaque niveau de catégorie."""
    logger.info(
        f"Calcul des statistiques - Catégorie: {selected_category}, Sous-catégorie: {selected_subcategory}, Sous-sous-catégorie: {selected_subsubcategory}")
    total_urls = len(directories_df)

    if selected_category == 'Toutes':
        logger.info(f"Statistiques globales - Total URLs: {total_urls}")
        return {
            'total': total_urls,
            'dir1': ('Toutes', total_urls),
            'dir2': ('-', '-'),
            'dir3': ('-', '-')
        }

    dir1_df = directories_df[directories_df['dir_1'] == selected_category]
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

def filter_and_display_urls(directories_df, selected_category, selected_subcategory='Toutes', selected_subsubcategory='Toutes'):
    """Filtre les URLs en fonction des catégories sélectionnées."""
    logger.info(
        f"Application des filtres - Catégorie: {selected_category}, Sous-catégorie: {selected_subcategory}, Sous-sous-catégorie: {selected_subsubcategory}")
    if selected_category == 'Toutes':
        logger.info("Retour de toutes les URLs sans filtre")
        return directories_df

    filtered_df = directories_df[directories_df['dir_1'] == selected_category]
    logger.info(f"URLs après filtre dir_1: {len(filtered_df)}")

    if selected_subcategory != 'Toutes':
        filtered_df = filtered_df[filtered_df['dir_2'] == selected_subcategory]
        logger.info(f"URLs après filtre dir_2: {len(filtered_df)}")

    if selected_subsubcategory != 'Toutes':
        filtered_df = filtered_df[filtered_df['dir_3'] == selected_subsubcategory]
        logger.info(f"URLs après filtre dir_3: {len(filtered_df)}")

    return filtered_df