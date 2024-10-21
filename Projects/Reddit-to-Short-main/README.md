## Reddit to Short Converter

**Introduction**

This project automates the conversion of engaging Reddit content into YouTube Shorts, leveraging the power of Python libraries and APIs. It streamlines the process of downloading relevant videos, editing them, and uploading them to your YouTube Shorts channel – all in one go!

**Key Features**

* **Reddit API Integration:** Accesses and retrieves engaging content from Reddit.
* **Automated Video Editing:** Transforms raw video clips into captivating YouTube Shorts format.
* **YouTube API Integration:** Uploads the converted Shorts directly to your YouTube channel.

**Installation**

We recommend using a virtual environment for managing dependencies. Here's a quick guide:

1. **FFmpeg Installation:** Download and install FFmpeg following the official instructions for your operating system:
    * **Mac:** [https://gist.github.com/clayton/6196167?permalink_comment_id=4042366](https://gist.github.com/clayton/6196167?permalink_comment_id=4042366)
    * **Windows 10:** [https://www.youtube.com/watch?v=qSlxv68Xpkw](https://www.youtube.com/watch?v=qSlxv68Xpkw)
    * **Linux:** [https://www.dedicatedcore.com/blog/installing-ffmpeg-ubuntu/](https://www.dedicatedcore.com/blog/installing-ffmpeg-ubuntu/)

2. **Python Packages:** Activate your virtual environment and install the required packages using pip:

```bash
pip install -r requirements.txt
```

**Configuration**

1. **Reddit API:**
    * Create a Reddit App ([https://www.reddit.com/r/developer/](https://www.reddit.com/r/developer/))
    * Update `config.py` with your obtained API credentials.
    * Follow this tutorial for guidance: [https://www.reddit.com/r/LegacyJailbreak/comments/11x9lqc/question_how_am_i_supposed_to_make_a_youtube_api/](https://www.reddit.com/r/LegacyJailbreak/comments/11x9lqc/question_how_am_i_supposed_to_make_a_youtube_api/)

2. **YouTube API:**
    * Enable the YouTube Data API v4 in the Google Cloud Console ([https://developers.google.com/youtube/v3](https://developers.google.com/youtube/v3))
    * Download your `client_secrets.json` file and place it in the same directory as `main.py`.
    * Refer to this tutorial for detailed instructions: [https://developers.google.com/youtube/v3](https://developers.google.com/youtube/v3)

**Running the Script**

1. Ensure you've completed the configuration steps.
2. Open a terminal and navigate to the project directory.
3. Run the script using the following command:

```bash
python main.py
```

**New to Python?**

If you're unfamiliar with running Python scripts in the terminal, right-click on `main.py` and choose "Open with" followed by Python's launcher.

**Code Structure**

The code is organized into well-defined modules for clarity and maintainability:

* `reddit_api.py`: Handles interaction with the Reddit API for fetching content.
* `video_editor.py`: Responsible for transforming raw video into an engaging YouTube Short format.
* `youtube_api.py`: Manages uploading the converted Short to your YouTube channel.

**By utilizing this tool, you can unlock the potential of repurposing engaging Reddit content for your YouTube Shorts channel, saving time and effort while expanding your reach!**

**License**

This project is licensed under the MIT License (see LICENSE file for details).
