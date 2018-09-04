from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings
urlpatterns=[
	path('',views.index,name='index'),
	path('signup/',views.SignUp.as_view(),name='signup'),
	path('entry/',views.entryNew,name='entry'),
	path('leaderboard',views.leaderBoard,name='leaderboard'),
	path('report',views.report,name='report'),
	path('profile/<user>/',views.profile,name='profile'),
	path('compare/',views.compareForm,name='compareform'),
	path('compare/<user1>/<user2>/',views.compare,name='compare'),
	path('ratings/',views.ratings,name='rating'),
	path('updatepic',views.updatePic,name='updatepic'),
	
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)