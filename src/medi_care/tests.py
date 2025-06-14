from unittest.mock import patch, Mock
from datetime import date
from django.test import TestCase
from django.conf import settings

from .services.doctor_stats_service import doctor_stats_service


class DoctorStatsServiceTests(TestCase):

    @patch('requests.get')
    def test_basic_stats_calculation(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'patient_id': 1,
                'date': '2024-01-15T10:00:00Z',
                'price': '100.00',
                'is_paid': True
            },
            {
                'patient_id': 2,
                'date': '2024-01-20T14:00:00Z',
                'price': '150.00',
                'is_paid': False
            }
        ]
        mock_get.return_value = mock_response

        result = doctor_stats_service(
            doctor_id=1,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31)
        )

        self.assertEqual(result.salary, 100.0)
        self.assertEqual(result.unique_patients, 2)
        self.assertEqual(result.all_visits, 2)
        self.assertEqual(result.number_paid_visits, 1)
        self.assertEqual(result.number_not_paid_visits, 1)
        self.assertEqual(result.percentage_paid_visits, 50.0)
        self.assertEqual(result.monthly_visit_count, 1)

    @patch('requests.get')
    def test_visits_outside_date_range(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'patient_id': 1,
                'date': '2024-01-15T10:00:00Z',
                'price': '100.00',
                'is_paid': True
            },
            {
                'patient_id': 2,
                'date': '2024-02-15T10:00:00Z',
                'price': '200.00',
                'is_paid': True
            }
        ]
        mock_get.return_value = mock_response

        result = doctor_stats_service(
            doctor_id=1,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31)
        )

        self.assertEqual(result.unique_patients, 1)
        self.assertEqual(result.all_visits, 1)
        self.assertEqual(result.salary, 100.0)

    @patch('requests.get')
    def test_empty_visits_list(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        result = doctor_stats_service(
            doctor_id=1,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31)
        )

        self.assertEqual(result.salary, 0.0)
        self.assertEqual(result.unique_patients, 0)
        self.assertEqual(result.all_visits, 0)
        self.assertEqual(result.number_paid_visits, 0)
        self.assertEqual(result.number_not_paid_visits, 0)
        self.assertEqual(result.percentage_paid_visits, 0)
        self.assertEqual(result.monthly_visit_count, 0)

    @patch('requests.get')
    def test_all_visits_unpaid(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'patient_id': 1,
                'date': '2024-01-15T10:00:00Z',
                'price': '100.00',
                'is_paid': False
            },
            {
                'patient_id': 2,
                'date': '2024-01-20T14:00:00Z',
                'price': '150.00',
                'is_paid': False
            }
        ]
        mock_get.return_value = mock_response

        result = doctor_stats_service(
            doctor_id=1,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31)
        )

        self.assertEqual(result.salary, 0.0)
        self.assertEqual(result.number_paid_visits, 0)
        self.assertEqual(result.number_not_paid_visits, 2)
        self.assertEqual(result.percentage_paid_visits, 0.0)
        self.assertEqual(result.monthly_visit_count, 0)

    @patch('requests.get')
    def test_api_call_made_correctly(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        doctor_id = 123
        doctor_stats_service(
            doctor_id=doctor_id,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31)
        )

        response_url = f'{settings.VISITS_SERVICE_URL}/visits/doctor/{doctor_id}/'
        mock_get.assert_called_once_with(response_url, timeout=10)