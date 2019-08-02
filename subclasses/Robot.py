from subclasses.initializer import comparable

@comparable
class Robot(object):
    def __init__(self, license_key, machine_name, name, username, description, robot_type, password, robot_environments, robot_id, execution_settings):
        self.license_key = license_key
        self.machine_name = machine_name
        self.name = name
        self.username = username
        self.description = description
        self.type = robot_type
        self.password = password
        self.robot_environments = robot_environments
        self.execution_settings = execution_settings
        self.id = robot_id
    
    def to_json(self):
        return {
            "LicenseKey": self.license_key,
			"MachineName": self.machine_name,
			"Name": self.name,
			"Username": self.username,
			"Description": self.description,
			"Type": self.type,
			"Password": self.password,
			"RobotEnvironments": ",".join([x.name for x in self.robot_environments]),
			"Id": self.id,
			"ExecutionSettings": self.execution_settings
        }