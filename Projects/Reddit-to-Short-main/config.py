debug = False # Debug Variable for getting Various detail of what the Script is doing.
subreddit = "funny" # Subreddit to get the Video from.
# You can combine multiple subreddits with '+'.
# Example: "funny+cars"

# Local text database file that ensures no duplicate videos get processed.
database = 'database.txt'

# Reddit login credentials
reddit_login = {
    'client_id': 'your-client-id',
    'client_secret': 'your-client-secret',
    'password': 'your-password',
    'user_agent': 'your-user-agent',
    'username': 'your-username'
}

# YouTube upload settings
youtube = {
    'tags': ['funny', 'shorts', 'lol'], # Can add more tags just like these
    'category': 23,  # Category ID. More about categories below.
    'status': 'public'  # {public, private, unlisted}
}

# Video settings
video = {
    'dimensions': (1080, 1920),  # (horizontal, vertical) or None to upload the original clip as is.
    'blur': False  # Blur non-perfect-fit clips
}
