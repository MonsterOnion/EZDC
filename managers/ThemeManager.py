import json
import os

class ThemeManager:
	PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	THEMES_FOLDER = os.path.join(PROJECT_ROOT, 'assets', 'themes')
	THEMES_CONFIG = os.path.join(PROJECT_ROOT, 'config', 'themes.json')

	def __init__(self):
		self.supported_themes = self.load_supported_themes()

	def load_supported_themes(self):
		""" Load the list of supported themes from the configuration file. """
		with open(self.THEMES_CONFIG, 'r', encoding='utf-8') as f:
			return json.load(f)

	def load_theme(self, theme_name):
		""" Load the theme file for the given theme name. """
		theme_file = self.supported_themes.get(theme_name, "light.qss")
		theme_path = os.path.join(self.THEMES_FOLDER, theme_file)

		with open(theme_path, "r") as f:
			return f.read()