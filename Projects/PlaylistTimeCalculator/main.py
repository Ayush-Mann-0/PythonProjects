import re
import googleapiclient.discovery
from datetime import timedelta
from urllib.parse import urlparse, parse_qs

# Replace with your actual API key
# API_KEY = "AIzaSyC5YaF8QRssdvF2peSQbwnjt7gCqgeksBA" # Example...

API_KEY = ""

# Playlist URL
playlist_url = input('Enter Playlist URL')

def get_playlist_id(playlist_url):
    parsed_url = urlparse(playlist_url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get("list", [None])[0]

def get_playlist_videos(youtube, playlist_id, start_index, end_index):
    video_ids = []
    next_page_token = None
    total_fetched = 0

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            total_fetched += 1
            if total_fetched >= start_index:
                video_ids.append(item['contentDetails']['videoId'])
            if total_fetched >= end_index:
                return video_ids

        if 'nextPageToken' not in response or total_fetched >= end_index:
            break

        next_page_token = response.get('nextPageToken')

    return video_ids

def get_video_durations(youtube, video_ids):
    total_duration = timedelta()
    video_durations = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="contentDetails,snippet",
            id=','.join(video_ids[i:i + 50])
        )
        response = request.execute()

        for item in response['items']:
            video_title = item['snippet']['title']
            duration = item['contentDetails']['duration']
            parsed_duration = parse_duration(duration)
            video_durations.append((video_title, parsed_duration))
            total_duration += parsed_duration

    return video_durations, total_duration

def parse_duration(duration):
    match = re.match(r'PT((\d+)H)?((\d+)M)?((\d+)S)?', duration)
    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(4)) if match.group(4) else 0
    seconds = int(match.group(6)) if match.group(6) else 0

    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def main():
    playlist_id = get_playlist_id(playlist_url)
    if not playlist_id:
        print("Invalid playlist URL. Please try again.")
        return

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    while True:
        try:
            start_index = int(input("Enter the start video number (1-based index): ").strip())
            end_index_input = input("Enter the end video number (leave blank for all videos from start index): ").strip()
            end_index = float('inf') if end_index_input == "" else int(end_index_input)

            if start_index <= 0 or (end_index != float('inf') and end_index < start_index):
                raise ValueError("Please enter valid positive integers with the end index greater than or equal to the start index.")
            break
        except ValueError as ve:
            print(f"Error: {ve}. Please try again.")

    print("Fetching video details, please wait...")
    video_ids = get_playlist_videos(youtube, playlist_id, start_index, end_index)
    video_durations, total_duration = get_video_durations(youtube, video_ids)

    print("\n--- Video Durations ---")
    for idx, (title, duration) in enumerate(video_durations, start=start_index):
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"{idx}. {title} - {int(hours)}h {int(minutes)}m {int(seconds)}s")

    while True:
        try:
            speed = float(input("Enter the playback speed: ").strip())
            if speed <= 0:
                raise ValueError("Playback speed must be a positive number.")
            break
        except ValueError as ve:
            print(f"Error: {ve}. Please try again.")

    # Adjust total duration by dividing by speed
    adjusted_total_duration = total_duration / speed
    adjusted_hours, remainder = divmod(adjusted_total_duration.total_seconds(), 3600)
    adjusted_minutes, adjusted_seconds = divmod(remainder, 60)

    print(f"\nTotal Playlist Duration for selected videos: {total_duration} "
          f"({int(adjusted_hours)}h {int(adjusted_minutes)}m {int(adjusted_seconds)}s at {speed}x speed)")

if __name__ == "__main__":
    main()
