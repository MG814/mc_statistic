import graphene
from ..types import DoctorStatsType
from ..services.doctor_stats_service import doctor_stats_service


class DoctorStatsQuery(graphene.ObjectType):
    doctor_stats = graphene.Field(DoctorStatsType, doctor_id=graphene.ID(required=True),
                                  start_date=graphene.Date(),
                                  end_date=graphene.Date()
                                  )

    def resolve_doctor_stats(self, info, doctor_id, start_date=None, end_date=None):
        return doctor_stats_service(doctor_id, start_date, end_date)
