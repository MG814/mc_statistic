import graphene


class DoctorStatsType(graphene.ObjectType):
    salary = graphene.Float()
    unique_patients = graphene.Int()
    all_visits = graphene.Int()
    number_paid_visits = graphene.Int()
    number_not_paid_visits = graphene.Int()
    percentage_paid_visits = graphene.Float()
    monthly_visit_count = graphene.Int()