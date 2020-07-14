from django.shortcuts import render,reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import util
from django.contrib import messages
from django.urls import reverse
import random
import markdown

# it will take the user to the index page of the site
def index(request):
    # it shows the list of entries that we currently have
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# it will take care of the entries like
# wiki/title
def entry(request, title):
    # if the title page exists
    if util.get_entry(title):
        md = markdown.Markdown()
        return render(request, "encyclopedia/entry.html",{
            "content": md.convert(util.get_entry(title)),
            "entry": title
        })

    # if title page doesn't exists
    else:
        return render(request, "encyclopedia/error.html",{
            "error": "Requested Page was not Found"
        })

def search(request):
    # when the user has searched his query 
    if request.method == "POST":
        # value will store the query made by the user
        value = request.POST['q']

        # if the query is already exists
        if util.get_entry(value):
            # then show them that entry
            md = markdown.Markdown()
            return render(request, "encyclopedia/search.html", {
                "content": md.convert(util.get_entry(value)),
                "entry": value,
                "conformation": 1
            })
        else:
            # list to store the entries which are superstring of the
            # substring that we entered in the search bar
            entries = []

            # iterating through all the entries that i
            # currently have
            for entry in util.list_entries():
                # checking that the string we provided is
                # a substring or not
                if value in entry:
                    # storing the superstring entries in the list
                    entries.append(entry)

            # checking that the list is empyt ,i.e.,
            # the string isn't the substring of any entry
            if len(entries) == 0:
                return render(request, "encyclopedia/error.html",{
                    "error": "This page is not in the list! But you can create it!"
                })

            # else giving returning all the entries which are superstring
            # of the string provided by us
            else:
                return render(request, "encyclopedia/search.html", {
                    "content": entries,
                    "entry": value,
                    "conformation": 0
                })
    else:
        # if the user tries to search using get request
        return HttpResponse("""<h2>This is a get request!</h2>
                           <p> You can't reach that page using get request!</p>
                           <div>Please fill out the form</div>""")

# it will create a new entry 
def create(request):
    # if the user clicked on the create new page link
    if request.method == "GET":
        # then take the user to the form
        return render(request, "encyclopedia/create.html")
    
    # when the user had filled the form
    else:
        # store all the entries that we currently have in 
        # the entries variable
        entries = util.list_entries()

        # if the title of the new entry that the user tries to make
        # already exists on our site 
        if request.POST['title'] in entries:
            # then show the user an error 
            return render(request, "encyclopedia/error.html",{
            "error": f"The page with this Title('{request.POST['title']}') already exists!"
            })

        # else save the new entry on our site
        util.save_entry(request.POST['title'], request.POST['content'])

        # it will redirect the user to the page that he just created now
        return HttpResponseRedirect(reverse('entry', args=(request.POST['title'],)))
        
def edit(request, entry):
    # it will contain the content of the entry which already exists
    data = util.get_entry(entry)
    
    # if the user enters the edit page using the link provided 
    # on the entry page of that title
    if request.method == "GET":
        # then return the user to the form which already contains
        # the fixed title and editable content
        return render(request, "encyclopedia/edit.html", {
            "title": entry,
            "content": data,
        })

    # if the user submits the form
    else:
        # else save the new entry on our site
        util.save_entry(entry, request.POST['content'])

        # it will redirect the user to the page that he just edited now
        return HttpResponseRedirect(reverse('entry', args=(entry,)))

def random_page(request):
    # it will contain all the entries that we have 
    entries = util.list_entries()
    
    # title will store the random entry from
    # the list of entries
    title = random.choice(entries)

    # redirecting to the title page
    return HttpResponseRedirect(reverse('entry', args=(title,)))
