from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip

def add_subtitle(input_video_path, subtitle_path, output_video_path):
    # Load the video clip
    video_clip = VideoFileClip(input_video_path)

    # Load the subtitles
    subtitles = SubtitlesClip(subtitle_path)

    # Set style for subtitles
    subtitles = subtitles.set_position(('center', 'bottom')).set_duration(video_clip.duration)

    # Overlay subtitles onto the video
    video_with_subtitles = CompositeVideoClip([video_clip, subtitles])

    # Write the resulting video with subtitles
    video_with_subtitles.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

input_video_path = '/Users/synan/Projects/webinar01/lambda/news.mp4'
subtitle_path = '/Users/synan/Projects/webinar01/lambda/subtitle.srt'
output_video_path = '/Users/synan/Projects/webinar01/lambda/news_with_caption.mp4'

add_subtitle(input_video_path, subtitle_path, output_video_path)
