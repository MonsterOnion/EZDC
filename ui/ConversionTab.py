import os
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QLineEdit, QPushButton, QCheckBox, QComboBox, QTextEdit, QProgressBar, QFileDialog, QMenu
from PySide6.QtCore import Qt, Slot

from threads.Conversion import ConversionThread

class ConversionTab(QWidget):
	update_progress = Slot(str, int, str)

	def __init__(self, conversion_preset, language, settings):
		super().__init__()
		self.conversion_preset = conversion_preset
		self.language = language
		self.settings = settings
		self.conversion_thread = None

		# Main Layout
		main_layout = QHBoxLayout()

		# Left Frame Section
		left_frame = QFrame()
		left_frame.setFrameShape(QFrame.Panel)
		left_frame.setFrameShadow(QFrame.Plain)
		left_frame.setLineWidth(2)

		left_frame_layout = QVBoxLayout(left_frame)

		# File List Section
		list_layout = QVBoxLayout()
		list_label = QLabel(self.language["conversionTab"].get("fileList"))
		self.file_list = QListWidget()

		list_layout.addWidget(list_label)
		list_layout.addWidget(self.file_list)
		list_layout.setStretch(0, 0)
		list_layout.setStretch(1, 1)

		left_frame_layout.addLayout(list_layout)

		# Right frame Section
		right_frame = QFrame()
		right_frame.setFrameShape(QFrame.Panel)
		right_frame.setFrameShadow(QFrame.Plain)
		right_frame.setLineWidth(2)

		right_frame_layout = QVBoxLayout(right_frame)

		# Add and Remove Buttons Section
		button_layout = QHBoxLayout()
		self.add_button = QPushButton(self.language["conversionTab"].get("addButton"))
		self.add_button.setAccessibleName(self.language["conversionTab"].get("addButton"))
		self.add_button.setAccessibleDescription(self.language["conversionTab"].get("addButtonDescription"))
		self.add_button.setToolTip(self.language["conversionTab"].get("addButtonDescription"))
		self.add_button.clicked.connect(self.add_files)

		self.remove_button = QPushButton(self.language["conversionTab"].get("removeButton"))
		self.remove_button.setAccessibleName(self.language["conversionTab"].get("removeButton"))
		self.remove_button.setAccessibleDescription(self.language["conversionTab"].get("removeButtonDescription"))
		self.remove_button.setToolTip(self.language["conversionTab"].get("removeButtonDescription"))
		self.remove_button.clicked.connect(self.show_remove_menu)

		button_layout.addWidget(self.add_button)
		button_layout.addWidget(self.remove_button)

		right_frame_layout.addLayout(button_layout)

		# Destination Section
		dest_layout = QHBoxLayout()
		self.dest_label = QLabel(self.language["conversionTab"].get("destLabel"))
		self.dest_input = QLineEdit(self.settings["defaultConversionFolder"])
		self.dest_input.setAccessibleName(self.language["conversionTab"].get("destLabel"))
		self.dest_input.setAccessibleDescription(self.language["conversionTab"].get("destDescription"))
		self.dest_input.setToolTip(self.language["conversionTab"].get("destDescription"))

		self.browse_button = QPushButton(self.language["conversionTab"].get("browseButton"))
		self.browse_button.setAccessibleName(self.language["conversionTab"].get("browseButton"))
		self.browse_button.setAccessibleDescription(self.language["conversionTab"].get("browseButtonDescription"))
		self.browse_button.setToolTip(self.language["conversionTab"].get("browseButtonDescription"))
		self.browse_button.clicked.connect(self.browse_folder)

		dest_layout.addWidget(self.dest_label)
		dest_layout.addWidget(self.dest_input)
		dest_layout.addWidget(self.browse_button)

		right_frame_layout.addLayout(dest_layout)

		# Preset Options
		options_layout = QVBoxLayout()

		preset_options = QVBoxLayout()
		self.preset_label = QLabel(self.language["conversionTab"].get("conversionLabel"))
		self.preset_combo = QComboBox()
		self.preset_combo.addItems(self.conversion_preset.keys())
		self.preset_combo.setCurrentIndex(self.settings["selectedConversionPreset"])
		self.preset_combo.setAccessibleName(self.language["conversionTab"].get("conversionLabel"))
		self.preset_combo.setAccessibleDescription(self.language["conversionTab"].get("conversionComboDescription"))
		self.preset_combo.setToolTip(self.language["conversionTab"].get("conversionComboDescription"))

		preset_options.addWidget(self.preset_label)
		preset_options.addWidget(self.preset_combo)

		options_layout.addLayout(preset_options)
		#options_layout.addLayout(more_layout)

		right_frame_layout.addLayout(options_layout)

		# Convert Button Section
		conversion_layout = QHBoxLayout()
		self.convert_button = QPushButton(self.language["conversionTab"].get("convertButton"))
		self.convert_button.setAccessibleName(self.language["conversionTab"].get("convertButton"))
		self.convert_button.setAccessibleDescription(self.language["conversionTab"].get("convertButtonDescription"))
		self.convert_button.setToolTip(self.language["conversionTab"].get("convertButtonDescription"))
		self.convert_button.clicked.connect(self.convert_file)
		conversion_layout.addWidget(self.convert_button, alignment=Qt.AlignCenter)

		right_frame_layout.addLayout(conversion_layout)

		# Log Section
		log_layout = QVBoxLayout()
		self.log_label = QLabel(self.language["conversionTab"].get("logLabel"))
		self.log_output = QTextEdit()
		self.log_output.setReadOnly(True)
		self.log_output.setAccessibleName(self.language["conversionTab"].get("logLabel"))
		self.log_output.setAccessibleDescription(self.language["conversionTab"].get("logDescription"))
		self.log_output.setToolTip(self.language["conversionTab"].get("logDescription"))

		log_layout.addWidget(self.log_label)
		log_layout.addWidget(self.log_output)

		log_layout.setStretch(0, 0)
		log_layout.setStretch(1, 1)

		right_frame_layout.addLayout(log_layout)

		# Progress Bar
		progress_bar_layout = QHBoxLayout()
		self.progress_bar = QProgressBar()
		self.progress_bar.setMinimum(0)
		self.progress_bar.setMaximum(100)
		progress_bar_layout.addWidget(self.progress_bar)



		# Set Layout
		main_layout.addWidget(left_frame)
		main_layout.addWidget(right_frame)

		main_layout.setStretch(0, 1)
		main_layout.setStretch(1, 2)

		main_layout.addLayout(progress_bar_layout)

		main_layout.setContentsMargins(10, 10, 10, 10)
		main_layout.setSpacing(15)
		self.setLayout(main_layout)



	# Class Method
	def add_files(self):
		"""
			Open a file dialog to allow the user to select one or more files. 
			Normalize the file paths for cross-platform compatibility. 
			Add the normalized paths to the file list widget.
		"""
		file_filter = "Media Files (*.mp3 *.mp4 *.avi *.wav *.mkv *.flv *.mov *.webm);;All Files (*)"

		files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", file_filter)
		if files:
			for file in files:
				normalize_path = os.path.normpath(file)
				self.file_list.addItem(normalize_path)

	def show_remove_menu(self):
		"""
			Shows a context menu with options to remove selected item or all items.
		"""
		context_menu = QMenu(self.remove_button)
		context_menu.setAccessibleName("Context Menu")

		remove_selected_action = context_menu.addAction(self.language["conversionTab"].get("removeSelectedFile"))
		remove_selected_action.triggered.connect(self.remove_selected_item)

		remove_all_action = context_menu.addAction(self.language["conversionTab"].get("removeAllFiles"))
		remove_all_action.triggered.connect(self.remove_all_items)

		context_menu.exec_(self.remove_button.mapToGlobal(self.remove_button.pos()))

	def remove_selected_item(self):
		"""
			Removes the selected item from the list.
		"""
		selected_items = self.file_list.selectedItems()
		if selected_items:
			for item in selected_items:
				row = self.file_list.row(item)
				self.file_list.takeItem(row)

	def remove_all_items(self):
		"""
			Removes all items from the list.
		"""
		self.file_list.clear()

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

	def convert_file(self):
		self.media_files = []
		destination = self.dest_input.text().strip()
		selected_preset = self.preset_combo.currentText()
		delete_file = self.settings["deleteOriginalFile"]

		for index in range(self.file_list.count()):
			file = self.file_list.item(index)
			self.media_files.append(file.text())

		self.conversion_thread = ConversionThread(
			self.media_files,
			destination,
			selected_preset,
			self.conversion_preset,
			self.language,
			self.settings,
			delete_file
		)

		self.conversion_thread.progress_signal.connect(self.update_progress)
		self.conversion_thread.completion_signal.connect(self.display_completion_message)
		self.conversion_thread.finished.connect(self.conversion_finished)

		self.add_button.setEnabled(False)
		self.remove_button.setEnabled(False)

		self.preset_combo.setEnabled(False)

		self.convert_button.setEnabled(False)
		self.convert_button.setText(self.language["conversionTab"].get("inProgressConvertButton"))
		self.convert_button.setAccessibleName(self.language["conversionTab"].get("inProgressConvertButton"))
		self.convert_button.setAccessibleDescription(self.language["conversionTab"].get("inProgressConvertDescription"))
		self.convert_button.setToolTip(self.language["conversionTab"].get("inProgressConvertDescription"))

		self.log_output.append("Preparing conversion process")
		self.conversion_thread.start()

	def display_completion_message(self, message):
		self.log_output.append(message)

	def conversion_finished(self):
		"""
			Handles post-conversion cleanup and resets the convert button.
		"""
		self.file_list.clear()
		self.media_files.clear()

		self.add_button.setEnabled(True)
		self.remove_button.setEnabled(True)

		self.preset_combo.setEnabled(True)

		self.convert_button.setEnabled(True)
		self.convert_button.setText(self.language["conversionTab"].get("convertButton"))
		self.convert_button.setAccessibleName(self.language["conversionTab"].get("convertButton"))
		self.convert_button.setAccessibleDescription(self.language["conversionTab"].get("convertButtonDescription"))
		self.convert_button.setToolTip(self.language["conversionTab"].get("convertButtonDescription"))

		self.conversion_thread = None

	def stop_conversion(self):
		"""
			Stops the ongoing conversion by terminating the conversion thread if it's running.
			Ensures the thread is properly terminated and resources are released.
			Prepares the application for a clean state after stopping the conversion.
		"""
		if self.conversion_thread and self.conversion_thread.isRunning():
			self.conversion_thread.terminate()
			self.conversion_thread.wait()
			self.conversion_thread = None

	@Slot(str, int, str)
	def update_progress(self, message, percent, status):
		if status != "processing":
			self.log_output.clear()
			self.progress_bar.setValue(0)

		self.log_output.append(message)
		self.progress_bar.setValue(percent)