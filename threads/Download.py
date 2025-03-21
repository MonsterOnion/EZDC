import os
import yt_dlp

from PySide6.QtCore import QThread, Signal

class DownloadThread(QThread):
	progress_signal = Signal(str, int, str)
	conversion_signal = Signal(list)
	completion_signal = Signal(str)

	def __init__(self, url, destination, playlist, conversion, selected_preset, download_preset, language, settings):
		super().__init__()
		self.url = url
		self.destination = destination
		self.playlist = playlist
		self.conversion = conversion
		self.selected_preset = selected_preset
		self.download_preset = download_preset
		self.language = language
		self.settings = settings

		self.total_video = 0
		self.downloaded_video = 0

		self.downloaded_files = []

	def run(self):
		"""
			Executes the download process, emitting progress updates and handling exceptions.
			Displays a success message upon completion or an error message if the download fails.
			Updates the status based on whether a single video or an entire playlist was downloaded.
		"""
		try:
			ydl_opts = self.get_download_options()
			self.download_video(ydl_opts)
		except Exception as e:
			error_message = self.language["downloadTab"].get("errorMessage")
			self.emit_progress(f"{error_message}: {e}", 0, "error")

		if self.playlist and self.downloaded_video == self.total_video:
			message = self.language["downloadTab"].get("playlistDownloadFinished")
			self.completion_signal.emit(f"{message}: {self.destination}")
		elif not self.playlist:
			message = self.language["downloadTab"].get("singleDownloadFinished")
			self.completion_signal.emit(f"{message}: {self.destination}")

		if self.conversion:
			if self.downloaded_files:
				message = self.language["downloadTab"].get("startingConversion")
				self.emit_progress(message, 100, "conversion")
				self.conversion_signal.emit(self.downloaded_files)
		else:
			self.downloaded_files.clear()

	def download_video(self, ydl_opts):
		"""
			Downloads the video using yt-dlp with the provided download options.
		"""
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			ydl.download([self.url])

	def get_download_options(self):
		"""
			Retrieves the download options for yt-dlp based on the URL and user settings.
			Constructs the save path, selects the download quality, and configures the options.
			Returns a dictionary with the configured yt-dlp options for video download.
		"""
		with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
			info = ydl.extract_info(self.url, download=False)

			if 'entries' in info:
				self.total_video = len(info['entries'])
				playlist_title = info.get('title', 'unknown_playlist')
				self.save_path = os.path.join(self.destination, playlist_title, "%(playlist_index)s. %(title)s.%(ext)s")
			else:
				video_title = info.get('title', 'unknown_title')
				self.save_path = os.path.join(self.destination, f"{video_title}.%(ext)s")

		selected_preset = self.download_preset[self.selected_preset]
		default_download = "bestvideo[height<=1080]+bestaudio/best"
		format_choice = selected_preset.get("format", default_download)
		output_format = selected_preset.get("outputFormat", "webm")

		download_options = {
			'format': format_choice,
			'outtmpl': self.save_path,
			'progress_hooks': [self.progress_hook],
			'noplaylist': not self.playlist,
			'rm_temp_files': True,
		}

		if selected_preset.get("downloadSubtitles", False):
			download_options.update({
				'writesubtitles': True,
				'embedsubtitles': selected_preset.get("embedsubtitles", False),
				'allsubtitles': selected_preset.get("allSubtitles", False),
				'subtitleslangs': None if selected_preset.get("allSubtitles", False) else ["en"]
			})

		return download_options

	def progress_hook(self, d):
		"""
			Processes the download progress and updates the UI with status, speed, and ETA.
			Handles different download statuses (downloading, finished) and formats the message.
			Emits progress updates to the UI through the `emit_progress` method.
		"""
		current_status = d['status'] 

		if current_status == 'downloading':
			self.percent_str = d.get('_percent_str', '').replace('\x1b[0;94m', '').replace('\x1b[0m', '')
			self.percent_str = self.percent_str.strip()
			self.percent_int = 0

			if self.percent_str and self.percent_str.endswith('%'):
				self.percent_int = int(float(self.percent_str[:-1].strip()))
			else:
				percent_int = 0

			self.speed = d.get('_speed_str', '').replace('\x1b[0;32m', '').replace('\x1b[0m', '')
			self.eta = d.get('_eta_str', '').replace('\x1b[0;33m', '').replace('\x1b[0m', '')

			video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv')
			audio_extensions = ('.mp3', '.wav', '.flac', '.aac', '.ogg', '.aiff', '.webm')
			subtitle_extensions = ('.ass', '.srt', '.sub', '.vtt')
			if d['filename'].endswith(video_extensions):
				self.file_type = self.language["downloadTab"].get("video")
			elif d['filename'].endswith(subtitle_extensions):
				self.file_type = self.language["downloadTab"].get("subtitle")
			else:
				self.file_type = self.language["downloadTab"].get("audio")

			downloading_message = self.language["downloadTab"].get("downloading")
			message = downloading_message.format(file_type=self.file_type,
				percent_str=self.percent_str,
				speed=self.speed,
				eta=self.eta
				)
			self.emit_progress(message, self.percent_int, current_status)

		elif current_status == 'finished':
			file_path = d.get('filename')
			if file_path and file_path not in self.downloaded_files:
				self.downloaded_files.append(file_path)
			if self.playlist and '.webm' in d['filename']:
				self.downloaded_video += 1
				complete_text = self.language["downloadTab"].get("playlistCompleted")
				message = complete_text.format(downloaded_video=self.downloaded_video, total_video=self.total_video)
				self.emit_progress(message, 100, "finished")
			else:
				message = self.language["downloadTab"].get("merging")
				self.emit_progress(message, 100, "merging")

	def emit_progress(self, message, percent, status):
		"""
			Emits progress updates to the connected UI components.
			Passes the message, percentage progress, and current status to the signal.
			Used for updating the UI with download or processing progress.
		"""
		self.progress_signal.emit(message, percent, status)
