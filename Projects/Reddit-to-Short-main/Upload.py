import httplib2
import logging
import config
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

debug = config.debug


def configure_logging():
    """Configure logging level based on the debug flag."""
    if debug:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class YouTubeUploader:
    """A class that simplifies uploading videos to YouTube using the YouTube Data API v3."""

    def __init__(self, client_secrets_file, storage_file, scope, api_service_name, api_version):
        """
        Initializes the YouTubeUploader object with necessary credentials and API details.

        Args:
            client_secrets_file (str): Path to the client secrets JSON file.
            storage_file (str): Path to the storage file for OAuth2 credentials.
            scope (str): The OAuth2 scope for YouTube upload.
            api_service_name (str): The API service name (e.g., "YouTube").
            api_version (str): The API version (e.g., "v3").
            debug (bool): Flag to enable or disable debug logging.
        """
        configure_logging()
        self.client_secrets_file = client_secrets_file
        self.storage_file = storage_file
        self.scope = scope
        self.api_service_name = api_service_name
        self.api_version = api_version
        self.youtube = self.get_authenticated_service()

    def get_authenticated_service(self):
        """
        Authenticates the uploader and builds the YouTube service object.

        Returns:
            googleapiclient.discovery.Resource: An authorized YouTube API client service object.
        """
        logging.debug("Starting authentication process.")
        flow = flow_from_clientsecrets(self.client_secrets_file, scope=self.scope)
        storage = Storage(self.storage_file)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            logging.debug("No valid credentials found. Running OAuth2 flow.")
            credentials = run_flow(flow, storage)

        logging.debug("Authentication successful.")
        return build(self.api_service_name, self.api_version, http=credentials.authorize(httplib2.Http()))

    def upload(self, file, metadata):
        """
        Uploads a video file to YouTube with the provided metadata.

        Args:
            file (str): The path to the video file to upload.
            metadata (dict): A dictionary containing metadata for the video (title, description, tags, category, status).

        Returns:
            dict: The response from the YouTube API if the upload is successful, None otherwise.
        """
        try:
            logging.debug(f"Preparing to upload file: {file} with metadata: {metadata}")
            insert_request = self.youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": metadata["title"],
                        "description": metadata["description"],
                        "tags": metadata["tags"],
                        "categoryId": metadata["category"]
                    },
                    "status": {
                        "privacyStatus": metadata["status"]
                    }
                },
                media_body=MediaFileUpload(file)
            )
            response = insert_request.execute()
            video_id = response.get("id")
            logging.info(f"Video uploaded successfully! Video ID: {video_id}")
            return response
        except HttpError as e:
            return None


def start(clip_name, title, description, tags, category, status):
    """
    Starts the video upload process to YouTube.

    Args:
        clip_name (str): The path to the video file to upload.
        title (str): The title of the video.
        description (str): The description of the video.
        tags (list): A list of tags for the video.
        category (str): The category ID for the video.
        status (str): The privacy status of the video (e.g., "public", "private").
        debug (bool): Flag to enable or disable debug logging.

    Returns:
        dict: The response from the YouTube API if the upload is successful, None otherwise.
    """
    configure_logging()

    # Constants for YouTube API credentials and scope
    CLIENT_SECRETS_FILE = "client_secrets.json"
    STORAGE_FILE = "upload-oauth2.json"
    YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    logging.debug("Initializing YouTubeUploader.")
    uploader = YouTubeUploader(
        client_secrets_file=CLIENT_SECRETS_FILE,
        storage_file=STORAGE_FILE,
        scope=YOUTUBE_UPLOAD_SCOPE,
        api_service_name=YOUTUBE_API_SERVICE_NAME,
        api_version=YOUTUBE_API_VERSION,
    )

    metadata = {
        "title": title,
        "description": description,
        "tags": tags,
        "category": category,
        "status": status
    }

    logging.debug(f"Starting upload process for {clip_name}.")
    response = uploader.upload(clip_name, metadata)
    return response


if __name__ == '__main__':
    # Example usage:
    clip_name = "example_video.mp4"
    title = "Example Video Title"
    description = "This is an example video description."
    tags = ["example", "video", "upload"]
    category = "22"  # Category ID for "People & Blogs"
    status = "public"
    debug = True  # Set to True to enable debug logging

    start(clip_name, title, description, tags, category, status)
