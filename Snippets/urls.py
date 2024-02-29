from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views



urlpatterns = [
    path('', views.index_page),
    path('snippets/add', views.add_snippet_page),
    path('snippets/list', views.snippets_page),
    path('admin/', admin.site.urls),
    path('snippets/<int:id>/', views.snippet_detail, name='snippet_detail'),  
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
