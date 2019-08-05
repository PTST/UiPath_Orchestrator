import re
import requests
from BaseAPI import BaseAPI
from subclasses.Robot import Robot
from Environments import Environments

class Robots(BaseAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Robot = Robot
        self.regex = re.compile(r"(?<!^)([A-Z])")
        self._environments = Environments(**kwargs)

    def get_robots(self, organization_unit):
        url = f"{self.base_url}/odata/Robots"
        headers = {
            "Authorization": self.auth_token,
            "X-UIPATH-OrganizationUnitId": str(organization_unit.id)
        }
        r = requests.get(url, headers=headers, verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self.get_robots(organization_unit)
            else:
                r.raise_for_status()
        return [self.json_to_robot(x, organization_unit) for x in r.json()["value"]]

    def json_to_robot(self, data, organization_unit):
        kwargs = {}
        keys = list(data)
        for key in keys:
            new_key = self.regex.sub(r"_\1", key).lower()
            kwargs[new_key] = data.pop(key)
        kwargs["robot_type"] = kwargs.pop("type")
        kwargs["robot_id"] = kwargs.pop("id")
        kwargs["robot_environments"] = [environment for environment in self._environments.get_environments(organization_unit) if kwargs["robot_environments"] == environment.name]
        return self.Robot(**kwargs)
