from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index_page),
    path('snippets/add', views.add_snippet_page, name='add_snippet_page'),
    path('snippets/list', views.snippets_page, name='view_snippets'),
    path('snippets/<int:id>/', views.snippet_detail, name='snippet_detail'),  
    path('snippets/<int:id>/delete', views.snippet_delete, name='snippet_delete'),
    path('admin/', admin.site.urls),
    path('snippets/<int:id>/edit', views.snippet_edit, name='snippet_edit'),
    path('my_snippets/', views.my_snippets, name='my_snippets'),
    path('signup/', views.signup, name='signup'),
    path('snippets/<int:snippet_id>/comment/add', views.comment_add, name='comment_add'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('accounts/signup/', views.signup, name='signup'),  
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
