from odoo.exceptions import ValidationError
from odoo.addons.autolog_mgmt.tests.common import TestPatientCommon
from odoo.tests import tagged


@tagged('post_install', '-at_install', 'status')
class TestRepairDeadlineMethods(TestPatientCommon):

    def test_01_check_unlink_draft_status(self):
        with self.assertRaises(ValidationError):
            self.status.status = 'in_stock'
            self.status.unlink()

    def test_02_check_unlink_draft_status(self):
        with self.assertRaises(ValidationError):
            self.status.status = 'sent_to_dealer'
            self.status.unlink()

    def test_03_check_unlink_draft_status(self):
        with self.assertRaises(ValidationError):
            self.status.status = 'repair'
            self.status.unlink()
