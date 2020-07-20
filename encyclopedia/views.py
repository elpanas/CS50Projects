from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from . import util
import random
import markdown2

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    content = forms.CharField(label="Entry Content", widget=forms.Textarea())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show_entry(request, entry):
    if check_entry(entry):      
        return render(request, "encyclopedia/entries.html", {
            "entry_name": entry.upper(),
            "entry_body": markdown2.markdown(util.get_entry(f"{entry}")),
            "entry_edit": entry.upper()
        })
    else:
        return render(request, "encyclopedia/error.html")

# render the result page
def show_search(request):
    entry = request.POST["q"]

    if check_entry(entry):
        return HttpResponseRedirect(f"{entry}")
    else:
        result = check_partial_result(entry)
        if len(result) > 0:
            return render(request, "encyclopedia/search.html", {
                "result": result
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "error": "Entry not found"
            })

def show_new(request):  
    if request.method == "POST":
        entryform = NewEntryForm(request.POST)
        if entryform.is_valid():
            title = entryform.cleaned_data["title"]
            if check_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "error": "Entry already exists"
                })
            else:
                content = entryform.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(f"{title}")
        else:
            return render(request, "encyclopedia/new.html", {
                "form": entryform
            })
        
    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })

def show_edit(request, entry):  
    if request.method == "POST":
        entryform = NewEntryForm(request.POST)
        if entryform.is_valid():         
            title = entryform.cleaned_data["title"]
            content = entryform.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f"../../../wiki/{title}")
    else:  
        return render(request, "encyclopedia/edit.html", {
            "entry_name": entry,
            "entry_body": util.get_entry(f"{entry}")            
        })

def show_random(request):
    r_entry = random.choice(util.list_entries())
    return HttpResponseRedirect(f"{r_entry}")

# check if the partial entry has a corrisponding one in the list
def check_partial_result(name):
    name = name.lower()
    result = []

    for entry in util.list_entries():
        entry = entry.lower()
        if name in entry:
            result.append(entry)

    return result

# check if the entry is in the list
def check_entry(name):
    for entry in util.list_entries():
        if name.lower() == entry.lower():
            return True

    return False