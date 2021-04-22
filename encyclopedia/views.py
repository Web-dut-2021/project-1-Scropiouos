from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from . import util
import random
import markdown2
import re

def decorate(html,title):
    style="<html lang=\"zh\"><head><link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css\" integrity=\"sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh\" crossorigin=\"anonymous\">"
    style=style+"<style>body {margin: 0;background-color: white;}code {white-space: pre;}h1 {margin-top: 0px;padding-top: 20px;}textarea {height: 90vh;width: 80%;}.main {padding: 10px;}.search {width: 100%;font-size: 15px;line-height: 15px;}.sidebar {background-color: #f0f0f0;height: 100vh;padding: 20px;}.sidebar h2 {margin-top: 5px;}</style></head>"
    style=style+"<body><div class=\"row\"><div class=\"sidebar col-lg-2 col-md-3\"><h2>Wiki</h2><form action=\"http://127.0.0.1:8000/search/\" method=\"post\"><input class=\"search\" type=\"text\" name=\"title\" placeholder=\"Search Encyclopedia\"></form><div><a href=\"/\">Home</a></div><div><a href=\"/create/\">New Page</a></div><div><a href=\"/random/\">Random Page</a></div></div><div class=\"main col-lg-10 col-md-9\">"
    html=style+html+"<form action=\"http://127.0.0.1:8000/edit/\" method=\"post\"><input type=\"hidden\" name=\"title\" value=\""+title+"\"><input type=\"submit\" value=\"Edit\"><input type=\"hidden\" name=\"flag\" value=\""+"0"+"\"></form></div></body></html>"
    return html

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def detail(request,title):
    content=util.get_entry(title)
    if content is None:
        return render(request,"encyclopedia/error.html",{"message":"INVALID TITLE!"})
    html=markdown2.markdown(content)
    #html=html+"<form action=\"{% url 'edit' %}\" method=\"post\"><input type=\"hidden\" name=\"title\" value=\""+title+"\"><input type=\"submit\" value=\"Submit\"></form>"
    html=decorate(html,title)
    return HttpResponse(html)
    #return render(request,"encyclopedia/detail.html",{"title":title,"content":content})

def randoms(request):
    titles=util.list_entries()
    title=random.choice(titles)
    return detail(request,title)

def create(request):
    if request.POST.get("title") is None:
        return render(request,"encyclopedia/create.html")
    if request.POST["title"] in util.list_entries():
        return render(request,"encyclopedia/error.html",{"message":"DUPLICATE TITLE!"})
    title=request.POST["title"]
    content=request.POST["content"]
    content="# "+title+"\r\n"+content
    util.save_entry(title, content)
    content=util.get_entry(title)
    html=markdown2.markdown(content)
    html=decorate(html,title)
    return HttpResponse(html)
    #return HttpResponseRedirect(reverse("index"))

def edit(request):
    if request.POST.get("flag") is "0":
        title=request.POST["title"]
        content=util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{"title":title,"content":content})
    title=request.POST["title"]
    content=request.POST["content"]
    #content="# "+title+"\r\n"+content
    util.save_entry(title, content)
    content=util.get_entry(title)
    html=markdown2.markdown(content)
    html=decorate(html,title)
    return HttpResponse(html)

def search(request):
    title=request.POST.get("title")
    entries=util.list_entries()
    if title in entries:
        return detail(request,title)
    items=[]
    for entry in entries:
        if re.search(title,entry) is not None:
            items.append(entry)
    return render(request,"encyclopedia/index.html",{"entries": items})
    

    
