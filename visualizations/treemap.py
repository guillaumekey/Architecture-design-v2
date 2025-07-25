# DANS VOTRE FICHIER treemap.py
# REMPLACER LA FONCTION create_treemap() PAR :

import plotly.express as px
import datetime
import logging
from config.translations import get_text

logger = logging.getLogger(__name__)

def create_treemap(directories_df, domain, lang='fr'):
    """Crée le treemap de la structure du site avec traductions."""
    logger.info("Création du treemap")

    today = datetime.datetime.now(datetime.timezone.utc).strftime('%B %d, %Y')

    treemap_fig = px.treemap(
        directories_df,
        path=['dominio', 'dir_1', 'dir_2', 'dir_3'],
        title=f'{domain} Categories Structure (date: {today})',
        height=750
    )

    # CORRECTION: Template traduit
    treemap_fig.update_traces(
        texttemplate=f"<b>%{{label}}</b><br>{get_text('pages', lang)}: %{{value}}<br>%{{percentParent}} {get_text('of_parent', lang)}<br>%{{percentRoot}} {get_text('of_total', lang)}",
        root_color="lightgrey"
    )

    return treemap_fig