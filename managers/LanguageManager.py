import json
import os

class LanguageManager:
	PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	LANGUAGE_FOLDER = os.path.join(PROJECT_ROOT, 'assets', 'languages')
	LANGUAGES_CONFIG = os.path.join(PROJECT_ROOT, 'config', 'languages.json')

	def __init__(self):
		self.supported_languages = self.load_supported_languages()

	def load_supported_languages(self):
		""" Load the list of supported languages from the configuration file. """
		with open(self.LANGUAGES_CONFIG, 'r', encoding='utf-8') as f:
			return json.load(f)

	def load_language(self, selected_language):
		"""
			Load the language file for the selected language.
			Raises a KeyError if the language is not supported.
		"""
		file_name = self.supported_languages.get(selected_language)
		if not file_name:
			raise KeyError(f"Language '{selected_language}' is not supported.")

		file_path = os.path.join(self.LANGUAGE_FOLDER, file_name)
		with open(file_path, 'r', encoding='utf-8') as f:
			return json.load(f)