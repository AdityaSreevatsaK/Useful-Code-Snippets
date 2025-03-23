from IPython.display import YouTubeVideo


def play_youtube_video(youtube_video_id: str, width_value: int = 800, height_value: int = 450):
    """
        Description: The play_youtube_video function embeds a YouTube video directly into a Jupyter notebook using the
        video ID. It allows autoplay and customisable dimensions for the video display (800x450 by default).
    """
    return YouTubeVideo(youtube_video_id, width=width_value, height=height_value, allow_autoplay=True)


# Replace with your desired YouTube video ID
video_id = "g91kQyy4G7E"
play_youtube_video(video_id)
