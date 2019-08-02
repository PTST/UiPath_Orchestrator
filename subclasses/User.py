from typing import List
from subclasses.initializer import initializer, comparable
from subclasses.OrganizationUnit import OrganizationUnit

@comparable
class User(object):
    @initializer
    def __init__(self, username:str, name:str, surname:str, email:str, roles:List[str], organization_units:List[OrganizationUnit], user_id:int):
        self.id = user_id
        self.username = username
        self.email = email

    def __repr__(self):
        return self.username + " - " + self.email