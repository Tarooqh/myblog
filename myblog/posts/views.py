from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .forms import PostForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from .models import posts
# Create your views here.
queryset = posts.objects.all()


def posts_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Content added successfully")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Content not added")
    context = {
        "form":form,
    }

    return render(request, "create.html", context)


def posts_retrieve(request, id=None):
    instance = get_object_or_404(posts, id = id)

    context = {
        "objectlist":queryset,
        'title':'detail',
        "instance": instance,
    }
    return render(request, "detail.html", context)


def posts_update(request, id=None):

    instance = get_object_or_404(posts, id=id)
    form = PostForm(request.POST or None, instance = instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'> Content updated successfully", extra_tags="html_safe")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Content not updated successfully")

    context = {
        "objectlist": queryset,
        'title': 'detail',
        "instance": instance,
        "form":form,
    }
    return render(request, "create.html", context)


def posts_delete(request, id = None):
    instance = get_object_or_404(posts, id=id)
    instance.delete()
    messages.success(request, "Content deleted successfully")
    return redirect("posts:default")


def posts_lists(request):
    queryset_list = posts.objects.all().order_by("-timestamp")
    paginator = Paginator(queryset_list, 5)  # Show 5 contacts per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)


    context = {
        'title':'list',
        "objectlist": queryset,
    }
    return render(request,"index.html",context)




