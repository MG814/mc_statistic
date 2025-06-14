import graphene

from .queries.doctor_stats import DoctorStatsQuery


class PatientData(graphene.ObjectType):
    name = graphene.String()
    surname = graphene.String()
    email = graphene.String()
    phone = graphene.String()


class Query(DoctorStatsQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
