from subclasses.OrganizationUnit import OrganizationUnit
from datetime import datetime, timezone
from subclasses.initializer import initializer, comparable

@comparable
class Queue(object):
    @initializer
    def __init__(self,
                 name: str,
                 description: str,
                 max_number_of_retries: int,
                 accept_automatically_retry: bool,
                 enforce_unique_reference: bool,
                 creation_time: datetime,
                 queue_id: int,
                 organization_unit: OrganizationUnit):
        self.id = queue_id
        if not isinstance(creation_time, datetime):
            if isinstance(creation_time, str):
                self.creation_time = datetime.strptime(creation_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                raise ValueError("creation_time needs to be a datetime")
        if self.creation_time and self.creation_time.tzinfo is None:
            self.creation_time = self.creation_time.astimezone().astimezone(timezone.utc)
