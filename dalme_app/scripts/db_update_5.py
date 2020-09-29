from dalme_app.models import *


# fix duplicate credits before adding constraint to db
def step_1():
    credits = Source_credit.objects.all()
    dup_list = []
    for credit in credits:
        self_set = Source_credit.objects.filter(source=credit.source, agent=credit.agent, type=credit.type)
        if self_set.count() > 1:
            dup_list.append(credit.source.id)
            self_set[0].delete()

            # for i in range(self_set.count() - 2):
            #     self_set[i].delete()
    print(len(dup_list))
    return 'Duplicate credits fixed.'
