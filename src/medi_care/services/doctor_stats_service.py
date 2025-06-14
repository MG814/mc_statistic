import requests

from django.conf import settings

from dateutil.parser import parse

from ..types import DoctorStatsType


def doctor_stats_service(doctor_id, start_date, end_date):
    response = requests.get(f'{settings.VISITS_SERVICE_URL}/visits/doctor/{doctor_id}/', timeout=10)
    visits = response.json()

    paid_visits_count = 0
    not_paid_visits_count = 0
    salary = 0.0
    unique_patient_ids = set()
    monthly_visits_count = 0
    all_visits_count = 0

    for visit in visits:
        if start_date and end_date:
            visit_date = parse(visit['date'])
            if start_date <= visit_date.date() <= end_date:
                unique_patient_ids.add(visit['patient_id'])
                all_visits_count += 1

                if visit.get('is_paid'):
                    paid_visits_count += 1
                    salary += float(visit['price'])
                    monthly_visits_count += 1
                else:
                    not_paid_visits_count += 1

    percentage_paid_visits = round(paid_visits_count / all_visits_count * 100 if all_visits_count > 0 else 0, 2)

    return DoctorStatsType(
        salary=salary,
        unique_patients=len(unique_patient_ids),
        all_visits=all_visits_count,
        number_paid_visits=paid_visits_count,
        number_not_paid_visits=not_paid_visits_count,
        percentage_paid_visits=percentage_paid_visits,
        monthly_visit_count=monthly_visits_count
    )