"""
Génération des graphiques (scatter plots, etc.) avec traductions complètes
"""

import plotly.express as px
import streamlit as st
import logging
from config.translations import get_text

logger = logging.getLogger(__name__)


def get_translated_axis_label(dimension, lang='fr'):
    """
    Retourne le label traduit pour une dimension donnée.

    Args:
        dimension (str): La dimension originale (ex: "Traffic Total")
        lang (str): Code de langue

    Returns:
        str: Label traduit
    """
    # Mapping des dimensions vers les clés de traduction
    dimension_mapping = {
        "Traffic Total": "traffic_total_dimension",
        "Total Mots-clés": "total_keywords_dimension",
        "Nombre URLs": "url_count_dimension",
        "Volume Total": "volume_total_dimension",
        # Ajouter les labels en anglais pour compatibilité
        "Total Traffic": "traffic_total_dimension",
        "Total Keywords": "total_keywords_dimension",
        "URL Count": "url_count_dimension",
        "Total Volume": "volume_total_dimension"
    }

    # Retourner la traduction si elle existe, sinon retourner la dimension originale
    translation_key = dimension_mapping.get(dimension)
    if translation_key:
        return get_text(translation_key, lang)
    return dimension


def plot_global_performance(performance_summary, x_dimension, y_dimension, size_dimension, lang='fr'):
    """
    Visualise la performance globale par catégorie avec des dimensions configurables.

    Args:
        performance_summary (DataFrame): Résumé des performances par répertoire.
        x_dimension (str): Nom de la colonne à utiliser pour l'axe X.
        y_dimension (str): Nom de la colonne à utiliser pour l'axe Y.
        size_dimension (str): Nom de la colonne à utiliser pour la taille des bulles.
        lang (str): Code de langue pour les traductions.

    Returns:
        None
    """

    # Traduire les labels des axes
    x_label = get_translated_axis_label(x_dimension, lang)
    y_label = get_translated_axis_label(y_dimension, lang)
    size_label = get_translated_axis_label(size_dimension, lang)

    # CORRECTION: Traduction complète du titre et des labels
    fig = px.scatter(
        performance_summary,
        x=x_dimension,
        y=y_dimension,
        size=size_dimension,
        color="Niveau",
        hover_name="Directory",
        title=f"{get_text('scatter_plot_title', lang)}: {x_label} vs {y_label}",
        labels={
            x_dimension: x_label,
            y_dimension: y_label,
            size_dimension: size_label,
            "Niveau": get_text('level', lang),
            "Directory": get_text('directory', lang)
        }
    )

    # CORRECTION: Mise en forme avec traductions
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title=get_text('level', lang),
        template="plotly_white"
    )

    # CORRECTION: Traduction du hover template
    fig.update_traces(
        hovertemplate=(
            f"<b>%{{hovertext}}</b><br>"
            f"{x_label}: %{{x}}<br>"
            f"{y_label}: %{{y}}<br>"
            f"{size_label}: %{{marker.size}}<br>"
            f"{get_text('level', lang)}: %{{fullData.color}}"
            "<extra></extra>"
        )
    )

    st.plotly_chart(fig, use_container_width=True)