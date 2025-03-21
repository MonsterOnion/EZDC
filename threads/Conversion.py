import os
import re
import subprocess

from PySide6.QtCore import QThread, Signal

class ConversionThread(QThread):
	progress_signal = Signal(str, int, str)
	completion_signal = Signal(str)

	def __init__(self, media_files, destination, selected_preset, conversion_preset, language, settings, delete_file):
		super().__init__()
		self.media_files = media_files
		self.destination = destination
		self.selected_preset = selected_preset
		self.conversion_preset = conversion_preset
		self.language = language
		self.settings = settings
		self.delete_file = delete_file

	def run(self):
		while self.media_files:
			input_file = self.media_files.pop(0)
			output_file = self.get_output_file(input_file)
			try:
				preset_type = self.conversion_preset[self.selected_preset].get("presetType", [])
				if preset_type == "video":
					self.convert_video(input_file, output_file)
				elif preset_type == "audio":
					self.convert_audio(input_file, output_file)

				completed_text = self.language["conversionTab"].get("complted")
				self.emit_progress(f"{completed_text}: {input_file}", 100, "completed")
				if self.delete_file:
					self.remove_file(input_file)

			except Exception as e:
				error_text = self.language["conversionTab"].get("error")
				self.emit_progress(f"{error_text}: {e}", 0, "error")

		all_completed = self.language["conversionTab"].get("allFilesConverted")
		self.completion_signal.emit(f"{all_completed} {self.destination}")

	def get_output_file(self, input_file):
		"""Generate output file name based on input file name and conversion settings."""
		preset_type = self.conversion_preset[self.selected_preset].get("presetType", [])
		filename, _ = os.path.splitext(os.path.basename(input_file))
		output_ext = self.conversion_preset[self.selected_preset].get("outputFormat", "mp4")

		if preset_type == "audio":
			bitrate_description = self.conversion_preset[self.selected_preset].get("audioBitrate", "audio")
			output_file = os.path.join(self.destination, f"{filename} - {bitrate_description}.{output_ext}")
		else:
			output_file = os.path.join(self.destination, f"{filename}.{output_ext}")
		return output_file

	def convert_video(self, input_file, output_file):
		preset = self.conversion_preset[self.selected_preset]
		width = preset.get("width", 1920)
		height = preset.get("height", 1080)
		video_codec = preset.get("videoCodec", "libx264")
		audio_codec = preset.get("audioCodec", "aac")
		video_bitrate = preset.get("videoBitrate", "5M")
		audio_bitrate = preset.get("audioBitrate", "192k")
		fps = preset.get("fps", 30)
		audio_channels = preset.get("audioChannels", 2)

		command = [
			"ffmpeg", "-y",
			"-i", input_file,
			"-vf", f"scale={width}:{height}",
			"-c:v", video_codec,
			"-b:v", video_bitrate,
			"-r", str(fps),
			"-c:a", audio_codec,
			"-b:a", audio_bitrate,
			"-ac", str(audio_channels),
			output_file
		]

		self.track_progress(command, input_file)

	def convert_audio(self, input_file, output_file):
		preset = self.conversion_preset[self.selected_preset]
		audio_codec = preset.get("audioCodec", "aac")
		audio_bitrate = preset.get("audioBitrate", "192k")
		audio_channels = preset.get("audioChannels", 2)

		command = [
			"ffmpeg", "-y",
			"-i", input_file,
			"-c:a", audio_codec,
			"-b:a", audio_bitrate,
			"-ac", str(audio_channels),
			output_file
		]

		self.track_progress(command, input_file)

	def track_progress(self, command, input_file):
		filename, file_ext = os.path.splitext(os.path.basename(input_file))
		total_duration = self.get_duration(input_file)

		creation_flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

		process = subprocess.Popen(
			command, 
			stdout=subprocess.PIPE, 
			stderr=subprocess.PIPE,
			bufsize=1,
			universal_newlines=True,
			text=True,
			encoding="utf-8",
			errors="replace",
			creationflags=creation_flags
		)

		duration_regex = re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")

		while True:
			output = process.stderr.readline()
			if not output:
				break

			match = duration_regex.search(output)
			if match:
				hours, minutes, seconds = map(float, match.groups())
				current_time = hours * 3600 + minutes * 60 + seconds
				percent = int((current_time / total_duration) * 100) if total_duration > 0 else 0
				conversion_processing = self.language["conversionTab"].get("processing")
				self.emit_progress(f"{conversion_processing}: {filename}{file_ext}, {percent}%", percent, "processing")

		process.wait()

	def get_duration(self, input_file):
		"""Retrieves total duration of the media file in seconds using FFprobe."""
		command = [
			"ffprobe", "-i", input_file, "-show_entries", "format=duration",
			"-v", "quiet", "-of", "csv=p=0"
		]
		result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		try:
			return float(result.stdout.strip())
		except ValueError:
			return 0

	def remove_file(self, input_file):
		try:
			if os.path.exists(input_file):
				os.remove(input_file)
				deleted_original = self.language["conversionTab"].get("deletedOriginal")
				self.emit_progress(f"{deleted_original}: {input_file}", 0, "deleted")
			else:
				original_not_found = self.language["conversionTab"].get("originalNotFound")
				self.emit_progress(f"{original_not_found}: {input_file}", 0, "error")
		except Exception as e:
			self.emit_progress(f"Error deleting file {input_file}: {e}", 0, "error")

	def emit_progress(self, message, percent, status):
		"""
			Emits progress updates to the connected UI components.
			Passes the message and percentage progress to the signal.
			Used for updating the UI with conversion or processing progress.
		"""
		self.progress_signal.emit(message, percent, status)
