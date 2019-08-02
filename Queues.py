import re
import json
import requests
from BaseAPI import BaseAPI
from datetime import datetime, timezone
from subclasses.Queue import Queue
from subclasses.ProcessingException import ProcessingException
from subclasses.QueueItem import QueueItem


class Queues(BaseAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Queue = Queue
        self.ProcessingException = ProcessingException
        self.QueueItem = QueueItem
        self.regex = re.compile(r"(?<!^)([A-Z])")

    def _Get_Queues(self, organization_unit):
        url = f"{self.base_url}/odata/QueueDefinitions"
        headers = {
            "Authorization": self.auth_token,
            "X-UIPATH-OrganizationUnitId": str(organization_unit.id)
        }

        r = requests.get(url, headers=headers, verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self._Get_Queues(organization_unit)
            else:
                r.raise_for_status()

        queues = []
        for queue in r.json()["value"]:
            name = queue["Name"]
            description = queue["Description"]
            max_number_of_retries = queue["MaxNumberOfRetries"]
            accept_automatically_retry = queue["AcceptAutomaticallyRetry"]
            enforce_unique_reference = queue["EnforceUniqueReference"]
            creation_time = queue["CreationTime"]
            queueid = queue["Id"]
            queues.append(self.Queue(name, description, max_number_of_retries, accept_automatically_retry,
                                     enforce_unique_reference, creation_time, queueid, organization_unit))
        self.Queues = queues
        return queues

    def Get_Queue(self, name, organization_unit):
        self._Get_Queues(organization_unit)
        matches = [x for x in self.Queues if x.name.lower() == name.lower() or x.id == name]
        if len(matches) == 0:
            raise ValueError("No queue by that name on this organization unit")
        return matches[0]

    def json_to_queue_item(self, data:dict, queue:Queue):
        kwargs = {}
        keys = list(data)
        for key in keys:
            new_key = self.regex.sub(r"_\1", key).lower()
            kwargs[new_key] = data.pop(key)
        if kwargs["processing_exception"]:
            kwargs["processing_exception"] = self.ProcessingException(
                *[v for k, v in kwargs["processing_exception"].items()])
        else:
            kwargs["processing_exception"] = self.ProcessingException()

        kwargs["specific_data"] = kwargs.pop("specific_content")
        kwargs["output_data"] = kwargs.pop("output")
        kwargs["queue"] = queue
        if "@odata.context" in kwargs:
            kwargs.pop("@odata.context")
        return self.QueueItem(**kwargs)

    def Get_Queue_Items(self, queue, top=None, skip=None, filters=None):
        url = f"{self.base_url}/odata/QueueItems"
        headers = {
            "Authorization": self.auth_token,
            "X-UIPATH-OrganizationUnitId": str(queue.organization_unit.id)
        }

        params = {
            "$filter": f"QueueDefinitionId eq {str(queue.id)}"
        }
        if top:
            params["$top"] = top
        if skip:
            params["$skip"] = skip
        if filters:
            params["$filter"] += f" and {filters}"

        r = requests.get(url, params=params, headers=headers,
                         verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self.Get_Queue_Items(queue, top, skip)
            else:
                r.raise_for_status()
        results = r.json()["value"]
        
            
        return [self.json_to_queue_item(x, queue) for x in results]

    def search_queue_items(self,
                           queue,
                           reference=None,
                           statuses=None,
                           exception_types=None,
                           specific_data=None,
                           output_data=None,
                           end_processing_greater_than=None,
                           end_processing_less_than=None,
                           queue_item_id=None):
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        odata_filters = []
        if queue_item_id:
            odata_filters.append(f"Id eq {queue_item_id}")
        if reference:
            odata_filters.append(f"Reference eq '{reference}'")
        if statuses:
            odata_filters.append(
                "(" + " or ".join([f"Status eq '{x}'" for x in statuses]) + ")")
        if exception_types:
            odata_filters.append(
                "(" + " or ".join([f"ProcessingExceptionType eq '{x}'" for x in statuses]) + ")")
        if specific_data:
            specific_data_filters = []
            for k, v in specific_data.items():
                specific_data_filters.append(
                    f"contains(SpecificData,'\"{k}\":\"{v}\"')")
            odata_filters.append(f"({' and '.join(specific_data_filters)})")
        if output_data:
            output_data_filters = []
            for k, v in output_data.items():
                output_data_filters.append(
                    f"contains(OutputData,'\"{k}\":\"{v}\"')")
            odata_filters.append(f"({' and '.join(output_data_filters)})")
        if end_processing_greater_than:
            if end_processing_greater_than.tzinfo is None:
                end_processing_greater_than = end_processing_greater_than.astimezone()
            if statuses is None or not set(statuses).isdisjoint(set(["New", "Inprogress", "Abandoned"])):
                odata_filters.append(
                    f"(EndProcessing ge {end_processing_greater_than.astimezone(timezone.utc).strftime(date_format)} or EndProcessing eq null)")
            else:
                odata_filters.append(
                    f"EndProcessing ge {end_processing_greater_than.astimezone(timezone.utc).strftime(date_format)}")
        if end_processing_less_than:
            if end_processing_less_than.tzinfo is None:
                end_processing_less_than = end_processing_less_than.astimezone()
            odata_filters.append(
                f"EndProcessing le {end_processing_less_than.isoformat()}")

        odata_filter = " and ".join(odata_filters)
        return self.Get_Queue_Items(queue, filters=odata_filter)

    def add_queue_item(self, queue, specific_data=None, priority="Normal", due_date=None, reference=None, defer_date=None):
        url = f"{self.base_url}/odata/Queues/UiPathODataSvc.AddQueueItem"

        headers = {
            "Authorization": self.auth_token,
            "X-UIPATH-OrganizationUnitId": str(queue.organization_unit.id)
        }

        date_format = "%Y-%m-%dT%H:%M:%SZ"
        if defer_date:
            if defer_date.tzinfo is None:
                defer_date = defer_date.astimezone()
            defer_date = defer_date.astimezone(
                timezone.utc).strftime(date_format)
        if due_date:
            if due_date.tzinfo is None:
                due_date = due_date.astimezone()
            due_date = due_date.astimezone(timezone.utc).strftime(date_format)

        payload = {
            "itemData": {
                "Name": queue.name,
                "Priority": priority,
                "SpecificContent": specific_data,
                "DeferDate": defer_date,
                "DueDate": due_date,
                "Reference": reference
            }
        }

        r = requests.post(url, json=payload, headers=headers,
                          verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self.add_queue_item(queue, specific_data, priority, due_date, reference, defer_date)
            else:
                r.raise_for_status()
        return self.json_to_queue_item(r.json(), queue)

    def set_transaction_status(self,
                               queue_item: QueueItem,
                               is_successful: bool,
                               exception_information: ProcessingException = None,
                               output: dict = None):
        if is_successful and exception_information:
            raise ValueError("Successful item cannot have exception information")
        if not is_successful and output:
            raise ValueError("Only successful items can have output")
        
        url = f"{self.base_url}/odata/Queues({queue_item.id})/UiPathODataSvc.SetTransactionResult"

        headers = {
            "Authorization": self.auth_token,
            "X-UIPATH-OrganizationUnitId": str(queue_item.queue.organization_unit.id),
            "Accept": "application/json"
        }

        payload = {
            "transactionResult": {
                "IsSuccessful": is_successful,
                "ProcessingException": exception_information.json if exception_information else None,
                "Output": output if output else None
            }
        }

        r = requests.post(url, json=payload, headers=headers, verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self.set_transaction_status(queue_item, is_successful, exception_information, output)
            else:
                r.raise_for_status()
        return

    def delete_queue_item(self, queue_item):
        url = f"{self.base_url}/odata/QueueItems({queue_item.id})"
        headers = {
            "Authorization": self.auth_token,
            "X-UIPATH-OrganizationUnitId": str(queue_item.queue.organization_unit.id)
        }
        r = requests.delete(url, headers=headers, verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self.set_transaction_status(queue_item, is_successful, exception_information, output)
            else:
                r.raise_for_status()
        return