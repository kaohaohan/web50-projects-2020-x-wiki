from django.shortcuts import render
from markdown2 import Markdown
import encyclopedia.util as util
from django import forms
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import HttpResponse
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# 轉換markdown to html


def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    # 如果內容沒東西return None 有的話markdown內容
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def entry(request, title):
    print('31')
    print('hihihihihihihi')
    print("title", title)
    html_content = convert_md_to_html(title)
    print('html_content', html_content)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            'message': "The requested page was not found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def search(request):
    print('47')
    # If user inputs the query which matchs the name of encyclopedi entry page, it should be redirected to the entry page
    # If query didn't match it, return the massage to the user

    if request.method == "POST":
        entry_search = request.POST.get('q')
     # If query matches an exact entry name, redirect to that entry page
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            # Check every element of our list
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })


def new_page(request):
    # create the link at new page
    # Users can enter a title for the page and should be able to markdown content for the page
    # Create save button
    if request.method == "GET":
        return render(request, 'encyclopedia/new.html')
    else:
        # Get the submitted form data
        title = request.POST["title"]
        content = request.POST["content"]
        # Check if an entry with the same title already exists
        if util.get_entry(title) is not None:
            return render(request, 'encyclopedia/error.html', {
                'message': "The requested page was not exit"
            })
         # Save the new page to the entries list
        else:
            html_content = convert_md_to_html(title)
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })


def edit(request):

    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        print('content', content)
        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'content': content
        })


def save_edit(request):

    if request.method == 'POST':

        title = request.POST['title']

        content = request.POST['content']
        util.save_entry(title, content)

        html_content = convert_md_to_html(title)  # 修正函数调用
        print('html_content:', html_content)
        return render(request, "encyclopedia/entry.html", {
            'title': title,
            'content': html_content  # 修正变量名
        })


def rand(request):
    allentries = util.list_entries()
    rand_entry = random.choice(allentries)
    html_content = convert_md_to_html(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        'title': rand_entry,
        'content': html_content
    })
