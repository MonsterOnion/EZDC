import json
import os
import platform
from pathlib import Path

class SettingsManager:
	SYSTEM = platform.system()

	if SYSTEM == "Windows":
		PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		CONFIG_FOLDER = os.path.join(PROJECT_ROOT, 'config')
		SETTINGS_FILE = os.path.join(CONFIG_FOLDER, 'settings.json')
		MEDIA_FOLDER = os.path.join(PROJECT_ROOT, 'media')
	elif SYSTEM == "Darwin":
		PROJECT_NAME = "Media download and conversion"
		CONFIG_FOLDER = os.path.join(str(Path.home()), "Library", "Application Support", PROJECT_NAME)
		MEDIA_FOLDER = os.path.join(str(Path.home()), "Downloads", PROJECT_NAME)
	else:
		raise NotImplementedError(f"Platform '{SYSTEM}' is not supported.")


	default_download_folder = os.path.join(MEDIA_FOLDER, "download")
	default_conversion_folder = os.path.join(MEDIA_FOLDER, "convert")

	os.makedirs(CONFIG_FOLDER, exist_ok=True)
	os.makedirs(MEDIA_FOLDER, exist_ok=True)
	os.makedirs(default_download_folder, exist_ok=True)
	os.makedirs(default_conversion_folder, exist_ok=True)

	DEFAULT_SETTINGS = {
		"language": "English",
		"themeName": "Light",
		"selectedTheme": 0,
		"fontSize": 14,
		"selectedFontSize": 1,
		"defaultDownloadFolder": default_download_folder,
		"downloadPreset": "",
		"selectedDownloadPreset": 1,
		"defaultConversionFolder": default_conversion_folder,
		"conversionPreset": "",
		"selectedConversionPreset": 0,
		"deleteOriginalFile": False
	}

	SETTINGS_FILE = os.path.join(CONFIG_FOLDER, "settings.json")

	def __init__(self):
		self.settings = self.load_settings()

	def load_settings(self):
		""" Load settings from the settings file or create default settings. """
		if os.path.exists(self.SETTINGS_FILE):
			with open(self.SETTINGS_FILE, 'r', encoding='utf-8') as f:
				return json.load(f)
		else:
			return self.save_settings(self.DEFAULT_SETTINGS)

	def save_settings(self, settings=None):
		""" Save the given settings to the settings file. """
		if settings is None:
			settings = self.settings
		with open(self.SETTINGS_FILE, 'w', encoding='utf-8') as f:
			json.dump(settings, f, indent=4)
		return settings

	def reset_settings(self):
		""" Reset settings to their default values. """
		return self.save_settings(self.DEFAULT_SETTINGS.copy())

