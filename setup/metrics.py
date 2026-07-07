from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse


def metrics_view(request):
    metrics_page = generate_latest()
    return HttpResponse(metrics_page, content_type=CONTENT_TYPE_LATEST)
