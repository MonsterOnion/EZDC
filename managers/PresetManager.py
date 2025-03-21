import json
import os

class PresetManager:

	PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	PRESET_FOLDER = os.path.join(PROJECT_ROOT, 'config', 'preset')
	DOWNLOAD_PRESET_FOLDER = os.path.join(PRESET_FOLDER, 'download')
	DOWNLOAD_PRESET_FILE = os.path.join(DOWNLOAD_PRESET_FOLDER, 'preset.json')
	CONVERSION_PRESET_FOLDER = os.path.join(PRESET_FOLDER, 'conversion')
	CONVERSION_PRESET_FILE = os.path.join(CONVERSION_PRESET_FOLDER, 'preset.json')

	def __init__(self):
		self.download_preset = self.load_download_preset()
		self.conversion_preset = self.load_conversion_preset()

	def load_download_preset(self):
		""" Load the list of download preset. """
		with open(self.DOWNLOAD_PRESET_FILE, 'r', encoding='utf-8') as f:
			return json.load(f)

	def load_conversion_preset(self):
		""" Load the list of conversion preset. """
		with open(self.CONVERSION_PRESET_FILE, 'r', encoding='utf-8') as f:
			return json.load(f)