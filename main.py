import os
import sys
import subprocess

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PySide6.QtGui import QFont
from ui.DownloadTab import DownloadTab
from ui.ConversionTab import ConversionTab
from ui.SettingsTab import SettingsTab

from managers.LanguageManager import LanguageManager
from managers.PresetManager import PresetManager
from managers.SettingsManager import SettingsManager
from managers.ThemeManager import ThemeManager

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.settings_manager = SettingsManager()
		self.settings = self.settings_manager.load_settings()

		self.language_manager = LanguageManager()
		self.language = self.language_manager.load_language(self.settings["language"])

		self.preset_manager = PresetManager()
		self.download_preset = self.preset_manager.load_download_preset()
		self.conversion_preset = self.preset_manager.load_conversion_preset()

		self.setWindowTitle(self.language["windowTitle"])
		self.setGeometry(100, 100, 500, 400)

		self.tab_widget = QTabWidget()
		self.tab_widget.setTabPosition(QTabWidget.North)
		self.tab_widget.setMovable(False)

		self.download_tab = DownloadTab(self.download_preset, self.conversion_preset, self.language, self.settings)
		self.conversion_tab = ConversionTab(self.conversion_preset, self.language, self.settings)
		self.settings_tab = SettingsTab(self.download_preset, self.conversion_preset, self.language, self.settings)

		self.tab_widget.addTab(self.download_tab, self.language["downloadTab"].get("title"))
		self.tab_widget.addTab(self.conversion_tab, self.language["conversionTab"].get("title"))
		self.tab_widget.addTab(self.settings_tab, self.language["settingsTab"].get("title"))

		self.setCentralWidget(self.tab_widget)



app = QApplication(sys.argv)

settings_manager = SettingsManager()
settings = settings_manager.load_settings()

theme_manager = ThemeManager()
theme_name = settings["themeName"]
theme_stylesheet = theme_manager.load_theme(theme_name)
if theme_stylesheet:
	app.setStyleSheet(theme_stylesheet)  # Apply theme to the entire application

font_size = int(settings.get("fontSize", 12))
app.setFont(QFont("Arial", font_size))

window = MainWindow()
window.show()
app.exec()