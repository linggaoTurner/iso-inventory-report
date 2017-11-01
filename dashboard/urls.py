from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.cross_account_report, name='cross_account_report')
    url(r'^$', views.update_info, name='update_info')
]
