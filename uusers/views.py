from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy,reverse
from django.views import generic

from .forms import NewEntry,ChangeDp
from .models import Entry,UserDetail,RatingHistory
from .GraphPlot import polt_pie_chart

from datetime import datetime



# Create your views here.

class SignUp(generic.CreateView):

	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'


def index (request):

	username = None
	if request.user.is_authenticated:
		username = request.user.username
	return render(request,'land.html')

#To insert new entry to the database for logged in user

def entry_new(request):

	if request.user.is_authenticated == False:
		return HttpResponseRedirect(reverse('login'))

	if request.method == 'POST':

		if True:     #Correct Form validation goes here

			try:
				UserDetail.objects.get(username = request.user.username)
			except UserDetail.DoesNotExist:
				user_base = UserDetail(username = request.user.username)
				user_base.save()

			ATTRIBUTES = [
			'movie','lecture','self_study',
			'exercise','went_out','sleep'
			]
			total_hrs = 0

			for i in ATTRIBUTES:
				total_hrs += int(request.POST[i])

			now = datetime.now()
			same_day_entry = Entry.objects.filter(
				time_stamp__day = now.day,
				time_stamp__month = now.month,
				time_stamp__year = now.year,
				username = request.user.username
				)

			if len(same_day_entry) == 0 and total_hrs <= 24:
				entry = Entry(
					username = UserDetail.objects.get(
						username = request.user.username
						),
				    movie = int(request.POST['movie']),
				    lectures = int(request.POST['lecture']),
					self_study = int(request.POST['self_study']),
					exercise = int (request.POST['exercise']),
					went_out = int(request.POST['went_out']),
					sleep = int(request.POST['sleep'])
					)

				user_base = UserDetail.objects.get(
					username = request.user.username
					)
				user_base.totSleep += entry.sleep
				user_base.totMovie += entry.movie
				user_base.totExercise += entry.exercise
				user_base.totStudy += entry.self_study
				user_base.totLectures += entry.lectures
				user_base.totWent += entry.went_out
				user_base.logs += 1
				user_base.score += total_hrs

				labels=[
				'Movies','Lectures','Self_Study',
				'Exercise','WentOut','Sleep'
				]

				sizes = [
				user_base.totMovie,user_base.totLectures,
				user_base.totStudy,user_base.totExercise,
				user_base.totWent,user_base.totSleep
				]
				user_base.pie = polt_pie_chart(
					labels,sizes,
					request.user.username
					)

				user_base.save()
				entry.save()

				return HttpResponseRedirect(reverse('index'))

			elif len(same_day_entry) != 0:
				return HttpResponse("Only One entry per day allowed ")

			else:
				return HttpResponse("YOU MESSED UP")
	else:
		cur_new_entry = NewEntry()

	return render(request,'new_entry.html')


#To generate Leaderboard

def leaderboard(request):

	board = UserDetail.objects.values_list('username', 'rating')
	rankings = []

	for x in board:
		rankings.append((x[1],x[0]))
	rankings = sorted(rankings,reverse=True)

	return render(request,'leaderboard.html',{'userdata':rankings})

#To generate report of logged in user

def  report(request):

	if request.user.is_authenticated:
		username = request.user.username
		path = UserDetail.objects.get(username = request.user.username)
		print(path.pie)
		return render(request,'report.html',{'path':path})
	else:
		return HttpResponseRedirect(reverse('login'))

#To create profile of user , the profile is public

def profile(request,user):

	try:
		user_base = UserDetail.objects.get(username=user)
	except UserDetail.DoesNotExist:
		return HttpResponse("User Does Not Exist")
	
	return render(request,'profile.html',{'data':user_base})

#To compare between 2 users

def compare(request):
	if not('user1' in request.GET and 'user2' in request.GET):
		return render(request,'compare_form.html')
	user1 = request.GET['user1']
	user2 = request.GET['user2']	

	winner = []   #0 for tie 1 for player1 and 2 for player2
	NUMBER_OF_EVALUATORS = 6

	player1=UserDetail.objects.values_list(
		'totMovie','totWent',
		'totLectures','totExercise',
		'totWent','totSleep',
		).filter(username = user1)
	player2=UserDetail.objects.values_list(
		'totMovie','totWent',
		'totLectures','totExercise',
		'totWent','totSleep',
		).filter(username = user2)

	if (len(player1) == 0 or len(player2) == 0):
		return HttpResponse("Invalid User") 

	for itr in range(0,NUMBER_OF_EVALUATORS):

		if player1[0][itr] > player2[0][itr]:
			winner.append(user1)
		elif player1[0][itr] < player2[0][itr]:
			winner.append(user2)
		else:
			winner.append('tie')

	return render(request,'compare_users.html',{'winner':winner})

#To generating user ratings

def ratings(request):

	user_list = UserDetail.objects.values_list(
		'username','score','rating'
		)
	print(user_list)
	list_of_users = []
	number_of_wins = {}
	total_rating = 0
	games = len(user_list)

	for x in user_list:
		list_of_users.append((x[0],x[1],x[2]))
		number_of_wins[x[0]] = 0
		total_rating = total_rating + x[2]

	for x in list_of_users:
		wins = 0
		loss = 0
		for y in list_of_users:

			if x[1] > y[1]:
				wins = wins + 1

			elif x[1] < y[1]:
				loss = loss + 1

		current_rating = RatingHistory()

		current_user = UserDetail.objects.get(username=x[0])
		current_rating.username = UserDetail.objects.get(username=x[0])
		new_rating = (max(1000,x[2] + 50*(wins-loss))
			/(games*(current_user.logs))
			)

		current_user.rating = new_rating
		current_rating.rating = new_rating

		current_rating.save()
		current_user.save()

	return HttpResponse("Ratings Recalculated")

#To update profile picture of users

def update_pic(request):

	if request.user.is_authenticated:
		try:
			current_user=UserDetail.objects.get(
				username=request.user.username
				)
		except UserDetail.DoesNotExist:
			return HttpResponse("NOT A VALID USER")

		if request.method=='POST':
			current_user.dp = request.FILES['profile']
			current_user.save()
			return HttpResponseRedirect(reverse('index'))

		return render(request,'changedp.html')
	else:

		return HttpResponseRedirect(reverse('login'))

	
