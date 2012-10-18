from django.http import HttpResponse


def random_headline(request):
    return HttpResponse("Hello world.")
