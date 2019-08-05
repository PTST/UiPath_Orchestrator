from BaseAPI import BaseAPI
from subclasses.Asset import Asset, RobotValue
import requests
import re
import json


class Assets(BaseAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Asset = Asset
        self.RobotValue = RobotValue
        self.regex = re.compile(r"(?<!^)([A-Z])")

    def get_assets(self, organization_unit):
        url = f"{self.base_url}/odata/Assets"
        headers = {
            "Authorization": self.auth_token,
            "X-UIPATH-OrganizationUnitId": str(organization_unit.id)
        }
        params = {
            "$expand": "RobotValues"
        }
        r = requests.get(url, headers=headers, params=params, verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self.get_assets(organization_unit)
            else:
                r.raise_for_status()
        return [self.json_to_asset(x) for x in r.json()["value"]]

    def get_asset(self, asset_name, organization_unit):
        matches = [asset for asset in self.get_assets(organization_unit) if asset.name.lower() == asset_name.lower()]
        if len(matches) == 0:
            raise ValueError("No asset found by that name")
        return matches[0]
    
    def create_asset(self, asset, organization_unit):
        url = f"{self.base_url}/odata/Assets"
        headers = {
            "Authorization": self.auth_token,
            "X-UIPATH-OrganizationUnitId": str(organization_unit.id)
        }
        r = requests.post(url, headers=headers, json=asset.to_json(), verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self.create_asset(asset, organization_unit)
            else:
                r.raise_for_status()

    def delete_asset(self, asset, organization_unit):
        url = f"{self.base_url}/odata/Assets({asset.id})"
        headers = {
            "Authorization": self.auth_token,
            "X-UIPATH-OrganizationUnitId": str(organization_unit.id)
        }
        r = requests.delete(url, headers=headers, verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self.delete_asset(asset, organization_unit)
            else:
                r.raise_for_status()

    def update_asset(self, asset, organization_unit):
        url = f"{self.base_url}/odata/Assets({asset.id})"
        headers = {
            "Authorization": self.auth_token,
            "X-UIPATH-OrganizationUnitId": str(organization_unit.id)
        }
        r = requests.put(url, json=asset.to_json(), headers=headers, verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self.delete_asset(asset, organization_unit)
            else:
                print(r.text)
                print("")
                print(json.dumps(asset.to_json(), indent=2))
                r.raise_for_status()
    
    def json_to_asset(self, data):
        kwargs = {}
        keys = list(data)
        for key in keys:
            new_key = self.regex.sub(r"_\1", key).lower()
            kwargs[new_key] = data.pop(key)
        kwargs["asset_id"] = kwargs.pop("id")
        return self.Asset(**kwargs)