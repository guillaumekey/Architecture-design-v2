"""
Configuration et constantes pour l'application SEO Analyzer
(Marchés SEMrush, headers HTTP, limites, configuration Streamlit)
"""

import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration Streamlit
STREAMLIT_CONFIG = {
    "layout": "wide",
    "page_title": "SEO Sitemap Analyzer"  # Sera mis à jour dynamiquement
}

# Marchés disponibles pour SEMrush
MARKETS = ['fr', 'it', 'es', 'uk', 'us', 'pt', 'nl', 'de', 'ca', 'br', 'be']

# Limites par défaut
DEFAULT_LIMITS = {
    'max_semrush_files': 6,
    'max_custom_sitemaps': 5,
    'request_timeout': 30
}

# Headers pour les requêtes HTTP
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

# Configuration des colonnes pour l'affichage des données
COLUMN_CONFIG = {
    "dominio": {"title": "Domaine", "width": 150},
    "dir_1": {"title": "Dir_1", "width": 100},
    "dir_2": {"title": "Dir_2", "width": 100},
    "dir_3": {"title": "Dir_3", "width": 100},
    "url": {"title": "URL", "width": None},
    "Directory": {"title": "Directory", "width": 150},
    "Niveau": {"title": "Niveau", "width": 100},
    "Nombre URLs": {"title": "Nombre URLs", "width": 120},
    "Traffic Total": {"title": "Traffic Total", "width": 120},
    "Total Mots-clés": {"title": "Total Mots-clés", "width": 120},
    "Volume Total": {"title": "Volume Total", "width": 120}
}

# SUPPRIMÉ: Options pour les dimensions du scatter plot
# (maintenant gérées dynamiquement via les traductions dans translations.py)