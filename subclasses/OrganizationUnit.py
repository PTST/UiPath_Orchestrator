from subclasses.initializer import initializer, comparable

@comparable
class OrganizationUnit(object):
    @initializer
    def __init__(self, display_name: str, organization_unit_id: int):
        self.id = organization_unit_id