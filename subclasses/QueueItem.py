from datetime import datetime, timezone
from subclasses.ProcessingException import ProcessingException
from subclasses.initializer import initializer, comparable
from subclasses.Queue import Queue
@comparable
class QueueItem(object):
    @initializer
    def __init__(self,
                 queue_definition_id: int,
                 output_data:dict,
                 status:str,
                 review_status:str,
                 reviewer_user_id:int,
                 key:str,
                 reference:str,
                 processing_exception_type:str,
                 due_date:datetime,
                 priority:str,
                 defer_date:datetime,
                 start_processing:datetime,
                 end_processing:datetime,
                 seconds_in_previous_attempts:int,
                 ancestor_id:int,
                 retry_number:int,
                 specific_data:dict,
                 creation_time:datetime,
                 progress:str,
                 row_version:str,
                 id:int,
                 processing_exception:ProcessingException,
                 queue:Queue):
        if due_date and not isinstance(due_date, datetime):
            if isinstance(due_date, str):
                self.due_date = datetime.strptime(due_date, "%Y-%m-%dT%H:%M:%SZ")
            else:
                raise ValueError("due_date needs to be a datetime")
        if self.due_date and self.due_date.tzinfo is None:
            self.due_date = self.due_date.astimezone().astimezone(timezone.utc)
        
        if defer_date and not isinstance(defer_date, datetime):
            if isinstance(defer_date, str):
                self.defer_date = datetime.strptime(defer_date, "%Y-%m-%dT%H:%M:%SZ")
            else:
                raise ValueError("defer_date needs to be a datetime")
        if self.defer_date and self.defer_date.tzinfo is None:
            self.defer_date = self.defer_date.astimezone().astimezone(timezone.utc)

        if start_processing and not isinstance(start_processing, datetime):
            if isinstance(start_processing, str):
                if len(start_processing) > 27:
                    start_processing = start_processing[:26] + "Z"
                self.start_processing = datetime.strptime(start_processing, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                raise ValueError("start_processing needs to be a datetime")
        if self.start_processing and self.start_processing.tzinfo is None:
            self.start_processing = self.start_processing.astimezone().astimezone(timezone.utc)

        if end_processing and not isinstance(end_processing, datetime):
            if isinstance(end_processing, str):
                if len(end_processing) > 27:
                    end_processing = end_processing[:26] + "Z"
                self.end_processing = datetime.strptime(end_processing, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                raise ValueError("end_processing needs to be a datetime")
        if self.end_processing and self.end_processing.tzinfo is None:
            self.end_processing = self.end_processing.astimezone().astimezone(timezone.utc)

        if creation_time and not isinstance(creation_time, datetime):
            if isinstance(creation_time, str):
                if len(creation_time) > 27:
                    creation_time = creation_time[:26] + "Z"
                self.creation_time = datetime.strptime(creation_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                raise ValueError("creation_time needs to be a datetime")
        if self.creation_time and self.creation_time.tzinfo is None:
            self.creation_time = self.creation_time.astimezone().astimezone(timezone.utc)
