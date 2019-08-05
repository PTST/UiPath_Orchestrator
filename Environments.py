import re
import requests
from BaseAPI import BaseAPI
from subclasses.Environment import Environment

class Environments(BaseAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Environment = Environment
        self.regex = re.compile(r"(?<!^)([A-Z])")

    def get_environments(self, organization_unit):
        url = f"{self.base_url}/odata/Environments"
        headers = {
            "Authorization": self.auth_token,
            "X-UIPATH-OrganizationUnitId": str(organization_unit.id)
        }
        r = requests.get(url, headers=headers, verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self.get_environments(organization_unit)
            else:
                r.raise_for_status()
        return [self.json_to_environment(x, organization_unit) for x in r.json()["value"]]
        

    def json_to_environment(self, data, organization_unit):
        kwargs = {}
        keys = list(data)
        for key in keys:
            new_key = self.regex.sub(r"_\1", key).lower()
            kwargs[new_key] = data.pop(key)
        kwargs["environment_type"] = kwargs.pop("type")
        kwargs["environment_id"] = kwargs.pop("id")
        kwargs["organization_unit"] = organization_unit
        if "@odata.context" in kwargs:
            kwargs.pop("@odata.context")
        return self.Environment(**kwargs)

    def create_environment(self, environment, robots):
        url = f"{self.base_url}/odata/Environments"
        payload = environment.to_json()
        payload["Robots"] = [robot.to_json() for robot in robots]
        headers = {
            "Authorization": self.auth_token,
            "X-UIPATH-OrganizationUnitId": str(environment.organization_unit.id)
        }
        r = requests.post(url, headers=headers, json=payload, verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self.create_environment(environment, robots)
            else:
                r.raise_for_status()
        return self.json_to_environment(r.json(), environment.organization_unit)

    def delete_environment(self, environment):
        url = f"{self.base_url}/odata/Environments({environment.id})"
        headers = {
            "Authorization": self.auth_token,
            "X-UIPATH-OrganizationUnitId": str(environment.organization_unit.id)
        }
        r = requests.delete(url, headers=headers, verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self.delete_environment(environment)
            else:
                r.raise_for_status()
        return
