import requests
from BaseAPI import BaseAPI
from subclasses.OrganizationUnit import OrganizationUnit

class OrganizationUnits(BaseAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.OrganizationUnit = OrganizationUnit
        self.organization_units = self._get()

    def _get(self):
        url = f"{self.base_url}/odata/OrganizationUnits"
        headers = {"Authorization": self.auth_token}
        r = requests.get(url, headers=headers, verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self._get()
            else:
                r.raise_for_status()
        org_units = [self.OrganizationUnit(x["DisplayName"], x["Id"]) for x in r.json()["value"]]
        return org_units

    def get(self, display_name):
        filtered_org_units = [x for x in self.organization_units if x.display_name.lower() == display_name.lower()]
        if len(filtered_org_units) == 0:
            self.org_units = self._get()
            filtered_org_units = [x for x in self.organization_units if x.display_name.lower() == display_name.lower()]
            if len(filtered_org_units) == 0:
                raise ValueError("No organization unit by that name")
        return filtered_org_units[0]
