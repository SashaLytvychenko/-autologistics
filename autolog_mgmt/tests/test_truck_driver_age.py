from datetime import datetime, timedelta
from odoo.addons.autolog_mgmt.tests.common import TestPatientCommon
from odoo.tests import tagged
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install', 'driver')
class TestPatientMethods(TestPatientCommon):

    def test_01_check_date_birth(self):
        with self.assertRaises(ValidationError):
            self.driver.date_birth = datetime.today() + timedelta(days=1)
            self.driver._check_date_birth()
