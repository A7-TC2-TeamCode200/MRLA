from django.contrib import admin
from posts.models import Service, ServiceComment, Community, CommunityComment


admin.site.register(Service)
admin.site.register(ServiceComment)
admin.site.register(Community)
admin.site.register(CommunityComment)
