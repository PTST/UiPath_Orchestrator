from Queues import Queues
from OrganizationUnits import OrganizationUnits
from Users import Users
from Assets import Assets
from Environments import Environments
from Robots import Robots

class Orchestrator(object):
    def __init__(self, base_url, username, password, verify_ssl=True):
        api_args = {
            "base_url": base_url,
            "username": username,
            "password": password,
            "verify_ssl": verify_ssl
        }
        self.queues = Queues(**api_args)
        self.users = Users(**api_args)
        self.organization_units = OrganizationUnits(**api_args)
        self.assets = Assets(**api_args)
        self.robots = Robots(**api_args)
        self.environments = Environments(**api_args)


if __name__ == "__main__":
    pass
