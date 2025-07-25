"""
Fichier de traductions COMPLET pour l'application SEO Analyzer
"""

TRANSLATIONS = {
    'fr': {
        # Interface principale
        'page_title': 'Analyseur SEO de Sitemap',
        'app_title': '📊 Analyseur SEO de Sitemap',
        'language_selector': 'Choisir la langue',

        # Entrées utilisateur
        'url_input': "Entrez l'URL du site à analyser:",
        'custom_sitemaps_title': 'Sitemaps personnalisés (optionnel)',
        'sitemap_url': 'URL du sitemap',
        'add_sitemap': '+ Ajouter un sitemap',
        'max_categories': 'Nombre max de catégories',
        'show_single_items': 'Afficher les catégories à 1 élément',

        # Section SEMrush
        'semrush_title': 'Ajout de données SEM RUSH',
        'semrush_file': 'Fichier SEMrush',
        'market': 'Marché',
        'add_file': '+ Ajouter un fichier',
        'drag_drop_file': 'Glisser-déposer le fichier ici',
        'file_limit': 'Limite 200MB par fichier • CSV',
        'browse_files': 'Parcourir les fichiers',

        # Exclusions
        'exclusions_title': 'Configuration des exclusions',
        'exclusions_dir1': 'Exclusions niveau 1 (dir_1)',
        'exclusions_dir2': 'Exclusions niveau 2 (dir_2)',
        'exclusions_dir3': 'Exclusions niveau 3 (dir_3)',
        'exclusions_help1': 'Catégories à exclure au niveau 1 (séparées par des virgules)',
        'exclusions_help2': 'Catégories à exclure au niveau 2 (séparées par des virgules)',
        'exclusions_help3': 'Catégories à exclure au niveau 3 (séparées par des virgules)',

        # Boutons et actions
        'analyze_button': 'Analyser le site',
        'analysis_in_progress': 'Analyse en cours...',
        'analysis_complete': 'Analyse terminée avec succès !',
        'analysis_error': 'Erreur lors de l\'analyse du site',
        'enter_valid_url': 'Veuillez entrer une URL valide',

        # Messages d'information
        'active_exclusions': 'Exclusions actives:',
        'sitemap_manual': 'Sitemap fourni manuellement utilisé.',
        'sitemap_robots': 'Sitemaps récupérés depuis robots.txt.',
        'sitemap_fallback': 'Aucun sitemap trouvé dans robots.txt. Utilisation du fallback /sitemap.xml.',
        'sitemap_error': 'Erreur lors de la lecture du robots.txt. Utilisation du fallback /sitemap.xml.',

        # Filtres et navigation
        'navigation_filters': 'Filtres de navigation',
        'select_category': 'Sélectionner une catégorie',
        'select_subcategory': 'Sélectionner une sous-catégorie',
        'select_subsubcategory': 'Sélectionner une sous-sous-catégorie',
        'all': 'Toutes',

        # Treemap hover labels (encadré blanc)
        'label': 'étiquette',
        'count_label': 'nombre',
        'parent_label': 'parent',
        'id_label': 'id',

        # Statistiques
        'url_statistics': 'Statistiques des URLs',
        'total_urls': 'URLs Totales',
        'category_urls': 'URLs de la catégorie',
        'total_urls_help': 'Nombre total d\'URLs dans le sitemap',
        'category_urls_help': 'Nombre d\'URLs dans la catégorie sélectionnée',
        'subcategory_urls_help': 'Nombre d\'URLs dans la sous-catégorie sélectionnée',
        'subsubcategory_urls_help': 'Nombre d\'URLs dans la sous-sous-catégorie sélectionnée',

        # Colonnes tableau
        'domain': 'Domaine',
        'directory': 'Répertoire',
        'level': 'Niveau',
        'url_count': 'Nombre URLs',
        'total_traffic': 'Trafic Total',
        'total_keywords': 'Total Mots-clés',
        'total_volume': 'Volume Total',

        # Sections résultats
        'semrush_statistics': 'Statistiques SEM Rush',
        'semrush_url_statistics': 'Statistiques URLs SEM Rush',
        'urls_not_in_sitemap': 'URLs présentes dans SEMrush mais absentes du sitemap',
        'results_by_page_level': 'Résultats par niveau de page',
        'filter_by_dir1': 'Filtrer par Dir_1',
        'filter_by_dir2': 'Filtrer par Dir_2',

        # Performance globale
        'global_performance': 'Analyse de Performance Globale',
        'configure_scatter': 'Configurer le Scatter Plot',
        'scatter_plot_title': 'Graphique de Dispersion',
        'x_axis': 'Axe X',
        'y_axis': 'Axe Y',
        'bubble_size': 'Taille des bulles',

        # Dimensions du scatter plot (NOUVELLES TRADUCTIONS)
        'traffic_total_dimension': 'Trafic Total',
        'total_keywords_dimension': 'Total Mots-clés',
        'url_count_dimension': 'Nombre URLs',
        'volume_total_dimension': 'Volume Total',

        # Totaux et métriques
        'total_url_count': 'Total nombre d\'URLs',
        'total_traffic_sum': 'Total trafic',
        'total_keywords_sum': 'Total mots clés',
        'total_volume_sum': 'Total volume',
        'total_keywords_metric': 'Total mots clés',

        # En-têtes de tableaux SEMrush (NOUVELLES TRADUCTIONS)
        'keyword': 'Mot-clé',
        'position': 'Position',
        'previous_position': 'Position précédente',
        'search_volume': 'Volume de recherche',
        'keyword_difficulty': 'Difficulté mot-clé',
        'cpc': 'CPC',
        'url': 'URL',
        'traffic': 'Trafic',
        'traffic_percent': 'Trafic (%)',
        'traffic_cost': 'Coût du trafic',
        'number_of_keywords': 'Nombre de mots-clés',
        'position_type': 'Type de position',

        # Treemap labels
        'pages': 'Pages',
        'of_parent': 'du parent',
        'of_total': 'du total',
        'count': 'nombre',
        'parent': 'parent',
        'about': 'À propos',
        'about_description': 'Cette application analyse la structure des URLs d\'un site web à partir de son sitemap.',
        'features': 'Fonctionnalités :',
        'feature_sitemap': 'Analyse de sitemap',
        'feature_treemap': 'Visualisation treemap',
        'feature_filtering': 'Filtrage par niveau',
        'feature_exclusion': 'Exclusion par niveau',
        'feature_semrush': 'Analyse SEMrush multi-marchés',
        'usage_guide': 'Guide d\'usage des filtres :',
        'max_categories_help': 'Limite le nombre de catégories dir_1 à afficher dans l\'analyse. Les catégories sont classées par ordre décroissant du nombre d\'URLs. `-1` = afficher toutes les catégories.',
        'exclusions_config': 'Configuration des exclusions :',
        'exclusions_warning': '⚠️ Important : Pour de meilleurs résultats, évitez d\'utiliser des termes d\'exclusion différents sur plusieurs niveaux de directory (dir_1, dir_2, dir_3).'
    },

    'en': {
        # Main interface
        'page_title': 'SEO Sitemap Analyzer',
        'app_title': '📊 SEO Sitemap Analyzer',
        'language_selector': 'Choose language',

        # User inputs
        'url_input': 'Enter the website URL to analyze:',
        'custom_sitemaps_title': 'Custom sitemaps (optional)',
        'sitemap_url': 'Sitemap URL',
        'add_sitemap': '+ Add sitemap',
        'max_categories': 'Max number of categories',
        'show_single_items': 'Show single-item categories',

        # SEMrush section
        'semrush_title': 'Add SEM RUSH data',
        'semrush_file': 'SEMrush file',
        'market': 'Market',
        'add_file': '+ Add file',
        'drag_drop_file': 'Drag and drop file here',
        'file_limit': 'Limit 200MB per file • CSV',
        'browse_files': 'Browse files',

        # Exclusions
        'exclusions_title': 'Exclusions configuration',
        'exclusions_dir1': 'Level 1 exclusions (dir_1)',
        'exclusions_dir2': 'Level 2 exclusions (dir_2)',
        'exclusions_dir3': 'Level 3 exclusions (dir_3)',
        'exclusions_help1': 'Categories to exclude at level 1 (comma separated)',
        'exclusions_help2': 'Categories to exclude at level 2 (comma separated)',
        'exclusions_help3': 'Categories to exclude at level 3 (comma separated)',

        # Buttons and actions
        'analyze_button': 'Analyze website',
        'analysis_in_progress': 'Analysis in progress...',
        'analysis_complete': 'Analysis completed successfully!',
        'analysis_error': 'Error during website analysis',
        'enter_valid_url': 'Please enter a valid URL',

        # Information messages
        'active_exclusions': 'Active exclusions:',
        'sitemap_manual': 'Manually provided sitemap used.',
        'sitemap_robots': 'Sitemaps retrieved from robots.txt.',
        'sitemap_fallback': 'No sitemap found in robots.txt. Using fallback /sitemap.xml.',
        'sitemap_error': 'Error reading robots.txt. Using fallback /sitemap.xml.',

        # Filters and navigation
        'navigation_filters': 'Navigation filters',
        'select_category': 'Select a category',
        'select_subcategory': 'Select a subcategory',
        'select_subsubcategory': 'Select a sub-subcategory',
        'all': 'All',

        # Treemap hover labels (white box)
        'label': 'label',
        'count_label': 'number',
        'parent_label': 'parent',
        'id_label': 'id',

        # Statistics
        'url_statistics': 'URL Statistics',
        'total_urls': 'Total URLs',
        'category_urls': 'Category URLs',
        'total_urls_help': 'Total number of URLs in the sitemap',
        'category_urls_help': 'Number of URLs in the selected category',
        'subcategory_urls_help': 'Number of URLs in the selected subcategory',
        'subsubcategory_urls_help': 'Number of URLs in the selected sub-subcategory',

        # Table columns
        'domain': 'Domain',
        'directory': 'Directory',
        'level': 'Level',
        'url_count': 'URL Count',
        'total_traffic': 'Total Traffic',
        'total_keywords': 'Total Keywords',
        'total_volume': 'Total Volume',

        # Results sections
        'semrush_statistics': 'SEM Rush Statistics',
        'semrush_url_statistics': 'SEM Rush URL Statistics',
        'urls_not_in_sitemap': 'URLs present in SEMrush but absent from sitemap',
        'results_by_page_level': 'Results by page level',
        'filter_by_dir1': 'Filter by Dir_1',
        'filter_by_dir2': 'Filter by Dir_2',

        # Global performance
        'global_performance': 'Global Performance Analysis',
        'configure_scatter': 'Configure Scatter Plot',
        'scatter_plot_title': 'Scatter Plot',
        'x_axis': 'X Axis',
        'y_axis': 'Y Axis',
        'bubble_size': 'Bubble size',

        # Scatter plot dimensions (NEW TRANSLATIONS)
        'traffic_total_dimension': 'Total Traffic',
        'total_keywords_dimension': 'Total Keywords',
        'url_count_dimension': 'URL Count',
        'volume_total_dimension': 'Total Volume',

        # Totals and metrics
        'total_url_count': 'Total URL count',
        'total_traffic_sum': 'Total traffic',
        'total_keywords_sum': 'Total keywords',
        'total_volume_sum': 'Total volume',
        'total_keywords_metric': 'Total keywords',

        # SEMrush table headers (NEW TRANSLATIONS)
        'keyword': 'Keyword',
        'position': 'Position',
        'previous_position': 'Previous position',
        'search_volume': 'Search Volume',
        'keyword_difficulty': 'Keyword Difficulty',
        'cpc': 'CPC',
        'url': 'URL',
        'traffic': 'Traffic',
        'traffic_percent': 'Traffic (%)',
        'traffic_cost': 'Traffic Cost',
        'number_of_keywords': 'Number of Keywords',
        'position_type': 'Position Type',

        # Treemap labels
        'pages': 'Pages',
        'of_parent': 'of parent',
        'of_total': 'of total',
        'count': 'count',
        'parent': 'parent',
        'about': 'About',
        'about_description': 'This application analyzes the URL structure of a website from its sitemap.',
        'features': 'Features:',
        'feature_sitemap': 'Sitemap analysis',
        'feature_treemap': 'Treemap visualization',
        'feature_filtering': 'Level-based filtering',
        'feature_exclusion': 'Level-based exclusion',
        'feature_semrush': 'Multi-market SEMrush analysis',
        'usage_guide': 'Filter usage guide:',
        'max_categories_help': 'Limits the number of dir_1 categories to display in the analysis. Categories are sorted by descending number of URLs. `-1` = show all categories.',
        'exclusions_config': 'Exclusions configuration:',
        'exclusions_warning': '⚠️ Important: For better results, avoid using different exclusion terms across multiple directory levels (dir_1, dir_2, dir_3).'
    },

    'es': {
        # Interfaz principal
        'page_title': 'Analizador SEO de Sitemap',
        'app_title': '📊 Analizador SEO de Sitemap',
        'language_selector': 'Elegir idioma',

        # Entradas del usuario
        'url_input': 'Ingresa la URL del sitio web a analizar:',
        'custom_sitemaps_title': 'Sitemaps personalizados (opcional)',
        'sitemap_url': 'URL del sitemap',
        'add_sitemap': '+ Agregar sitemap',
        'max_categories': 'Número máximo de categorías',
        'show_single_items': 'Mostrar categorías de un elemento',

        # Sección SEMrush
        'semrush_title': 'Agregar datos de SEM RUSH',
        'semrush_file': 'Archivo SEMrush',
        'market': 'Mercado',
        'add_file': '+ Agregar archivo',
        'drag_drop_file': 'Arrastra y suelta el archivo aquí',
        'file_limit': 'Límite 200MB por archivo • CSV',
        'browse_files': 'Explorar archivos',

        # Exclusiones
        'exclusions_title': 'Configuración de exclusiones',
        'exclusions_dir1': 'Exclusiones nivel 1 (dir_1)',
        'exclusions_dir2': 'Exclusiones nivel 2 (dir_2)',
        'exclusions_dir3': 'Exclusiones nivel 3 (dir_3)',
        'exclusions_help1': 'Categorías a excluir en el nivel 1 (separadas por comas)',
        'exclusions_help2': 'Categorías a excluir en el nivel 2 (separadas por comas)',
        'exclusions_help3': 'Categorías a excluir en el nivel 3 (separadas por comas)',

        # Botones y acciones
        'analyze_button': 'Analizar sitio web',
        'analysis_in_progress': 'Análisis en progreso...',
        'analysis_complete': '¡Análisis completado exitosamente!',
        'analysis_error': 'Error durante el análisis del sitio web',
        'enter_valid_url': 'Por favor ingresa una URL válida',

        # Mensajes de información
        'active_exclusions': 'Exclusiones activas:',
        'sitemap_manual': 'Sitemap proporcionado manualmente utilizado.',
        'sitemap_robots': 'Sitemaps recuperados desde robots.txt.',
        'sitemap_fallback': 'No se encontró sitemap en robots.txt. Usando fallback /sitemap.xml.',
        'sitemap_error': 'Error leyendo robots.txt. Usando fallback /sitemap.xml.',

        # Filtros y navegación
        'navigation_filters': 'Filtros de navegación',
        'select_category': 'Seleccionar una categoría',
        'select_subcategory': 'Seleccionar una subcategoría',
        'select_subsubcategory': 'Seleccionar una sub-subcategoría',
        'all': 'Todas',

        # Etiquetas hover del treemap (cuadro blanco)
        'label': 'etiqueta',
        'count_label': 'número',
        'parent_label': 'padre',
        'id_label': 'id',

        # Estadísticas
        'url_statistics': 'Estadísticas de URLs',
        'total_urls': 'URLs Totales',
        'category_urls': 'URLs de la categoría',
        'total_urls_help': 'Número total de URLs en el sitemap',
        'category_urls_help': 'Número de URLs en la categoría seleccionada',
        'subcategory_urls_help': 'Número de URLs en la subcategoría seleccionada',
        'subsubcategory_urls_help': 'Número de URLs en la sub-subcategoría seleccionada',

        # Columnas de tabla
        'domain': 'Dominio',
        'directory': 'Directorio',
        'level': 'Nivel',
        'url_count': 'Cantidad URLs',
        'total_traffic': 'Tráfico Total',
        'total_keywords': 'Total Palabras Clave',
        'total_volume': 'Volumen Total',

        # Secciones de resultados
        'semrush_statistics': 'Estadísticas SEM Rush',
        'semrush_url_statistics': 'Estadísticas URLs SEM Rush',
        'urls_not_in_sitemap': 'URLs presentes en SEMrush pero ausentes del sitemap',
        'results_by_page_level': 'Resultados por nivel de página',
        'filter_by_dir1': 'Filtrar por Dir_1',
        'filter_by_dir2': 'Filtrar por Dir_2',

        # Rendimiento global
        'global_performance': 'Análisis de Rendimiento Global',
        'configure_scatter': 'Configurar Gráfico de Dispersión',
        'scatter_plot_title': 'Gráfico de Dispersión',
        'x_axis': 'Eje X',
        'y_axis': 'Eje Y',
        'bubble_size': 'Tamaño de burbuja',

        # Dimensiones del scatter plot (NUEVAS TRADUCCIONES)
        'traffic_total_dimension': 'Tráfico Total',
        'total_keywords_dimension': 'Total Palabras Clave',
        'url_count_dimension': 'Cantidad URLs',
        'volume_total_dimension': 'Volumen Total',

        # Totales y métricas
        'total_url_count': 'Total cantidad de URLs',
        'total_traffic_sum': 'Total tráfico',
        'total_keywords_sum': 'Total palabras clave',
        'total_volume_sum': 'Total volumen',
        'total_keywords_metric': 'Total palabras clave',

        # Encabezados de tabla SEMrush (NUEVAS TRADUCCIONES)
        'keyword': 'Palabra clave',
        'position': 'Posición',
        'previous_position': 'Posición anterior',
        'search_volume': 'Volumen de búsqueda',
        'keyword_difficulty': 'Dificultad palabra clave',
        'cpc': 'CPC',
        'url': 'URL',
        'traffic': 'Tráfico',
        'traffic_percent': 'Tráfico (%)',
        'traffic_cost': 'Costo del tráfico',
        'number_of_keywords': 'Número de palabras clave',
        'position_type': 'Tipo de posición',

        # Etiquetas del treemap
        'pages': 'Páginas',
        'of_parent': 'del padre',
        'of_total': 'del total',
        'count': 'cantidad',
        'parent': 'padre',
        'about': 'Acerca de',
        'about_description': 'Esta aplicación analiza la estructura de URLs de un sitio web desde su sitemap.',
        'features': 'Características:',
        'feature_sitemap': 'Análisis de sitemap',
        'feature_treemap': 'Visualización treemap',
        'feature_filtering': 'Filtrado por nivel',
        'feature_exclusion': 'Exclusión por nivel',
        'feature_semrush': 'Análisis SEMrush multi-mercado',
        'usage_guide': 'Guía de uso de filtros:',
        'max_categories_help': 'Limita el número de categorías dir_1 a mostrar en el análisis. Las categorías se ordenan por número descendente de URLs. `-1` = mostrar todas las categorías.',
        'exclusions_config': 'Configuración de exclusiones:',
        'exclusions_warning': '⚠️ Importante: Para mejores resultados, evita usar términos de exclusión diferentes en múltiples niveles de directorio (dir_1, dir_2, dir_3).'
    },

    'de': {
        # Hauptoberfläche
        'page_title': 'SEO Sitemap Analysator',
        'app_title': '📊 SEO Sitemap Analysator',
        'language_selector': 'Sprache wählen',

        # Benutzereingaben
        'url_input': 'Website-URL zur Analyse eingeben:',
        'custom_sitemaps_title': 'Benutzerdefinierte Sitemaps (optional)',
        'sitemap_url': 'Sitemap-URL',
        'add_sitemap': '+ Sitemap hinzufügen',
        'max_categories': 'Maximale Anzahl Kategorien',
        'show_single_items': 'Ein-Element-Kategorien anzeigen',

        # SEMrush-Bereich
        'semrush_title': 'SEM RUSH Daten hinzufügen',
        'semrush_file': 'SEMrush-Datei',
        'market': 'Markt',
        'add_file': '+ Datei hinzufügen',
        'drag_drop_file': 'Datei hier ablegen',
        'file_limit': 'Limit 200MB pro Datei • CSV',
        'browse_files': 'Dateien durchsuchen',

        # Ausschlüsse
        'exclusions_title': 'Ausschlüsse-Konfiguration',
        'exclusions_dir1': 'Ebene 1 Ausschlüsse (dir_1)',
        'exclusions_dir2': 'Ebene 2 Ausschlüsse (dir_2)',
        'exclusions_dir3': 'Ebene 3 Ausschlüsse (dir_3)',
        'exclusions_help1': 'Kategorien auf Ebene 1 ausschließen (durch Kommas getrennt)',
        'exclusions_help2': 'Kategorien auf Ebene 2 ausschließen (durch Kommas getrennt)',
        'exclusions_help3': 'Kategorien auf Ebene 3 ausschließen (durch Kommas getrennt)',

        # Schaltflächen und Aktionen
        'analyze_button': 'Website analysieren',
        'analysis_in_progress': 'Analyse läuft...',
        'analysis_complete': 'Analyse erfolgreich abgeschlossen!',
        'analysis_error': 'Fehler bei der Website-Analyse',
        'enter_valid_url': 'Bitte geben Sie eine gültige URL ein',

        # Informationsmeldungen
        'active_exclusions': 'Aktive Ausschlüsse:',
        'sitemap_manual': 'Manuell bereitgestellte Sitemap verwendet.',
        'sitemap_robots': 'Sitemaps aus robots.txt abgerufen.',
        'sitemap_fallback': 'Keine Sitemap in robots.txt gefunden. Verwende Fallback /sitemap.xml.',
        'sitemap_error': 'Fehler beim Lesen von robots.txt. Verwende Fallback /sitemap.xml.',

        # Filter und Navigation
        'navigation_filters': 'Navigationsfilter',
        'select_category': 'Kategorie auswählen',
        'select_subcategory': 'Unterkategorie auswählen',
        'select_subsubcategory': 'Unter-Unterkategorie auswählen',
        'all': 'Alle',

        # Treemap-Hover-Labels (weißer Kasten)
        'label': 'Bezeichnung',
        'count_label': 'Anzahl',
        'parent_label': 'Elternelement',
        'id_label': 'Id',

        # Statistiken
        'url_statistics': 'URL-Statistiken',
        'total_urls': 'Gesamt-URLs',
        'category_urls': 'Kategorie-URLs',
        'total_urls_help': 'Gesamtanzahl der URLs in der Sitemap',
        'category_urls_help': 'Anzahl der URLs in der ausgewählten Kategorie',
        'subcategory_urls_help': 'Anzahl der URLs in der ausgewählten Unterkategorie',
        'subsubcategory_urls_help': 'Anzahl der URLs in der ausgewählten Unter-Unterkategorie',

        # Tabellenspalten
        'domain': 'Domain',
        'directory': 'Verzeichnis',
        'level': 'Ebene',
        'url_count': 'URL-Anzahl',
        'total_traffic': 'Gesamt-Traffic',
        'total_keywords': 'Gesamt-Keywords',
        'total_volume': 'Gesamt-Volumen',

        # Ergebnisbereiche
        'semrush_statistics': 'SEM Rush Statistiken',
        'semrush_url_statistics': 'SEM Rush URL-Statistiken',
        'urls_not_in_sitemap': 'URLs in SEMrush vorhanden, aber in Sitemap fehlend',
        'results_by_page_level': 'Ergebnisse nach Seitenebene',
        'filter_by_dir1': 'Nach Dir_1 filtern',
        'filter_by_dir2': 'Nach Dir_2 filtern',

        # Globale Leistung
        'global_performance': 'Globale Leistungsanalyse',
        'configure_scatter': 'Streudiagramm konfigurieren',
        'scatter_plot_title': 'Streudiagramm',
        'x_axis': 'X-Achse',
        'y_axis': 'Y-Achse',
        'bubble_size': 'Blasengröße',

        # Scatter-Plot-Dimensionen (NEUE ÜBERSETZUNGEN)
        'traffic_total_dimension': 'Gesamt-Traffic',
        'total_keywords_dimension': 'Gesamt-Keywords',
        'url_count_dimension': 'URL-Anzahl',
        'volume_total_dimension': 'Gesamt-Volumen',

        # Gesamtwerte und Metriken
        'total_url_count': 'Gesamt URL-Anzahl',
        'total_traffic_sum': 'Gesamt-Traffic',
        'total_keywords_sum': 'Gesamt-Keywords',
        'total_volume_sum': 'Gesamt-Volumen',
        'total_keywords_metric': 'Gesamt-Keywords',

        # SEMrush-Tabellenkopfzeilen (NEUE ÜBERSETZUNGEN)
        'keyword': 'Schlüsselwort',
        'position': 'Position',
        'previous_position': 'Vorherige Position',
        'search_volume': 'Suchvolumen',
        'keyword_difficulty': 'Keyword-Schwierigkeit',
        'cpc': 'CPC',
        'url': 'URL',
        'traffic': 'Traffic',
        'traffic_percent': 'Traffic (%)',
        'traffic_cost': 'Traffic-Kosten',
        'number_of_keywords': 'Anzahl der Keywords',
        'position_type': 'Positionstyp',

        # Treemap-Labels
        'pages': 'Seiten',
        'of_parent': 'vom Elternteil',
        'of_total': 'vom Gesamt',
        'count': 'Anzahl',
        'parent': 'Elternteil',
        'about': 'Über',
        'about_description': 'Diese Anwendung analysiert die URL-Struktur einer Website aus ihrer Sitemap.',
        'features': 'Funktionen:',
        'feature_sitemap': 'Sitemap-Analyse',
        'feature_treemap': 'Treemap-Visualisierung',
        'feature_filtering': 'Ebenen-basierte Filterung',
        'feature_exclusion': 'Ebenen-basierte Ausschlüsse',
        'feature_semrush': 'Multi-Markt SEMrush-Analyse',
        'usage_guide': 'Leitfaden zur Filternutzung:',
        'max_categories_help': 'Begrenzt die Anzahl der dir_1-Kategorien, die in der Analyse angezeigt werden. Kategorien werden nach absteigender URL-Anzahl sortiert. `-1` = alle Kategorien anzeigen.',
        'exclusions_config': 'Ausschlüsse-Konfiguration:',
        'exclusions_warning': '⚠️ Wichtig: Für bessere Ergebnisse vermeiden Sie unterschiedliche Ausschlussbegriffe auf mehreren Verzeichnisebenen (dir_1, dir_2, dir_3).'
    },

    'it': {
        # Interfaccia principale
        'page_title': 'Analizzatore SEO Sitemap',
        'app_title': '📊 Analizzatore SEO Sitemap',
        'language_selector': 'Scegli lingua',

        # Input utente
        'url_input': 'Inserisci l\'URL del sito web da analizzare:',
        'custom_sitemaps_title': 'Sitemap personalizzate (opzionale)',
        'sitemap_url': 'URL sitemap',
        'add_sitemap': '+ Aggiungi sitemap',
        'max_categories': 'Numero massimo di categorie',
        'show_single_items': 'Mostra categorie a elemento singolo',

        # Sezione SEMrush
        'semrush_title': 'Aggiungi dati SEM RUSH',
        'semrush_file': 'File SEMrush',
        'market': 'Mercato',
        'add_file': '+ Aggiungi file',
        'drag_drop_file': 'Trascina e rilascia il file qui',
        'file_limit': 'Limite 200MB per file • CSV',
        'browse_files': 'Sfoglia file',

        # Esclusioni
        'exclusions_title': 'Configurazione esclusioni',
        'exclusions_dir1': 'Esclusioni livello 1 (dir_1)',
        'exclusions_dir2': 'Esclusioni livello 2 (dir_2)',
        'exclusions_dir3': 'Esclusioni livello 3 (dir_3)',
        'exclusions_help1': 'Categorie da escludere al livello 1 (separate da virgole)',
        'exclusions_help2': 'Categorie da escludere al livello 2 (separate da virgole)',
        'exclusions_help3': 'Categorie da escludere al livello 3 (separate da virgole)',

        # Pulsanti e azioni
        'analyze_button': 'Analizza sito web',
        'analysis_in_progress': 'Analisi in corso...',
        'analysis_complete': 'Analisi completata con successo!',
        'analysis_error': 'Errore durante l\'analisi del sito web',
        'enter_valid_url': 'Si prega di inserire un URL valido',

        # Messaggi informativi
        'active_exclusions': 'Esclusioni attive:',
        'sitemap_manual': 'Sitemap fornita manualmente utilizzata.',
        'sitemap_robots': 'Sitemap recuperate da robots.txt.',
        'sitemap_fallback': 'Nessuna sitemap trovata in robots.txt. Usando fallback /sitemap.xml.',
        'sitemap_error': 'Errore nella lettura di robots.txt. Usando fallback /sitemap.xml.',

        # Filtri e navigazione
        'navigation_filters': 'Filtri di navigazione',
        'select_category': 'Seleziona una categoria',
        'select_subcategory': 'Seleziona una sottocategoria',
        'select_subsubcategory': 'Seleziona una sotto-sottocategoria',
        'all': 'Tutte',

        # Etichette hover treemap (riquadro bianco)
        'label': 'etichetta',
        'count_label': 'numero',
        'parent_label': 'genitore',
        'id_label': 'id',

        # Statistiche
        'url_statistics': 'Statistiche URL',
        'total_urls': 'URL Totali',
        'category_urls': 'URL della categoria',
        'total_urls_help': 'Numero totale di URL nella sitemap',
        'category_urls_help': 'Numero di URL nella categoria selezionata',
        'subcategory_urls_help': 'Numero di URL nella sottocategoria selezionata',
        'subsubcategory_urls_help': 'Numero di URL nella sotto-sottocategoria selezionata',

        # Colonne tabella
        'domain': 'Dominio',
        'directory': 'Directory',
        'level': 'Livello',
        'url_count': 'Conteggio URL',
        'total_traffic': 'Traffico Totale',
        'total_keywords': 'Parole Chiave Totali',
        'total_volume': 'Volume Totale',

        # Sezioni risultati
        'semrush_statistics': 'Statistiche SEM Rush',
        'semrush_url_statistics': 'Statistiche URL SEM Rush',
        'urls_not_in_sitemap': 'URL presenti in SEMrush ma assenti dalla sitemap',
        'results_by_page_level': 'Risultati per livello di pagina',
        'filter_by_dir1': 'Filtra per Dir_1',
        'filter_by_dir2': 'Filtra per Dir_2',

        # Performance globale
        'global_performance': 'Analisi delle Performance Globali',
        'configure_scatter': 'Configura Grafico a Dispersione',
        'scatter_plot_title': 'Grafico a Dispersione',
        'x_axis': 'Asse X',
        'y_axis': 'Asse Y',
        'bubble_size': 'Dimensione bolla',

        # Dimensioni scatter plot (NUOVE TRADUZIONI)
        'traffic_total_dimension': 'Traffico Totale',
        'total_keywords_dimension': 'Parole Chiave Totali',
        'url_count_dimension': 'Conteggio URL',
        'volume_total_dimension': 'Volume Totale',

        # Totali e metriche
        'total_url_count': 'Conteggio totale URL',
        'total_traffic_sum': 'Traffico totale',
        'total_keywords_sum': 'Parole chiave totali',
        'total_volume_sum': 'Volume totale',
        'total_keywords_metric': 'Parole chiave totali',

        # Intestazioni tabella SEMrush (NUOVE TRADUZIONI)
        'keyword': 'Parola chiave',
        'position': 'Posizione',
        'previous_position': 'Posizione precedente',
        'search_volume': 'Volume di ricerca',
        'keyword_difficulty': 'Difficoltà parola chiave',
        'cpc': 'CPC',
        'url': 'URL',
        'traffic': 'Traffico',
        'traffic_percent': 'Traffico (%)',
        'traffic_cost': 'Costo del traffico',
        'number_of_keywords': 'Numero di parole chiave',
        'position_type': 'Tipo di posizione',

        # Etichette treemap
        'pages': 'Pagine',
        'of_parent': 'del genitore',
        'of_total': 'del totale',
        'count': 'conteggio',
        'parent': 'genitore',
        'about': 'Informazioni',
        'about_description': 'Questa applicazione analizza la struttura degli URL di un sito web dalla sua sitemap.',
        'features': 'Caratteristiche:',
        'feature_sitemap': 'Analisi sitemap',
        'feature_treemap': 'Visualizzazione treemap',
        'feature_filtering': 'Filtri per livello',
        'feature_exclusion': 'Esclusioni per livello',
        'feature_semrush': 'Analisi SEMrush multi-mercato',
        'usage_guide': 'Guida all\'uso dei filtri:',
        'max_categories_help': 'Limita il numero di categorie dir_1 da mostrare nell\'analisi. Le categorie sono ordinate per numero decrescente di URL. `-1` = mostra tutte le categorie.',
        'exclusions_config': 'Configurazione esclusioni:',
        'exclusions_warning': '⚠️ Importante: Per migliori risultati, evitare di usare termini di esclusione diversi su più livelli di directory (dir_1, dir_2, dir_3).'
    }
}

def get_text(key, lang='fr'):
    """Récupère le texte traduit pour une clé donnée."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['fr']).get(key, key)

def get_available_languages():
    """Retourne la liste des langues disponibles."""
    return {
        'fr': 'Français',
        'en': 'English',
        'es': 'Español',
        'de': 'Deutsch',
        'it': 'Italiano'
    }

def get_translated_dimension_options(lang='fr'):
    """Retourne les options de dimensions traduites pour le scatter plot."""
    return {
        get_text('traffic_total_dimension', lang): "Traffic Total",
        get_text('total_keywords_dimension', lang): "Total Mots-clés",
        get_text('url_count_dimension', lang): "Nombre URLs",
        get_text('volume_total_dimension', lang): "Volume Total"
    }