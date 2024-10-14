import uuid
from tinydb import TinyDB, Query


class VideoDatabase:
    def __init__(self, db_path='video_database.json'):
        self.db = TinyDB(db_path)
        self.ingested_videos = self.db.table('ingested_videos')
        self.transcriptions = self.db.table('transcriptions')
        self.raw_scripts = self.db.table('raw_scripts')
        self.corrected_scripts = self.db.table('corrected_scripts')

    def add_ingested_video(self, video_file):
        video_id = str(uuid.uuid4())
        self.ingested_videos.insert(
            {'video_id': video_id, 'video_file': video_file})
        return video_id

    def add_transcription(self, video_id, time_start, time_end, segment):
        self.transcriptions.insert({
            'video_id': video_id,
            'time_start': time_start,
            'time_end': time_end,
            'segment': segment
        })

    def add_raw_script(self, video_id, time_start, time_end, clip_file_path):
        self.raw_scripts.insert({
            'video_id': video_id,
            'time_start': time_start,
            'time_end': time_end,
            'clip_file_path': clip_file_path
        })

    def add_corrected_script(self, video_id, time_start, time_end, clip_file_path):
        self.corrected_scripts.insert({
            'video_id': video_id,
            'time_start': time_start,
            'time_end': time_end,
            'clip_file_path': clip_file_path
        })

    def get_ingested_video(self, video_id):
        Video = Query()
        return self.ingested_videos.search(Video.video_id == video_id)

    def get_transcriptions(self, video_id):
        Transcription = Query()
        return self.transcriptions.search(Transcription.video_id == video_id)

    def get_raw_scripts(self, video_id):
        RawScript = Query()
        return self.raw_scripts.search(RawScript.video_id == video_id)

    def get_corrected_scripts(self, video_id):
        CorrectedScript = Query()
        return self.corrected_scripts.search(CorrectedScript.video_id == video_id)

    def update_corrected_script(self, video_id, time_start, time_end, new_clip_file_path):
        CorrectedScript = Query()
        self.corrected_scripts.update(
            {'clip_file_path': new_clip_file_path},
            (CorrectedScript.video_id == video_id) &
            (CorrectedScript.time_start == time_start) &
            (CorrectedScript.time_end == time_end)
        )

    def delete_ingested_video(self, video_id):
        Video = Query()
        self.ingested_videos.remove(Video.video_id == video_id)
        self.transcriptions.remove(Video.video_id == video_id)
        self.raw_scripts.remove(Video.video_id == video_id)
        self.corrected_scripts.remove(Video.video_id == video_id)
