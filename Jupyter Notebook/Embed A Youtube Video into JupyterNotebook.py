from IPython.display import YouTubeVideo


def play_youtube_video(youtube_video_id: str, width_value: int = 800, height_value: int = 450):
    """
        Description: Embed a YouTube video in a Jupyter Notebook.

        Args:
            youtube_video_id (str): The ID of the YouTube video to be embedded.
            width_value (int, optional): The width of the video player. Defaults to 800.
            height_value (int, optional): The height of the video player. Defaults to 450.

        Returns:
            YouTubeVideo: An IPython.display.YouTubeVideo object that can be displayed in a Jupyter Notebook.
    """
    return YouTubeVideo(youtube_video_id, width=width_value, height=height_value, allow_autoplay=True)


# Replace with your desired YouTube video ID
video_id = "g91kQyy4G7E"
play_youtube_video(video_id)
