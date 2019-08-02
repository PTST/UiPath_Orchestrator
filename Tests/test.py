import unittest
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from Orchestrator import Orchestrator
import os
import time
from datetime import datetime
import json

URL = os.environ["UIP_URL"]
USER = os.environ["UIP_USER"]
PASSWORD = os.environ["UIP_PASSWORD"]


class OrchestratorTest(unittest.TestCase):

    def setUp(self):
        self.uip = Orchestrator(URL, USER, PASSWORD, False)

    # def test_users(self):
    #     org_unit = self.uip.organization_units.get("TnDK-Operations")
    #     ptst_users = self.uip.users.get_user(username="PTST", organization_unit=org_unit)
    #     self.assertTrue(len(ptst_users) > 0)
    #     self.assertTrue(len(self.uip.users.get_user(username="PTSD", organization_unit=org_unit)) == 0)
        

    # def test_get_queues(self):
    #     org_unit = self.uip.organization_units.get("TnDK-Operations")
    #     queue = self.uip.queues.Get_Queue("Create", org_unit)
    #     queue_items = self.uip.queues.Get_Queue_Items(queue, top=5)
    #     self.assertTrue(len(queue_items) == 5)
    #     with self.assertRaises(ValueError):
    #         self.uip.queues.Get_Queue("Master Of The Universe", org_unit)
    #     output_based = self.uip.queues.search_queue_items(queue, output_data={"test": "test2"})
    #     self.assertTrue(len(output_based) > 0)
    #     date_based = self.uip.queues.search_queue_items(queue, end_processing_greater_than=datetime(2019, 7, 30))
    #     self.assertTrue(len(date_based) > 0)
    #     date_status_based = self.uip.queues.search_queue_items(queue, statuses=["Successful"], end_processing_greater_than=datetime(2018, 6, 13))
    #     self.assertTrue(len(date_status_based) > 0)
    
    # def test_add_delete_queue_item(self):
    #     org_unit = self.uip.organization_units.get("TnDK-Operations")
    #     queue = self.uip.queues.Get_Queue("Test", org_unit)
    #     queue_item = self.uip.queues.add_queue_item(queue,
    #         specific_data={"TicketNo": "Test"},
    #         priority="Low",
    #         due_date=datetime(2019, 12, 31),
    #         defer_date=datetime(2019, 12, 1),
    #         reference="TestTicket")
    #     self.uip.queues.delete_queue_item(queue_item)
        
    # def test_set_transaction_status(self):
    #     org_unit = self.uip.organization_units.get("TnDK-Operations")
    #     queue = self.uip.queues.Get_Queue("Create", org_unit)
    #     queue_item = self.uip.queues.search_queue_items(queue, reference="test")[0]
    #     self.uip.queues.set_transaction_status(queue_item, True, output={"test": "test2"})
    #     exception = self.uip.queues.ProcessingException(reason="Fordi jeg siger det", exception_type="BusinessException", creation_time=datetime.now())
    #     self.uip.queues.set_transaction_status(queue_item, False, exception_information=exception)

    # def test_assets(self):
    #     org_unit = self.uip.organization_units.get("TnDK-Operations")
    #     assets = self.uip.assets.get_assets(org_unit)
    
    # def test_create_update_delete_asset(self):
    #     org_unit = self.uip.organization_units.get("TnDK-Operations")
    #     robot_values = [self.uip.assets.RobotValue(36, "Test", "Credential", credential_username="admin", credential_password="Password123")]
    #     asset = self.uip.assets.Asset(name="Test_Cred", value="Test", value_type="Credential", robot_values=robot_values)
    #     self.uip.assets.create_asset(asset, org_unit)
    #     asset = self.uip.assets.get_asset("Test_Cred", org_unit)
    #     asset.name = "Test_Cred_Updated"
    #     self.uip.assets.update_asset(asset, org_unit)
    #     self.uip.assets.delete_asset(asset, org_unit)
        

    # def test_robots(self):
    #     org_unit = self.uip.organization_units.get("TnDK-Operations")
    #     print(self.uip.robots.get_robots(org_unit))
    
    def test_create_delete_environment(self):
        org_unit = self.uip.organization_units.get("TnDK-Operations")
        env = self.uip.environments.Environment("Test_PTST", "Test", "Dev", org_unit)
        robots = self.uip.robots.get_robots(org_unit)
        new_env = self.uip.environments.create_environment(env, robots)
        self.uip.environments.delete_environment(new_env)
    

if __name__ == '__main__':
    unittest.main(verbosity=2)