try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except:
    pass

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .forms import PostForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils import timezone

from .models import posts


# Create your views here.
queryset = posts.objects.all()


def posts_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

   # if not request.user.is_authenticated:
    #    raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user=request.user
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
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    share_string = quote_plus(instance.content)
    context = {
        "objectlist":queryset,
        'title':'detail',
        "instance": instance,
        "share_string":share_string
    }
    return render(request, "detail.html", context)


def posts_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(posts, id=id)
    instance.delete()
    messages.success(request, "Content deleted successfully")
    return redirect("posts:default")


def posts_lists(request):
    queryset_list = posts.objects.active()#.order_by("-timestamp")
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
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
        "page_request_var": page_request_var,
    }
    return render(request,"index.html",context)




