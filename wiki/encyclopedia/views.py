from django import forms
from django.shortcuts import render, redirect


from . import util
 
import markdown2
import random

class NewWiki(forms.Form):
    title = forms.CharField(label=False, widget=forms.TextInput(attrs={"placeholder": "Enter Title"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter Markdown content"}), label=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "title": "All Pages",
        "entries": util.list_entries()
    })
def title(request, entry):
    content = util.get_entry(entry)
    if content is not None:
        return render(request, "encyclopedia/title.html", {
            "page": markdown2.markdown(content),
            "entry": entry
        })
    else:
        return render(request, "encyclopedia/404.html")
def search(request):
    if request.method == "GET":
        search = request.GET.get("q")
        entry = util.get_entry(search)
        if entry is not None:
            return redirect(title, search)
        else:
            return render(request, "encyclopedia/index.html", {
                "title": "Search Results",
                "entries": util.search_substring(search)
            })
def newpage(request):
    if request.method == "POST":
        form = NewWiki(request.POST)
        new_page_title = form.data["title"]
        new_page_content = form.data["content"]
        if new_page_title.lower() in (entry.lower() for entry in util.list_entries()):
            return render_form(request, form, error="Title exsits already!") 
        else:
            util.save_entry(new_page_title, new_page_content)
            return redirect(title, new_page_title)
    else:
        return render_form(request, NewWiki())
def editpage(request):
    if request.method == "POST":
        form = NewWiki(request.POST)
        new_page_title = form.data["title"]
        new_page_content = form.data["content"]
        util.save_entry(new_page_title, new_page_content)
        return redirect(title, new_page_title)
    else:
        entry_title = request.GET.get('entry')
        entry_content = util.get_entry(entry_title)
        form = NewWiki({
            "title": entry_title,
            "content": entry_content
        })
        form.fields["title"].widget.attrs["readonly"] = True
        return render_form(request, form)
def randompage(request):
    return redirect(title, random.choice(util.list_entries()))

def render_form(request, form, error=""):
    return render(request, "encyclopedia/newpage.html", {
        "form": form,
        "error": error
    })


