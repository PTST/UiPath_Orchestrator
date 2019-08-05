from datetime import datetime, timezone
from subclasses.initializer import initializer, comparable
import json

@comparable
class ProcessingException(object):
    def __init__(self, reason:str=None, details:str=None, exception_type:str=None, associated_image_filepath:str=None, creation_time:datetime=None):
        self.reason = reason
        self.details = details
        self.type = exception_type
        self.associated_image_filepath = associated_image_filepath
        self.creation_time = creation_time
        if creation_time and not isinstance(creation_time, datetime):
            if isinstance(creation_time, str):
                if len(creation_time) > 27:
                    creation_time = creation_time[:26] + "Z"
                self.creation_time = datetime.strptime(creation_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                raise ValueError("creation_time needs to be a datetime")
        if self.creation_time and self.creation_time.tzinfo is None:
            self.creation_time = self.creation_time.astimezone().astimezone(timezone.utc)
        
        self.json = self.to_json()
        
    def to_json(self):
        return {
            "Reason": self.reason,
            "Details": self.details,
            "Type": self.type,
            "AssociatedImageFilePath": self.associated_image_filepath,
            "CreationTime": self.creation_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if self.creation_time else None
        }
