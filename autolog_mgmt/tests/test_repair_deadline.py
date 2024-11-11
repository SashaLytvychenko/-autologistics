from datetime import datetime, timedelta
from odoo.addons.autolog_mgmt.tests.common import TestPatientCommon
from odoo.tests import tagged


@tagged('post_install', '-at_install', 'repair_deadline')
class TestRepairDeadlineMethods(TestPatientCommon):

    def test_01_check_repair_deadline(self):

        self.repair_deadline.repair_start_date = datetime.today().date()
        self.repair_deadline.priority = '1'  # Low priority

        self.repair_deadline._deadline()

        expected_end_date = self.repair_deadline.repair_start_date + timedelta(
            days=2)

        self.assertEqual(self.repair_deadline.repair_end_date,
                         expected_end_date,
                         "Repair end date should be 2 days after start date "
                         "for 'Low' priority")
