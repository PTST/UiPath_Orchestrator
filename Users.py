import requests
from BaseAPI import BaseAPI
from OrganizationUnits import OrganizationUnits
from datetime import datetime
from subclasses.User import User

class Users(BaseAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._org_units = OrganizationUnits(**kwargs)
        self.User = User
        self.users = self.get_users()
        self._last_updated = datetime.now()

    def get_users(self):
        url = f"{self.base_url}/odata/Users"
        params = {
            "$expand": "OrganizationUnits"
        }
        headers = {
            "Authorization": self.auth_token
        }
        r = requests.get(url, params=params, headers=headers,
                         verify=self.verify_ssl)
        if not r.ok:
            if r.status_code == 401:
                self.Authenticate()
                return self.get_users()
            else:
                r.raise_for_status()
        users = []
        for user in r.json()["value"]:
            username = user["UserName"]
            name = user["Name"]
            surname = user["Surname"]
            email = user["EmailAddress"]
            roles = user["RolesList"]
            user_id = user["Id"]
            organization_units = [
                self._org_units.get(x["DisplayName"]) for x in user["OrganizationUnits"]]
            users.append(self.User(username, name, surname,
                                    email, roles, organization_units, user_id))
        self.users = users
        self._last_updated = datetime.now()
        return users
    
    def get_user(self, username=None, name=None, surname=None, email=None, role=None, organization_unit=None):
        matches = []
        for user in self.users:
            match = []
            if username:
                match.append(user.username.lower() == username.lower())
            if name:
                match.append(user.name == name.lower())
            if surname:
                match.append(user.surname.lower() == surname.lower())
            if email:
                match.append(user.email.lower() == email.lower())
            if role:
                match.append(role.lower() in [x.lower() for x in user.roles])
            if organization_unit:
                match.append(organization_unit in user.organization_units)
            if match.count(False) == 0:
                matches.append(user)

        if len(matches) == 0 and (datetime.now()-self._last_updated).total_seconds() > 5:
            self.get_users()
            return self.get_user(username, name, surname, email, role, organization_unit)

        return matches
