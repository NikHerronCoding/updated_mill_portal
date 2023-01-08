from .models import MillProcedure


def get_obj():
    return MillProcedure.objects.all()[0]