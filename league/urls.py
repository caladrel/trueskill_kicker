from django.conf.urls import patterns, include, url
from django.contrib import admin

from league import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'kicker_league.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(patterns(
        '',
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^players$', views.PlayerView.as_view(), name='players'),
        url(r'^players/(?P<pk>\d+)$', views.PlayerDetailView.as_view(),
            name='player_detail'),
        url(r'^matches$', views.MatchView.as_view(), name='matches'),
        url(r'^matches/enter$', views.MatchCreate.as_view(),
            name='matches_enter'),
    ), namespace='league')),
)