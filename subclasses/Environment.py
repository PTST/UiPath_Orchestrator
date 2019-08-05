from subclasses.initializer import comparable

@comparable
class Environment(object):
    def __init__(self, name, description, environment_type, organization_unit, environment_id = 0):
        self.name = name
        self.description = description
        self.type = environment_type
        self.id = environment_id
        self.organization_unit = organization_unit

    def to_json(self):
        return {
            "Name": self.name,
            "Description": self.description,
            "Type": self.type,
            "Id": self.id
        }