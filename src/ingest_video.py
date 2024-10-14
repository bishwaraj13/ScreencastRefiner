from common.connection import VideoDatabase


def ingest_video(video_file):
    db = VideoDatabase()
    video_id = db.add_ingested_video(video_file)
    print(video_file)

    return video_id


if __name__ == '__main__':
    ingest_video(
        '/Users/bishwaraj/Documents/explainer_videos/add_button_to_notion.mp4'
    )
