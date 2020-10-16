from django.http import HttpResponse

import rapidapi

api = rapidapi.RapidAPI(namespace="api")


@api.route("route", methods=["GET", "POST"])
def api_route(request):
    return HttpResponse(f"ROUTE:{request.method}")


@api.get("")
def api_get(request):
    return HttpResponse("GET")


@api.head("")
def api_head(request):
    return HttpResponse("")


@api.post("")
def api_post(request):
    return HttpResponse("POST")


@api.put("")
def api_put(request):
    return HttpResponse("PUT")


@api.patch("")
def api_patch(request):
    return HttpResponse("PATCH")


@api.delete("")
def api_delete(request):
    return HttpResponse("DELETE")


@api.options("")
def api_options(request):
    return HttpResponse("OPTIONS")


@api.trace("")
def api_trace(request):
    return HttpResponse("TRACE")
