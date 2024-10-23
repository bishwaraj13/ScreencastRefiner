import uuid
from tinydb import TinyDB, Query
from datetime import datetime
import pytz


class VideoDatabase:
    def __init__(self, db_path='video_database.json'):
        self.db = TinyDB(db_path)
        self.ingested_videos = self.db.table('ingested_videos')
        self.transcriptions = self.db.table('transcriptions')
        self.scenes = self.db.table('scenes')

    def get_db(self):
        return self.db

    def add_ingested_video(self, video_file):
        video_id = str(uuid.uuid4())
        self.ingested_videos.insert(
            {'video_id': video_id, 'video_file': video_file})
        return video_id

    def add_transcription(self, video_id, transcript_dict):
        self.transcriptions.insert({
            'video_id': video_id,
            'transcript_dict': transcript_dict
        })

    def add_scene(self,
                  video_id,
                  step_number,
                  title,
                  time_start,
                  time_end,
                  original_narration,
                  polished_narration):
        return self.scenes.insert({
            'video_id': video_id,
            'step_number': step_number,
            'title': title,
            'time_start': time_start,
            'time_end': time_end,
            'original_narration': original_narration,
            'polished_narration': polished_narration
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

    def _get_current_time(self):
        ist_timezone = pytz.timezone("Asia/Kolkata")
        return datetime.now(ist_timezone).strftime('%Y-%m-%d %H:%M:%S.%f %Z')

    def update_ingested_video(self, video_id, step_name, completed=True, error=None):
        Video = Query()
        video = self.ingested_videos.get(Video.video_id == video_id)

        if video:
            steps_completed = video.get('steps_completed', {})
            steps_completed[f"{step_name}_completed"] = completed

            execution_time = video.get('execution_time', {})
            execution_time[step_name] = self._get_current_time()

            update_data = {
                'steps_completed': steps_completed,
                'execution_time': execution_time
            }

            if error:
                errors = video.get('errors', {})
                errors[step_name] = error
                update_data['errors'] = errors

            self.ingested_videos.update(
                update_data, Video.video_id == video_id)
        else:
            print(f"Video with id {video_id} not found.")

    def get_record(self, collection_name, query_field, query_value):
        collection = self.db.table(collection_name)
        Record = Query()
        return collection.get(getattr(Record, query_field) == query_value)
    
    def get_records(self, collection_name, query_field, query_value):
        """
        Get all records from a collection that match the given query.

        :param collection_name: Name of the collection to query
        :param query_field: Field to query for finding the records
        :param query_value: Value to match in the query field
        :return: List of matching records
        """
        collection = self.db.table(collection_name)
        Record = Query()
        return collection.search(getattr(Record, query_field) == query_value)

    def get_specific_values(self, collection_name, query_field, query_value, *fields):
        record = self.get_record(collection_name, query_field, query_value)
        if record:
            return {field: record.get(field) for field in fields if field in record}
        return None

    def update_record(self, table_name: str, query_field: str, query_value: str, update_field: str, update_value: any):
        """
        Update a specific field in a record of any table.

        :param table_name: Name of the table to update
        :param query_field: Field to query for finding the record
        :param query_value: Value to match in the query field
        :param update_field: Field to update
        :param update_value: New value for the update field
        """
        table = self.db.table(table_name)
        Record = Query()
        table.update({update_field: update_value}, getattr(
            Record, query_field) == query_value)
        
    def update_record(self, table_name: str, query_criteria: dict, update_field: str, update_value: any):
        """
        Update a specific field in a record of any table based on multiple criteria.

        :param table_name: Name of the table to update
        :param query_criteria: Dictionary of field-value pairs to use as query criteria
        :param update_field: Field to update
        :param update_value: New value for the update field
        """
        table = self.db.table(table_name)
        Record = Query()
        
        # Build the query condition
        condition = None
        for field, value in query_criteria.items():
            if condition is None:
                condition = (getattr(Record, field) == value)
            else:
                condition &= (getattr(Record, field) == value)
        
        # Update the record
        table.update({update_field: update_value}, condition)
