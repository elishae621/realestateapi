from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
from main import serializers
from rest_framework import viewsets
from django.db.models.functions import Random
from django_filters import rest_framework as filters
from main import models
from main.filters import PropertyFilter, AgentFilter, SchoolFilter, NeighborhoodFilter
import random
import requests


# connect scrapyd service
scrapyd = ScrapydAPI("http://localhost:6800")


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url) 
    except ValidationError:
        return False

    return True


PropertyAgentStrings = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
]


class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Property.objects.order_by(Random())
    lookup_field = "slug"
    serializer_class = serializers.PropertySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PropertyFilter

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class AgentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Agent.objects.order_by(Random())
    lookup_field = "slug"
    serializer_class = serializers.AgentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AgentFilter

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.School.objects.order_by(Random())
    lookup_field = "slug"
    serializer_class = serializers.SchoolSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SchoolFilter

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class NeighborhoodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Neighborhood.objects.order_by(Random())
    lookup_field = "slug"
    serializer_class = serializers.NeighborhoodSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = NeighborhoodFilter()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


def scrapUrlView(request):
    response = requests.post(
        f"{request._current_scheme_host}/crawl/",
        data={"url": request.GET.get("url", None)},
    )
    return HttpResponse(response.text, content_type="json")

def cancel(request):
    jobs = scrapyd.list_jobs('default')
    count = 0
    for job in jobs['pending']:
        scrapyd.cancel('default', job.id)
        count += 1
    for job in jobs['running']:
        scrapyd.cancel('default', job['id'])
        count += 1
    return HttpResponse(f"{count} jobs cancelled")

@csrf_exempt
@require_http_methods(["POST", "GET"])  # only get and post
def crawl(request):
    # Post requests are for new crawling tasks
    if request.method == "POST":
        url = request.POST.get(
            "url", None
        )  # take url comes from client. (From an input may be?)

        if not url:
            return JsonResponse({"error": "Missing  args"})

        if not is_valid_url(url):
            return JsonResponse({"error": "URL is invalid"})

        domain = urlparse(url).netloc  # parse the url and extract the domain
        unique_id = str(uuid4())  # create a unique ID.

        # This is the custom settings for scrapy spider.
        # We can send anything we want to use it inside spiders and pipelines.
        # I mean, anything
        settings = {
            "unique_id": unique_id,  # unique ID for each record for DB
            "Property_AGENT": random.choice(PropertyAgentStrings),
        }

        # Here we schedule a new crawling task from scrapyd.
        # Notice that settings is a special argument name.
        # But we can pass other arguments, though.
        # This returns a ID which belongs and will be belong to this task
        # We are goint to use that to check task's status.
        task = scrapyd.schedule(
            "default", "realtorspider", settings=settings, url=url, domain=domain
        )

        return JsonResponse(
            {"task_id": task, "unique_id": unique_id, "status": "started"}
        )

    # Get requests are for getting result of a specific crawling task
    elif request.method == "GET":
        # We were passed these from past request above. Remember ?
        # They were trying to survive in client side.
        # Now they are here again, thankfully. <3
        # We passed them back to here to check the status of crawling
        # And if crawling is completed, we respond back with a crawled data.
        task_id = request.GET.get("task_id", None)
        unique_id = request.GET.get("unique_id", None)

        if not task_id or not unique_id:
            return JsonResponse({"error": "Missing args"})

        # Here we check status of crawling that just started a few seconds ago.
        # If it is finished, we can query from database and get results
        # If it is not finished we can return active status
        # Possible results are -> pending, running, finished
        status = scrapyd.job_status("default", task_id)
        if status == "finished":
            try:
                # this is the unique_id that we created even before crawling started.
                item = models.Property.objects.get(unique_id=unique_id)
                return JsonResponse({"data": item.to_dict["data"]})
            except Exception as e:
                return JsonResponse({"error": str(e)})
        else:
            return JsonResponse({"status": status})
