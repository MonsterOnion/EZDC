import os
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QTextEdit, QListWidget, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QProcess

from managers.LanguageManager import LanguageManager
from managers.PresetManager import PresetManager
from managers.SettingsManager import SettingsManager
from managers.ThemeManager import ThemeManager

class SettingsTab(QWidget):

	def __init__(self, download_preset, conversion_preset, language, settings):
		super().__init__()
		self.download_ppreset = download_preset
		self.conversion_preset = conversion_preset
		self.language = language
		self.settings = settings

		self.language_manager = LanguageManager()
		self.supported_languages = self.language_manager.load_supported_languages()

		self.theme_manager = ThemeManager()
		self.supported_themes = self.theme_manager.load_supported_themes()

		# Main Layout
		main_layout = QVBoxLayout()

		# General Settings
		general_settings_box = QGroupBox(self.language["settingsTab"].get("generalSettings"))
		general_settings_layout = QVBoxLayout()

		version_layout = QHBoxLayout()
		self.version_label = QLabel(self.language["settingsTab"].get("currentVersion"))
		self.version_text = QLineEdit("1.0.0")
		self.version_text.setReadOnly(True)
		self.version_text.setAccessibleName(self.language["settingsTab"].get("currentVersion"))

		version_layout.addWidget(self.version_label)
		version_layout.addWidget(self.version_text)

		general_settings_layout.addLayout(version_layout)

		# Language, Theme and Font options
		general_options = QHBoxLayout()

		# Language
		language_layout = QVBoxLayout()
		self.language_label = QLabel(self.language["settingsTab"].get("language"))
		self.language_combo = QComboBox()
		self.language_combo.addItems(self.supported_languages.keys())
		self.language_combo.setCurrentText(self.settings["language"])
		self.language_combo.setAccessibleName(self.language["settingsTab"].get("language"))
		self.language_combo.setAccessibleDescription(self.language["settingsTab"].get("languageDescription"))
		self.language_combo.setToolTip(self.language["settingsTab"].get("languageDescription"))

		language_layout.addWidget(self.language_label)
		language_layout.addWidget(self.language_combo)

		# Theme
		theme_layout = QVBoxLayout()
		self.theme_label = QLabel(self.language["settingsTab"].get("theme"))
		self.theme_combo = QComboBox()
		self.theme_combo.addItems(self.supported_themes.keys())
		self.theme_combo.setCurrentIndex(self.settings["selectedTheme"])
		self.theme_combo.setAccessibleName(self.language["settingsTab"].get("theme"))
		self.theme_combo.setAccessibleDescription(self.language["settingsTab"].get("themeDescription"))
		self.theme_combo.setToolTip(self.language["settingsTab"].get("themeDescription"))

		theme_layout.addWidget(self.theme_label)
		theme_layout.addWidget(self.theme_combo)

		# Font Size
		FONT_SIZE = {
			"12": 12,
			"14": 14,
			"16": 16,
			"18": 18,
			"20": 20,
			"24": 24
		}

		font_size_layout = QVBoxLayout()
		self.font_size_label = QLabel("Font Size")
		self.font_size_combo = QComboBox()
		self.font_size_combo.addItems(FONT_SIZE.keys())
		self.font_size_combo.setCurrentIndex(self.settings["selectedFontSize"])
		self.font_size_combo.setAccessibleName(self.language["settingsTab"].get("fontSize"))
		self.font_size_combo.setAccessibleDescription(self.language["settingsTab"].get("fontSizeDescription"))
		self.font_size_combo.setToolTip(self.language["settingsTab"].get("fontSizeDescription"))

		font_size_layout.addWidget(self.font_size_label)
		font_size_layout.addWidget(self.font_size_combo)

		general_options.addLayout(language_layout)
		general_options.addLayout(theme_layout)
		general_options.addLayout(font_size_layout)

		general_settings_layout.addLayout(general_options)

		general_settings_box.setLayout(general_settings_layout)


		# Download Settings
		download_settings_box = QGroupBox(self.language["settingsTab"].get("downloadSettings"))
		download_settings_layout = QVBoxLayout()

		# Download Folder
		download_folder_layout = QHBoxLayout()
		self.download_label = QLabel(self.language["settingsTab"].get("downloadFolder"))
		self.download_input = QLineEdit(self.settings["defaultDownloadFolder"])
		self.download_input.setText(self.settings["defaultDownloadFolder"])
		self.download_input.setAccessibleName(self.language["settingsTab"].get("downloadFolder"))
		self.download_input.setAccessibleDescription(self.language["settingsTab"].get("downloadFolderDescription"))
		self.download_input.setToolTip(self.language["settingsTab"].get("downloadFolderDescription"))

		self.browse_download = QPushButton(self.language["settingsTab"].get("browseButton"))
		self.browse_download.setAccessibleName(self.language["settingsTab"].get("browseButton"))
		self.browse_download.setAccessibleDescription(self.language["settingsTab"].get("browseButtonDescription"))
		self.browse_download.setToolTip(self.language["settingsTab"].get("browseButtonDescription"))
		self.browse_download.clicked.connect(self.browse_download_folder)

		download_folder_layout.addWidget(self.download_label)
		download_folder_layout.addWidget(self.download_input)
		download_folder_layout.addWidget(self.browse_download)

		# Download Options
		download_options = QHBoxLayout()

		# Default Download Preset
		download_preset_layout = QVBoxLayout()
		self.download_preset_label = QLabel(self.language["settingsTab"].get("downloadPreset"))
		self.download_preset_combo = QComboBox()
		self.download_preset_combo.addItems(self.download_ppreset.keys())
		self.download_preset_combo.setCurrentIndex(self.settings["selectedDownloadPreset"])
		self.download_preset_combo.setAccessibleName(self.language["settingsTab"].get("downloadPreset"))
		self.download_preset_combo.setAccessibleDescription(self.language["settingsTab"].get("downloadPresetCombo"))
		self.download_preset_combo.setToolTip(self.language["settingsTab"].get("downloadPresetCombo"))

		download_preset_layout.addWidget(self.download_preset_label)
		download_preset_layout.addWidget(self.download_preset_combo)

		download_options.addLayout(download_preset_layout)

		download_settings_layout.addLayout(download_folder_layout)
		download_settings_layout.addLayout(download_options)

		download_settings_box.setLayout(download_settings_layout)


		# Conversion Settings
		conversion_settings_box = QGroupBox(self.language["settingsTab"].get("conversionSettings"))
		conversion_settings_layout = QVBoxLayout()

		# Conversion Folder
		conversion_folder_layout = QHBoxLayout()
		self.conversion_folder_label = QLabel(self.language["settingsTab"].get("conversionFolder"))
		self.conversion_input = QLineEdit(self.settings["defaultConversionFolder"])
		self.conversion_input.setAccessibleName(self.language["settingsTab"].get("conversionFolder"))
		self.conversion_input.setAccessibleDescription(self.language["settingsTab"].get("conversionFolderDescription"))
		self.conversion_input.setToolTip(self.language["settingsTab"].get("conversionFolderDescription"))

		self.browse_conversion = QPushButton(self.language["settingsTab"].get("browseButton"))
		self.browse_conversion.setAccessibleName(self.language["settingsTab"].get("browseButton"))
		self.browse_conversion.setAccessibleDescription(self.language["settingsTab"].get("browseButtonDescription"))
		self.browse_conversion.setToolTip(self.language["settingsTab"].get("browseButtonDescription"))
		self.browse_conversion.clicked.connect(self.browse_conversion_folder)

		conversion_folder_layout.addWidget(self.conversion_folder_label)
		conversion_folder_layout.addWidget(self.conversion_input)
		conversion_folder_layout.addWidget(self.browse_conversion)

		# Conversion Options
		conversion_options = QHBoxLayout()

		# Default Conversion Preset
		conversion_preset_layout = QVBoxLayout()
		self.conversion_preset_label = QLabel(self.language["settingsTab"].get("conversionPreset"))
		self.conversion_preset_combo = QComboBox()
		self.conversion_preset_combo.addItems(self.conversion_preset.keys())
		self.conversion_preset_combo.setCurrentIndex(self.settings["selectedConversionPreset"])
		self.conversion_preset_combo.setAccessibleName(self.language["settingsTab"].get("conversionPreset"))
		self.conversion_preset_combo.setAccessibleDescription(self.language["settingsTab"].get("conversionPresetCombo"))
		self.conversion_preset_combo.setToolTip(self.language["settingsTab"].get("conversionPresetCombo"))

		conversion_preset_layout.addWidget(self.conversion_preset_label)
		conversion_preset_layout.addWidget(self.conversion_preset_combo)

		conversion_options.addLayout(conversion_preset_layout)

		# More Conversion Settings
		more_conversion_layout = QHBoxLayout()
		self.delete_original_check = QCheckBox(self.language["settingsTab"].get("deleteOriginal"))
		self.delete_original_check.setAccessibleName(self.language["settingsTab"].get("deleteOriginal"))
		self.delete_original_check.setAccessibleDescription(self.language["settingsTab"].get("deleteOriginalDescription"))
		self.delete_original_check.setToolTip(self.language["settingsTab"].get("deleteOriginalDescription"))
		self.delete_original_check.setChecked(self.settings["deleteOriginalFile"])

		more_conversion_layout.addWidget(self.delete_original_check)

		conversion_settings_layout.addLayout(conversion_folder_layout)
		conversion_settings_layout.addLayout(conversion_options)
		conversion_settings_layout.addLayout(more_conversion_layout)

		conversion_settings_box.setLayout(conversion_settings_layout)

		# Save and Reset Button
		button_layout = QHBoxLayout()

		self.save_button = QPushButton(self.language["settingsTab"].get("saveButton"))
		self.save_button.setAccessibleName(self.language["settingsTab"].get("saveButton"))
		self.save_button.setAccessibleDescription(self.language["settingsTab"].get("saveButtonDescription"))
		self.save_button.setToolTip(self.language["settingsTab"].get("saveButtonDescription"))
		self.save_button.clicked.connect(self.save_settings)

		self.reset_button = QPushButton(self.language["settingsTab"].get("resetButton"))
		self.reset_button.setAccessibleName(self.language["settingsTab"].get("resetButton"))
		self.reset_button.setAccessibleDescription(self.language["settingsTab"].get("resetButtonDescription"))
		self.reset_button.setToolTip(self.language["settingsTab"].get("resetButtonDescription"))
		self.reset_button.clicked.connect(self.reset_settings)

		button_layout.addWidget(self.reset_button)
		button_layout.addStretch()
		button_layout.addWidget(self.save_button)


		# Set Layout
		main_layout.addWidget(general_settings_box)
		main_layout.addWidget(download_settings_box)
		main_layout.addWidget(conversion_settings_box)
		main_layout.addLayout(button_layout)

		main_layout.setContentsMargins(10, 10, 10, 10)
		main_layout.setSpacing(15)
		self.setLayout(main_layout)



	# Class Method
	def browse_download_folder(self):
		"""
			Opens a dialog to select a destination folder for default downloaded folder and updates the destination input field.
			This method displays a QFileDialog to allow the user to select a folder.
			If a folder is selected, the path is normalized to match the current operating system's path format (e.g., backslashes on Windows) and set in the destination input field.
		"""
		folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
		if folder:
			normalize_path = os.path.normpath(folder)
			self.download_input.setText(normalize_path)

	def browse_conversion_folder(self):
		"""
			Opens a dialog to select a destination folder for default conversion folder and updates the destination input field.
			This method displays a QFileDialog to allow the user to select a folder.
			If a folder is selected, the path is normalized to match the current operating system's path format (e.g., backslashes on Windows) and set in the destination input field.
		"""
		folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
		if folder:
			normalize_path = os.path.normpath(folder)
			self.conversion_input.setText(normalize_path)

	def reset_settings(self):
		""" Reset all settings to default values. """
		settings_manager = SettingsManager()
		default_settings = settings_manager.DEFAULT_SETTINGS

		self.language_combo.setCurrentText(default_settings["language"])
		self.theme_combo.setCurrentIndex(default_settings["selectedTheme"])
		self.font_size_combo.setCurrentIndex(default_settings["selectedFontSize"])
		self.download_input.setText(default_settings["defaultDownloadFolder"])
		self.download_preset_combo.setCurrentIndex(default_settings["selectedDownloadPreset"])
		self.conversion_input.setText(default_settings["defaultConversionFolder"])
		self.conversion_preset_combo.setCurrentIndex(default_settings["selectedConversionPreset"])
		self.delete_original_check.setChecked(default_settings["deleteOriginalFile"])

		settings_manager.reset_settings()
		alert_title = self.language["settingsTab"].get("resetAlertTitle")
		alert_message = self.language["settingsTab"].get("resetAlertMessage")
		QMessageBox.information(self, alert_title, alert_message)

		QApplication.instance().quit()
		QProcess.startDetached(sys.executable, sys.argv)

	def save_settings(self):
		"""Save the current settings and notify the user."""
		settings_manager = SettingsManager()

		new_settings = {
			"language": self.language_combo.currentText(),
			"themeName": self.theme_combo.currentText(),
			"selectedTheme": self.theme_combo.currentIndex(),
			"fontSize": self.font_size_combo.currentText(),
			"selectedFontSize": self.font_size_combo.currentIndex(),
			"defaultDownloadFolder": self.download_input.text(),
			"downloadPreset": self.download_preset_combo.currentText(),
			"selectedDownloadPreset": self.download_preset_combo.currentIndex(),
			"defaultConversionFolder": self.conversion_input.text(),
			"conversionPreset": self.conversion_preset_combo.currentText(),
			"selectedConversionPreset": self.conversion_preset_combo.currentIndex(),
			"deleteOriginalFile": self.delete_original_check.isChecked()
		}

		settings_manager.save_settings(new_settings)
		alert_title = self.language["settingsTab"].get("saveAlertTitle")
		alert_message = self.language["settingsTab"].get("saveAlertMessage")
		QMessageBox.information(self, alert_title, alert_message)

		QApplication.instance().quit()
		QProcess.startDetached(sys.executable, sys.argv)