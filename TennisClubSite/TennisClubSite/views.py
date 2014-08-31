from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from ladder.models import PlayerProfile,Match
from django.template import RequestContext, loader


def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def about(request):
    template = loader.get_template('about.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def news(request):
    template = loader.get_template('news.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def roster(request):
    template = loader.get_template('roster.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def faq(request):
    template = loader.get_template('faq.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def media(request):
    template = loader.get_template('media.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def contact(request):
    template = loader.get_template('contact.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
