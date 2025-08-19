from django.http import JsonResponse
from django.conf import settings
from django.db import connection
from django.db.utils import OperationalError


def health(request):
    details = {}
    ok = True
    error_message = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
    except OperationalError as exc:
        ok = False
        error_message = str(exc)

    db_settings = settings.DATABASES.get('default', {})
    details['database'] = {
        'ok': ok,
        'engine': db_settings.get('ENGINE'),
        'name': db_settings.get('NAME'),
        'host': db_settings.get('HOST'),
        'port': db_settings.get('PORT'),
        'error': error_message,
    }

    # Optional: include simple counts when DB is OK
    if ok:
        try:
            from apps.lectures.models import Lecture, LectureCategory
            details['counts'] = {
                'lectures': Lecture.objects.count(),
                'lecture_categories': LectureCategory.objects.count(),
            }
        except Exception:
            pass

    return JsonResponse(details)


