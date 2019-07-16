### Urls contains all the url that is generated in the website and its entire path
## r signals a Regex with ^ being the start and $ being the end of the regex
# all the functionalities of urls are handelled in views.py



from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'search/$', views.search, name='search'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^vitae/(?P<update>[0-1])/$', views.vitae, name='vitae'),
    url(r'^stats/$', views.stats, name='stats'),
    url(r'details/(?P<id>[0-9]+)$', views.details, name='details'),
    url(r'^add/$', views.add, name='add'),
    url(r'^jhos/$', views.populateResumetoDb, name='populateResumetoDb'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
   ]