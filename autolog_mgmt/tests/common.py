from datetime import datetime, timedelta
from odoo.tests.common import TransactionCase


class TestPatientCommon(TransactionCase):

    def setUp(self):
        super(TestPatientCommon, self).setUp()
        self.driver = self.env['autolog.truck.driver'].create({
            'name': 'Test Truck driver',
            'date_birth': datetime.today() - timedelta(days=365 * 30),
            'truck_number': '12345678',

        })

        self.repair_deadline = self.env['autolog.repair.car'].create({
            'priority': '1',
            'repair_start_date': '2024-11-23',
            'repair_end_date': '2024-11-25'
        })

        self.status = self.env['autolog.receive.car'].create({
            'status': 'draft',
            'vin_code': '1111111',
            'manufacture_date': '2024-10-20'
        })
