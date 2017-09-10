from django.contrib import admin
from .models import posts
# Register your models here.



class postsAdmin(admin.ModelAdmin):
    class meta:
        model = posts

    # actions

    def make_published(self, request, posts):
        posts.update(status='p')

        if rows_updated == 1:
            message_bit = "1 story was"

        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    def make_draft(self, request, posts):
        posts.update(status='d')

        if rows_updated == 1:
            message_bit = "1 story was"

        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as draft." % message_bit)


    def make_withdrawn(self, request, posts):
        posts.update(status='w')

        if rows_updated == 1:
            message_bit = "1 story was"

        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as withdrawn." % message_bit)

    actions = [make_published, make_draft, make_withdrawn]
    # list based options



    list_display = ["title", "timestamp", "updated","status"]
    list_display_links = ['title','updated']
    list_filter = ['updated', 'timestamp']

#search based options

    search_fields = ('title', 'content')

#ordering
    ordering = ['title', 'updated']




admin.site.register(posts, postsAdmin)


