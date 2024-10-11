import glob
import os
import shutil
import time

from moviepy.editor import VideoFileClip

import EditVideo
import Folders
import Reddit
import Upload
import config

debug = config.debug


def start():
    global debug
    start_input = int(input("Press 0 to Start the Script..."))
    if start_input == 0:
        debug = False
        print("Starting Main Function...")
        main()
    elif start_input == 10:
        print("DEBUG MODE ON...")
        debug = True
        print("Starting Main Function...")
        main()
    else:
        print("Invalid Input...")
        start()


def debug_print(message):
    if debug:
        print(f"DEBUG: {message}")


def folder_creator():
    """
    Creates necessary folders for the video processing workflow.

    Returns:
        dict: A dictionary containing paths to the base, reddit, render, and final folders.
    """
    create_folder = Folders.FolderManager()
    debug_print(f"Creating folders: {create_folder}")
    result = create_folder.create_folders()
    print("Folders created successfully.")
    debug_print(f"Folder creation result: {result}")

    return {
        'base_folder': create_folder.base_folder,
        'reddit_folder': create_folder.reddit_folder_path,
        'render_folder': create_folder.render_folder_path,
        'final_folder': create_folder.final_folder_path
    }


def get_video_info(directory):
    """
    Fetches video information from Reddit.

    Args:
        directory (str): The directory where video information is stored.

    Returns:
        list: A list of dictionaries containing video information such as URL and title.
    """
    subreddit = config.subreddit
    info = Reddit.GetRedditLink(subreddit, directory=directory)
    debug_print(f"Fetching video info from Reddit for subreddit: {subreddit}, directory: {directory}")
    fetched_info = info.main()
    print("Fetched video information from Reddit.")
    debug_print(f"Fetched video info: {fetched_info}")
    return fetched_info


def download_video(directory, info):
    """
    Downloads videos from Reddit based on the provided info.

    Args:
        directory (str): The directory where the video will be downloaded.
        info (list): A list of dictionaries containing video information.

    Returns:
        bool: True if at least one video is successfully downloaded, False otherwise.
    """
    for item in info:
        url = item['url']
        debug_print(f"Attempting to download video from URL: {url}")
        print(f"Attempting to download video: {item['title']}")
        download = Reddit.DownloadRedditVideo(url=url, directory=directory)
        if download.download():
            debug_print(f"Video downloaded successfully: {download}")
            print(f"Video downloaded from URL: {url}")
            return True
    return False


def render_video(directory, clip_name, output_name, resolution):
    """
    Renders the video to the specified resolution.

    Args:
        directory (str): The directory where the video is located.
        clip_name (str): The name of the input clip.
        output_name (str): The name of the output clip.
        resolution (tuple): The desired resolution for the output video.

    Returns:
        str or None: The path to the rendered video if successful, None otherwise.
    """
    render = EditVideo.Render(directory=directory, clip_name=clip_name, output_name=output_name, resolution=resolution)
    debug_print(f"Rendering video: {render}")
    if render.render:
        debug_print(f"Rendered video successfully: {render}")
        print(f"Video rendered to {output_name}")
        return os.path.join(directory, output_name)
    return None


def upload_video(clip_name, title):
    """
    Uploads the video to YouTube.

    Args:
        clip_name (str): The path to the video clip.
        title (str): The title for the YouTube video.

    Returns:
        bool: True if the upload is successful, False otherwise.
    """
    description = (
        "#shorts, #funny, #reddit, #redditfunny, #redditvideos, #funnyvideos, "
        "#shortsreddit, #shortsfunny, #shortsredditfunny, #shortsredditvideos, "
        "#shortsfunnyvideos, #redditfunnyvideos, #redditshorts, #redditshortsfunny, "
        "#redditshortsvideos, #redditfunnyshorts, #redditfunnyshortsvideos, "
        "#redditvideosshorts, #funnyshorts, #funnyshortsvideos, #funnyvideosshorts, "
        "#shortsfunnyvideos, #shortsredditfunnyvideos, #shortsredditvideosfunny, "
        "#shortsvideosfunny, #shortsvideos"
    )
    tags = config.youtube['tags']
    category = config.youtube['category']
    status = config.youtube['status']

    debug_print(f"Starting upload with title: {title}")
    upload = Upload.start(
        clip_name=clip_name,
        title=title,
        description=description,
        tags=tags,
        category=category,
        status=status
    )

    if upload is not None:
        debug_print(f"Video uploaded successfully: {upload}")
        print(f"Video uploaded with title: {title}")
        return True
    return False


def day_complete(reason):
    """
    Handles the completion of a day's worth of uploads.

    Args:
        reason (str): The reason for completion ('API' or 'count').
    """
    hour = 3600
    day = 86400

    debug_print(f"Day complete reason: {reason}")
    if reason == 'API':
        print("Day Complete... Taking a break for 24 hours.")
        time.sleep(day)
    elif reason == 'count':
        print("Upload Count = 6. Trying again in 1 hour...")
        time.sleep(hour)


def video_duration(video_path):
    """
    Gets the duration of a video.

    Args:
        video_path (str): The path to the video file.

    Returns:
        float: The duration of the video in seconds.
    """
    with VideoFileClip(video_path) as clip:
        duration = clip.duration
        debug_print(f"Video duration for {video_path}: {duration} seconds")
        return duration


def main():
    """
    Main function to manage the entire workflow from creating folders, downloading,
    rendering, and uploading videos.
    """
    folders = folder_creator()
    reddit_directory = folders['reddit_folder']
    video_info = get_video_info(reddit_directory)
    if not video_info:
        print("No video information found.")
        return
    render_clip_name = 'render_input.mp4'
    render_output_name = 'render_output.mp4'
    render_directory = folders['render_folder']
    upload_count = 0
    upload_directory = folders['final_folder']
    upload_output = 'FINAL_VIDEO.mp4'
    resolution = config.video['dimensions']
    for info in video_info:
        url = info['url']
        title = info['title']
        print(f"Attempting to download video: {title}")
        download_success = download_video(directory=reddit_directory, info=[info])
        if not download_success:
            print(f"Failed to download video: {title}")
            continue
        video_found = False
        for file in glob.glob(os.path.join(reddit_directory, '*.mp4')):
            if os.path.basename(file).startswith(os.path.basename(url)):
                shutil.copy(file, os.path.join(render_directory, render_clip_name))
                video_found = True
                break
        if not video_found:
            print(f"No video file found for URL: {url}")
            continue
        duration = video_duration(os.path.join(render_directory, render_clip_name))
        print(f"Downloaded video duration: {duration} seconds")
        if duration >= 60:
            print(f"Video too big for a Short. Skipping {title}...")
            continue
        rendered_file = render_video(directory=render_directory, clip_name=render_clip_name,
                                     output_name=render_output_name, resolution=resolution)
        if rendered_file:
            shutil.copy(rendered_file, os.path.join(upload_directory, upload_output))
            if upload_count < 6:
                if upload_video(clip_name=os.path.join(upload_directory, upload_output), title=title):
                    upload_count += 1
                    with open(config.database, 'a') as f:
                        f.write(f"{url},")
                else:
                    day_complete('API')
            else:
                day_complete('count')
        else:
            print(f"Rendering failed for {title}. Skipping uploading.")
        print("Taking a break for 10 seconds...")
        time.sleep(10)


if __name__ == "__main__":
    start()
