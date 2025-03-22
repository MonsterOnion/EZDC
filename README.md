# EZDC | The essential tool for effortless media file downloads and conversions
EZDC is an easy-to-use tool designed for downloading online videos and converting media files, with accessibility in mind—particularly for blind users who rely on screen readers to operate their computers.

## Description
EZDC is designed for simplicity and ease of use, ensuring accessibility for all users, including those who use screen readers. This tool enables you to download videos from a variety of websites (see the list of supported sites on the [YT-DLP project](https://github.com/yt-dlp/yt-dlp)) and easily convert media files to popular formats such as MP3 and MP4.

The application has been translated into multiple languages to serve users worldwide. Currently supported languages include English, Spanish, French, Portuguese, Italian, German, Russian, Ukrainian, Polish, Japanese, Korean, Simplified Chinese, Traditional Chinese, and Thai. You can add more languages by editing the languages.json file located in the config folder, and creating a corresponding language content file in the assets/languages directory.

If the default presets shipped with the application don't meet your needs, you can create custom presets for both downloading and conversion by editing the preset.json file in the config folder. Just ensure that your custom presets are compatible with the arguments used by YT-DLP and FFmpeg.

## Features
EZDC offers the following features:

- ** Download videos from supported websites using the YT-DLP library.

- ** You can choose to download a single video or an entire playlist from the download tab in the application.
Instant media conversion: After downloading a video, you can select the option to convert it immediately, choose a conversion preset, and start the process.

- ** Batch conversion: The conversion tab allows you to convert multiple files at once, so you don't have to convert them one by one.

- ** Customization options: Adjust your preferences, including language, theme, font size, default download location, default conversion location, and default presets. This means you won't have to select the same preset every time you open the application.

- ** Extensibility: Users can extend the download presets, conversion presets, translations, and even custom themes. Just follow the argument formats used by YT-DLP (for download presets), FFmpeg (for conversion presets), the language file format used in the pre-packaged language files, and the QSS format for PySide6 themes.

## Installation
1. Download the ZIP file of the application.
2. Extract the contents of the ZIP file.
3. The application is ready to use!

## Development
 After cloning this repository and installing the dependencies listed in requirements.txt, you need to download the FFmpeg and FFProbe binaries separately and place them in the same directory as main.py to ensure the application works properly. The FFmpeg binary used in this project is available from [here](https://github.com/BtbN/FFmpeg-Builds/releases) or the [official page](https://www.ffmpeg.org/download.html)

## License
This project is licensed under the [Apache 2.0](LICENSE.txt)