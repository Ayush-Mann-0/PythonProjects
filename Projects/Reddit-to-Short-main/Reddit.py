import praw
import redvid
import config
import os

DEBUG = config.debug


def debug_print(message, level="INFO"):
    if DEBUG:
        print(f"[{level}] {message}")


class DownloadRedditVideo:
    def __init__(self, url, directory):
        """
        Initializes the DownloadRedditVideo object with the URL and directory.

        Args:
            url (str): The URL of the Reddit video to download.
            directory (str): The directory where the video will be saved.
        """
        self.url = url
        self.directory = directory

    def download(self):
        """
        Downloads the Reddit video from the specified URL.

        Returns:
            bool: True if the download is successful, False otherwise.
        """
        try:
            download = redvid.Downloader(self.url, max_q=True)
            if int(download.duration) <= 60:
                download.path = self.directory
                download.download()
                debug_print(f"Downloaded video of duration: {download.duration} seconds")
                return True
            else:
                debug_print(f"Video too long: {download.duration} seconds. Skipping: {self.url}", "WARNING")
                return False
        except Exception as e:
            debug_print(f"Error downloading video: {e}", "ERROR")
            return False


class GetRedditLink:
    def __init__(self, subreddit, directory):
        """
        Initializes the GetRedditLink object with subreddit and directory.

        Args:
            subreddit (str): The subreddit to fetch posts from.
            directory (str): The directory to use for storing video information.
        """
        self.subreddit = subreddit
        self.directory = directory
        self.reddit_login = config.reddit_login
        self.login = None
        self.posts = []
        self.filtered_output = []

    def log_in(self):
        """
        Logs into Reddit using the provided credentials.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        debug_print("Trying to log into Reddit...")
        try:
            self.login = praw.Reddit(
                client_id=self.reddit_login['client_id'],
                client_secret=self.reddit_login['client_secret'],
                username=self.reddit_login['username'],
                password=self.reddit_login['password'],
                user_agent=self.reddit_login['user_agent']
            )
            debug_print("Login successful.")
            return True
        except praw.exceptions.PRAWException as e:
            debug_print(f"Failed to log in: {e}", "ERROR")
            return False

    def get_posts(self):
        """
        Fetches the top posts from the specified subreddit.

        Returns:
            bool: True if fetching posts is successful, False otherwise.
        """
        debug_print("Fetching top posts...")
        try:
            self.posts = list(self.login.subreddit(self.subreddit).top(time_filter="week", limit=99))
            debug_print(f"Fetched {len(self.posts)} posts.")
            return True
        except Exception as e:
            debug_print(f"Failed to get posts: {e}", "ERROR")
            return False

    def filter_posts(self):
        """
        Filters the fetched posts to include only suitable videos.

        Returns:
            bool: True if filtering is successful, False otherwise.
        """
        debug_print("Filtering posts...")
        try:
            database_path = config.database
            if not os.path.exists(database_path):
                with open(database_path, 'w') as f:
                    pass
                debug_print(f"Created database file: {database_path}")

            with open(database_path, 'r') as f:
                database = f.read().split(',')

            for post in self.posts:
                author_name = post.author.name if post.author else 'Unknown'
                if post.stickied or post.over_18 or post.url in database or not post.url.startswith('https://v.redd.it'):
                    continue
                self.filtered_output.append({
                    'url': post.url,
                    'title': post.title,
                    'author': author_name
                })
            debug_print(f"Filtered {len(self.filtered_output)} posts.")
            return True
        except Exception as e:
            debug_print(f"Error filtering posts: {e}", "ERROR")
            return False

    def main(self):
        """
        Main method to log in, fetch, and filter posts.

        Returns:
            list: A list of dictionaries containing filtered post information.
        """
        if self.log_in():
            if self.get_posts():
                if self.filter_posts():
                    return self.filtered_output
                else:
                    debug_print("Filtering posts failed.", "ERROR")
            else:
                debug_print("Fetching posts failed.", "ERROR")
        else:
            debug_print("Logging in failed.", "ERROR")
        return []


if __name__ == '__main__':
    subreddit = config.subreddit
    reddit_instance = GetRedditLink(subreddit, 'output/test')
    output = reddit_instance.main()
    for item in output:
        url = item['url']
        downloader = DownloadRedditVideo(url=url, directory='output/test')
        downloader.download()
