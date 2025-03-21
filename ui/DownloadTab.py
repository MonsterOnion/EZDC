import os
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QTextEdit, QProgressBar, QFileDialog
from PySide6.QtCore import Qt, Slot

from threads.Download import DownloadThread
from threads.Conversion import ConversionThread

class DownloadTab(QWidget):
	update_progress = Slot(str, int, str)

	def __init__(self, download_preset, conversion_preset, language, settings):
		super().__init__()
		self.download_preset = download_preset
		self.conversion_preset = conversion_preset
		self.language = language
		self.settings = settings
		self.download_thread = None
		self.conversion_thread = None

		# Main Layout
		main_layout = QVBoxLayout()

		# Top Frame Section
		top_frame = QFrame()
		top_frame.setFrameShape(QFrame.Panel)
		top_frame.setFrameShadow(QFrame.Plain)
		top_frame.setLineWidth(2)

		top_frame_layout = QVBoxLayout(top_frame)

		# URL Section
		url_layout = QHBoxLayout()
		self.url_label = QLabel("URL:")
		self.url_input = QLineEdit()
		self.url_input.setAccessibleName("URL:")
		self.url_input.setAccessibleDescription(self.language["downloadTab"].get("urlDescription"))
		self.url_input.setToolTip(self.language["downloadTab"].get("urlDescription"))

		self.clear_button = QPushButton(self.language["downloadTab"].get("clearButton"))
		self.clear_button.setAccessibleName(self.language["downloadTab"].get("clearButton"))
		self.clear_button.setAccessibleDescription(self.language["downloadTab"].get("clearButtonDescription"))
		self.clear_button.setToolTip(self.language["downloadTab"].get("clearButtonDescription"))
		self.clear_button.clicked.connect(self.clear_url)

		url_layout.addWidget(self.url_label)
		url_layout.addWidget(self.url_input)
		url_layout.addWidget(self.clear_button)

		top_frame_layout.addLayout(url_layout)

		# Destination Folder Section
		dest_layout = QHBoxLayout()
		self.dest_label = QLabel(self.language["downloadTab"].get("destLabel"))
		self.dest_input = QLineEdit(self.settings["defaultDownloadFolder"])
		self.dest_input.setAccessibleName(self.language["downloadTab"].get("destLabel"))
		self.dest_input.setAccessibleDescription(self.language["downloadTab"].get("destDescription"))
		self.dest_input.setToolTip(self.language["downloadTab"].get("destDescription"))

		self.browse_button = QPushButton(self.language["downloadTab"].get("browseButton"))
		self.browse_button.setAccessibleName(self.language["downloadTab"].get("browseButton"))
		self.browse_button.setAccessibleDescription(self.language["downloadTab"].get("browseButtonDescription"))
		self.browse_button.setToolTip(self.language["downloadTab"].get("browseButtonDescription"))
		self.browse_button.clicked.connect(self.browse_folder)

		dest_layout.addWidget(self.dest_label)
		dest_layout.addWidget(self.dest_input)
		dest_layout.addWidget(self.browse_button)

		top_frame_layout.addLayout(dest_layout)

		# Download Options
		options_layout = QHBoxLayout()

		check_options = QVBoxLayout()
		self.playlist_check = QCheckBox(self.language["downloadTab"].get("playlistCheck"))
		self.playlist_check.setAccessibleDescription(self.language["downloadTab"].get("playlistCheckDescription"))
		self.playlist_check.setToolTip(self.language["downloadTab"].get("playlistCheckDescription"))
		self.conversion_check = QCheckBox(self.language["downloadTab"].get("conversionCheck"))
		self.conversion_check.setAccessibleDescription(self.language["downloadTab"].get("conversionCheckDescription"))
		self.conversion_check.setToolTip(self.language["downloadTab"].get("conversionCheckDescription"))
		self.conversion_check.toggled.connect(self.on_conversion_checked)

		check_options.addWidget(self.playlist_check)
		check_options.addWidget(self.conversion_check)

		preset_options = QVBoxLayout()
		self.preset_label = QLabel(self.language["downloadTab"].get("downloadLabel"))
		self.preset_combo = QComboBox()
		self.preset_combo.addItems(self.download_preset.keys())
		self.preset_combo.setCurrentIndex(self.settings["selectedDownloadPreset"])
		self.preset_combo.setAccessibleName(self.language["downloadTab"].get("downloadLabel"))
		self.preset_combo.setAccessibleDescription(self.language["downloadTab"].get("downloadComboDescription"))
		self.preset_combo.setToolTip(self.language["downloadTab"].get("downloadComboDescription"))
		self.preset_combo.currentTextChanged.connect(self.on_preset_change)

		self.selected_download = ""
		self.selected_conversion = ""

		preset_options.addWidget(self.preset_label)
		preset_options.addWidget(self.preset_combo)

		options_layout.addStretch()
		options_layout.addLayout(check_options)
		options_layout.addStretch()
		options_layout.addLayout(preset_options)
		options_layout.addStretch()

		top_frame_layout.addLayout(options_layout)

		#top_frame_layout.addLayout(more_options)

		# Bottom frame Section
		bottom_frame = QFrame()
		bottom_frame.setFrameShape(QFrame.Panel)
		bottom_frame.setFrameShadow(QFrame.Plain)
		bottom_frame.setLineWidth(2)

		bottom_frame_layout = QVBoxLayout(bottom_frame)

		# Download Status and Download Button Section
		download_layout = QHBoxLayout()

		button_layout = QVBoxLayout()
		self.download_button = QPushButton(self.language["downloadTab"].get("downloadButton"))
		self.download_button.setAccessibleName(self.language["downloadTab"].get("downloadButton"))
		self.download_button.setAccessibleDescription(self.language["downloadTab"].get("downloadButtonDescription"))
		self.download_button.setToolTip(self.language["downloadTab"].get("downloadButtonDescription"))
		self.download_button.clicked.connect(self.download)
		button_layout.addWidget(self.download_button, alignment=Qt.AlignCenter)

		log_layout = QVBoxLayout()
		self.log_label = QLabel(self.language["downloadTab"].get("logLabel"))
		self.log_output = QTextEdit()
		self.log_output.setReadOnly(True)
		self.log_output.setAccessibleName(self.language["downloadTab"].get("logLabel"))
		self.log_output.setAccessibleDescription(self.language["downloadTab"].get("logDescription"))
		self.log_output.setToolTip(self.language["downloadTab"].get("logDescription"))

		log_layout.addWidget(self.log_label)
		log_layout.addWidget(self.log_output)

		log_layout.setStretch(0, 0)
		log_layout.setStretch(1, 1)

		download_layout.addLayout(button_layout)
		download_layout.addStretch()
		download_layout.addLayout(log_layout)

		bottom_frame_layout.addLayout(download_layout)

		# Progress Bar
		progress_bar_layout = QHBoxLayout()
		self.progress_bar = QProgressBar()
		self.progress_bar.setMinimum(0)
		self.progress_bar.setMaximum(100)
		progress_bar_layout.addWidget(self.progress_bar)



		# Set Layout
		main_layout.addWidget(top_frame)
		main_layout.addWidget(bottom_frame)
		main_layout.addLayout(progress_bar_layout)

		main_layout.setContentsMargins(10, 10, 10, 10)
		main_layout.setSpacing(15)
		self.setLayout(main_layout)



	# Class Method
	def clear_url(self):
		"""
			Clears the text in the URL input field.
		"""
		self.url_input.clear()

	def browse_folder(self):
		"""
			Opens a dialog to select a destination folder and updates the destination input field.
			This method displays a QFileDialog to allow the user to select a folder.
			If a folder is selected, the path is normalized to match the current operating system's path format (e.g., backslashes on Windows) and set in the destination input field.
		"""
		folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
		if folder:
			normalize_path = os.path.normpath(folder)
			self.dest_input.setText(normalize_path)

	def on_conversion_checked(self):
		""" The function to change the label and loop preset options base on the conversion check box. """
		if self.conversion_check.isChecked():
			self.preset_combo.clear()
			self.preset_combo.addItems(self.conversion_preset.keys())
			self.preset_combo.setCurrentText(self.selected_conversion)

			self.preset_label.setText(self.language["downloadTab"].get("conversionLabel"))
			self.preset_combo.setAccessibleName(self.language["downloadTab"].get("conversionLabel"))
			self.preset_combo.setAccessibleDescription(self.language["downloadTab"].get("conversionComboDescription"))
			self.preset_combo.setToolTip(self.language["downloadTab"].get("conversionComboDescription"))
		else:
			self.preset_combo.clear()
			self.preset_combo.addItems(self.download_preset.keys())
			self.preset_combo.setCurrentText(self.selected_download)

			self.preset_label.setText(self.language["downloadTab"].get("downloadLabel"))
			self.preset_combo.setAccessibleName(self.language["downloadTab"].get("downloadLabel"))
			self.preset_combo.setAccessibleDescription(self.language["downloadTab"].get("downloadComboDescription"))
			self.preset_combo.setToolTip(self.language["downloadTab"].get("downloadComboDescription"))

	def on_preset_change(self):
		if self.conversion_check.isChecked():
			self.selected_conversion = self.preset_combo.currentText()
			print(f"conversion preset is: {self.selected_conversion}")
		else:
			self.selected_download = self.preset_combo.currentText()
			print(f"download preset is: {self.selected_download}")

	def download(self):
		"""
			Starts the download process by creating a DownloadThread with user inputs.
			Connects thread signals for progress updates and completion handling.
			Disables the download button and updates its text while the download runs.
		"""
		url = self.url_input.text()
		destination = self.dest_input.text()
		playlist = self.playlist_check.isChecked()
		conversion = self.conversion_check.isChecked()
		selected_preset = self.selected_download

		self.download_thread = DownloadThread(
			url, 
			destination, 
			playlist,
			conversion,
			selected_preset,
			self.download_preset, 
			self.language, 
			self.settings
			)

		self.download_thread.progress_signal.connect(self.update_progress)
		self.download_thread.conversion_signal.connect(self.start_conversion)
		self.download_thread.completion_signal.connect(self.display_completion_message)
		self.download_thread.finished.connect(self.download_finished)

		self.preset_combo.setEnabled(False)
		self.download_button.setEnabled(False)
		self.download_button.setText(self.language["downloadTab"].get("inProgressDownloadButton"))
		self.download_button.setAccessibleName(self.language["downloadTab"].get("inProgressDownloadButton"))
		self.download_button.setAccessibleDescription(self.language["downloadTab"].get("inProgressDownloadDescription"))
		self.download_button.setToolTip(self.language["downloadTab"].get("inProgressDownloadDescription"))

		self.log_output.append(self.language["downloadTab"].get("startingDownload"))
		self.download_thread.start()

	def start_conversion(self, downloaded_files):
		destination = self.dest_input.text()
		option = self.conversion_check.isChecked()
		selected_preset = self.selected_conversion

		self.conversion_thread = ConversionThread(
			downloaded_files,
			destination,
			selected_preset,
			self.conversion_preset,
			self.language,
			self.settings,
			option
		)

		self.conversion_thread.progress_signal.connect(self.update_progress)
		self.conversion_thread.completion_signal.connect(self.display_completion_message)
		self.conversion_thread.start()

	def display_completion_message(self, message):
		"""Handles the final completion message and updates the log UI."""
		self.log_output.append(message)

	def download_finished(self):
		"""
			Handles post-download cleanup and resets the download button.
		"""
		self.preset_combo.setEnabled(True)
		self.download_button.setEnabled(True)
		self.download_button.setText(self.language["downloadTab"].get("downloadButton"))
		self.download_button.setAccessibleName(self.language["downloadTab"].get("downloadButton"))
		self.download_button.setAccessibleDescription(self.language["downloadTab"].get("downloadButtonDescription"))
		self.download_button.setToolTip(self.language["downloadTab"].get("downloadButtonDescription"))

		self.download_thread = None

	def stop_download(self):
		"""
			Stops the ongoing download by terminating the download thread if it's running.
			Ensures the thread is properly terminated and resources are released.
			Prepares the application for a clean state after stopping the download.
		"""
		if self.download_thread and self.download_thread.isRunning():
			self.download_thread.terminate()
			self.download_thread.wait()
			self.download_thread = None

	@Slot(str, int, str)
	def update_progress(self, message, percent, status):
		"""
			Updates the download progress by displaying the message and setting the progress bar value.
			Clears the log and resets the progress bar if the status is not 'downloading'.
		"""
		if status != 'downloading' and status != "processing":
			self.log_output.clear()
			self.progress_bar.setValue(0)

		self.log_output.append(message)
		self.progress_bar.setValue(percent)
