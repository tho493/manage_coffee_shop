
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
# from django.conf.urls import handler404, handler500
# from home import views

# handler404 = views.error
# handler500 = views.error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name="login.html", next_page='/home'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', include('home.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
