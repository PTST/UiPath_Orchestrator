import requests

class BaseAPI(object):
    def __init__(self, base_url, username, password, verify_ssl=True):
        self.base_url = base_url
        if self.base_url[-1] == "/":
            self.base_url = self.base_url[:-1]

        self.user = username
        self.password = password
        self.verify_ssl = verify_ssl
        if not self.verify_ssl:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.Authenticate()

    def Authenticate(self):
        """Authenticates with the Orchestrator instance and gets the bearer token used for all further API calls
        """
        url = f"{self.base_url}/api/Account"
        payload = {
            "usernameOrEmailAddress": self.user,
            "password": self.password
        }
        r = requests.post(url, json=payload, verify=self.verify_ssl)
        if not r.ok:
            r.raise_for_status()
        self.auth_token = f"Bearer {r.json()['result']}"
        return self.auth_token

if __name__ == "__main__":
    import os
    url = os.environ["UIP_URL"]
    user = os.environ["UIP_USER"]
    password = os.environ["UIP_PASSWORD"]
    uip = BaseAPI(url, user, password, False)