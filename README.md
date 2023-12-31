
# Auto-YouTube

Python code for creating automated YouTube shorts and videos with real-time news, including audio, video, and subtitles – all without any manual work.

## Features

- **Content Generation:** Fetch content from various sources, such as ChatGPT or other APIs.

- **Audio Generation:** Utilize Amazon Polly for Text-to-Speech (TTS) to generate audio content.

- **Video Generation:** Use MoviePy in Python to create videos.

- **Uploading:** Automatically upload finished videos to YouTube.

## Getting Started

To get started with Auto-YouTube, follow these steps:

1. Configure the `const.py` files in the `utilities` directories.

2. Run the `yt_auto_main.py` script.

### Configuration

- Before running the script, make sure to configure the `const.py` files in the `audiobook_server` and `utilities` directories. Provide necessary API keys, credentials, and other required information.
- Copy stock videos collections to STOCK_VIDEO_FOLDER path; these videos will be used as the video background.

### Dependencies

Make sure to install the required dependencies before running the script:

```bash
pip install -r requirements.txt
```


### Usage

After installing dependencies, run the `yt_auto_main.py` script to initiate the automated YouTube content generation process. Here's an example:

```bash
python yt_auto_main.py
```

After the project execution, the output can be seen in the OUTPUT_FINAL_VIDEO path. Related video info can be found in OUTPUT_FINAL_INFO.

### License

This project is licensed under the [MIT License](LICENSE).

### Acknowledgements

- Thank you to the creators of ChatGPT and other APIs for providing content sources.
- Special thanks to Amazon Polly for TTS services.
- MoviePy for video generation.

``` 
Feel free to further customize and use it on your specific needs.
