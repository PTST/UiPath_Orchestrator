from subclasses.initializer import comparable, represent
import re



@comparable
class RobotValue(object):
    def __init__(self,
                 robot_id,
                 value,
                 value_type,
                 robot_name=None,
                 key_trail=None,
                 string_value="",
                 bool_value=False,
                 int_value=0,
                 credential_username="",
                 credential_password="",
                 robot_value_id=None,
                 key_value_list=[]):
        if value_type not in ["Text", "Bool", "Integer", "Credential"]:
            raise ValueError("Onlt value_types of 'Text', 'Bool', 'Integer', or 'Credential' is allowed")
        self.robot_id = robot_id
        self.robot_name = robot_name
        self.key_trail = key_trail
        self.value_type = value_type
        self.string_value = string_value
        self.bool_value = bool_value
        self.int_value = int_value
        self.value = value
        self.credential_username = credential_username
        self.credential_password = credential_password
        self.id = robot_value_id
        self.key_value_list = key_value_list
    
    def to_json(self):
        if self.value_type == "Credential":
            self.string_value = ""
            self.value = f"username: {self.credential_username}"
        elif self.value_type == "Text":
            self.string_value = self.value
        elif self.value_type == "Bool":
            self.bool_value = self.value
        elif self.value_type == "Integer":
            self.int_value = self.value

        return {
            "RobotId": self.robot_id,
			"ValueType": self.value_type,
			"StringValue": self.string_value,
			"BoolValue": self.bool_value,
			"IntValue": self.int_value,
			"Value": self.value,
			"CredentialUsername": self.credential_username,
			"CredentialPassword": self.credential_password,
			"KeyValueList": self.key_value_list
        }


class Asset(object):
    def __init__(self, name,
                 value,
                 value_type,
                 can_be_deleted=True,
                 value_scope="Global",
                 string_value="",
                 bool_value=False,
                 int_value=0,
                 credential_username="",
                 credential_password="",
                 asset_id=0,
                 key_value_list=[],
                 robot_values=[]):

        if value_type not in ["Text", "Bool", "Integer", "Credential"]:
            raise ValueError("Onlt value_types of 'Text', 'Bool', 'Integer', or 'Credential' is allowed")
        
        self.name = name
        self.can_be_deleted = can_be_deleted
        self.value_scope = value_scope
        self.value_type = value_type
        self.value = value
        self.string_value = string_value
        self.bool_value = bool_value
        self.int_value = int_value
        self.credential_username = credential_username
        self.credential_password = credential_password
        self.id = asset_id
        self.key_value_list = key_value_list
        self.robot_values = robot_values

        self.regex = re.compile(r"(?<!^)([A-Z])")

        if robot_values and len(robot_values) > 0 and not isinstance(robot_values[0], RobotValue):
            self.robot_values = [self.create_robot_value(x) for x in self.robot_values]

        
                

    def create_robot_value(self, data):
        kwargs = {}
        keys = list(data)
        for key in keys:
            new_key = self.regex.sub(r"_\1", key).lower()
            kwargs[new_key] = data.pop(key)
        kwargs["robot_value_id"] = kwargs.pop("id")
        return RobotValue(**kwargs)

    def to_json(self):
        if self.value_type == "Credential":
            self.string_value = ""
            self.value = f"username: {self.credential_username}"
        elif self.value_type == "Text":
            self.string_value = self.value
        elif self.value_type == "Bool":
            self.bool_value = self.value
        elif self.value_type == "Integer":
            self.int_value = self.value

        if len(self.robot_values) > 0:
            self.value_scope = "PerRobot"

        data = {
            "Id": self.id,
            "Name": self.name,
            "CanBeDeleted": self.can_be_deleted,
            "ValueScope": self.value_scope,
            "ValueType": self.value_type,
            "Value": str(self.value),
            "StringValue": self.string_value,
            "BoolValue": self.bool_value,
            "IntValue": self.int_value,
            "CredentialUsername": self.credential_username,
            "CredentialPassword": self.credential_password,
            "KeyValueList": self.key_value_list,
            "RobotValues": [x.to_json() for x in self.robot_values]
        }
        return data

if __name__ == "__main__":
    asset = Asset("test", "test", "Credential")
    print(asset)