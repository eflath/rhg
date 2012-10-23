from django.http import HttpResponse
from rhg import Headline


def random_headline(request):
    headline = Headline(type="charity")
    # obit = Obituary()

    page_string = "<html><body>"
    page_string += "<h1>" + headline.main_headline.capitalize() + "</h1>"
    page_string += "<p>" + headline.blurb + "</p>"
    page_string += "<p>-----------------</p>"
    # page_string += "<h1>" + obit.headline.capitalize() + "</h1>"
    # page_string += "<p>" + obit.full_text.capitalize() + "</p>"
    page_string += "</html></body>"
    return HttpResponse(page_string)
