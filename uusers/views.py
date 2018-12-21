from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy,reverse
from django.views import generic

from .forms import NewEntry,ChangeDp
from .models import Entry,UserDetail,RatingHistory
from .GraphPlot import poltPieChart

from datetime import datetime


#helper functions

# Create your views here.

def index (request):
	username = None
	if request.user.is_authenticated:
		username = request.user.username
	return render(request,'land.html')

class SignUp(generic.CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'


def entryNew(request):
	if request.user.is_authenticated==False:
		return HttpResponseRedirect(reverse('login'))
	if request.method == 'POST':
		curNewEntry = NewEntry(request.POST)
		print("HerePOST")
		if True:     #Correct Form validation goes here
			print("HEREDB")
			try:
				UserDetail.objects.get(username=request.user.username)
			except UserDetail.DoesNotExist:
				userbase = UserDetail(username=request.user.username)
				userbase.save()
			attributes=['movie','lecture','self_study','exercise','went_out','sleep']
			total_hrs=0
			for i in attributes:
				total_hrs+=int(request.POST[i])
			now = datetime.now()
			same_day_entry = Entry.objects.filter(
				time_stamp__day=now.day,
				time_stamp__month=now.month,
				time_stamp__year=now.year,
				username=request.user.username)
			print (len(same_day_entry))
			if len(same_day_entry)==0 and total_hrs<=24:
				entry = Entry(username=UserDetail.objects.get(username=request.user.username),
				movie=int(request.POST['movie']),lectures=int(request.POST['lecture']),
					self_study=int(request.POST['self_study']),exercise=int (request.POST['exercise']),
					went_out=int(request.POST['went_out']),sleep=int(request.POST['sleep']))
				userbase = UserDetail.objects.get(username=request.user.username)
				userbase.totSleep+=entry.sleep
				userbase.totMovie+=entry.movie
				userbase.totExercise+=entry.exercise
				userbase.totStudy+=entry.self_study
				userbase.totLectures+=entry.lectures
				userbase.totWent+=entry.went_out
				userbase.logs +=1
				userbase.score += total_hrs
				labels=['Movies','Lectures','Self_Study','Exercise','WentOut','Sleep']

				sizes = [userbase.totMovie,userbase.totLectures,userbase.totStudy,userbase.totExercise,
				userbase.totWent,userbase.totSleep]
				print(sizes)
				userbase.pie = poltPieChart(labels,sizes,request.user.username)
				userbase.save()
				entry.save()
				return HttpResponseRedirect(reverse('index'))
			elif len(same_day_entry)!=0:
				return HttpResponse("Only One entry per day allowed ")
			else:
				return HttpResponse("YOU MESSED UP")
	else:
		curNewEntry = NewEntry()
	return render(request,'new_entry.html')


#To generate Leaderboard
def leaderBoard(request):
	board=UserDetail.objects.values_list('username', 'rating')
	rankings=[]
	for x in board:
		rankings.append((x[1],x[0]))
	rankings=sorted(rankings,reverse=True)
	return render(request,'leaderboard.html',{'userdata':rankings})

#To generate report of logged in user
def  report(request):
	if request.user.is_authenticated:
		username = request.user.username
		path = UserDetail.objects.get(username=request.user.username)
		print(path.pie)
		return render(request,'report.html',{'path':path})
	else:
		return HttpResponseRedirect(reverse('login'))

#To create profile of user , the profile is public
def profile(request,user):
	try:
		userbase = UserDetail.objects.get(username=user)
	except UserDetail.DoesNotExist:
		return HttpResponse("User Does Not Exist")
	
	return render(request,'profile.html',{'data':userbase})

#To compare between 2 users
import itertools
def compare(request,user1,user2):
	winner=[]   #0 for tie 1 for player1 and 2 for player2
	attributes=['totMovie','totWent','totLectures',
	'totExercise','totWent','totSleep']
	length = len(attributes)
	player1=UserDetail.objects.values_list('totMovie','totWent',
		'totLectures','totExercise','totWent','totSleep',
		).filter(username=user1)

	player2=UserDetail.objects.values_list('totMovie','totWent',
		'totLectures','totExercise','totWent','totSleep',
		).filter(username=user2)
	if (len(player1)==0 or len(player2)==0):
		return HttpResponse("Invalid User") 
	for itr in range(0,length):
		print(player2)
		if player1[0][itr]>player2[0][itr]:
			winner.append(user1)
		elif player1[0][itr]<player2[0][itr]:
			winner.append(user2)
		else:
			winner.append('tie')
	return render(request,'compare_users.html',{'winner':winner})


def ratings(request):
	userList = UserDetail.objects.values_list('username','score','rating')
	print(userList)
	ListOfUsers=[]
	numberOfWins ={}
	totRating=0
	games = len(userList)
	for x in userList:
		ListOfUsers.append((x[0],x[1],x[2]))
		numberOfWins[x[0]]=0
		totRating+=x[2]
	for x in ListOfUsers:
		wins=0
		loss=0
		for y in ListOfUsers:
			if x[1]>y[1]:
				wins+=1
			elif x[1]<y[1]:
				loss+=1
		curRating=RatingHistory()
		curUser = UserDetail.objects.get(username=x[0])
		curRating.username = UserDetail.objects.get(username=x[0])
		newRating=max(1000,x[2]+50*(wins-loss)/(games*(curUser.logs)))
		print(newRating)
		curUser.rating=newRating
		curRating.rating=newRating
		curRating.save()
		curUser.save()
	return HttpResponse("okok")

def updatePic(request):
	if request.user.is_authenticated:
		try:
			curUser=UserDetail.objects.get(username=request.user.username)
		except UserDetail.DoesNotExist:
			return HttpResponse("NOT A VALID USER")
		if request.method=='POST':
			dp = ChangeDp(request.POST,request.FILES)
			if dp.is_valid():
				print("HA")
			curUser.dp = request.FILES['profile']
			curUser.save()
			return HttpResponseRedirect(reverse('index'))
		else:
			dp=ChangeDp()
		return render(request,'changedp.html')
	else:
		return HttpResponseRedirect(reverse('login'))

def compareForm(request):
	if request.method=='POST':
		user1 = request.POST['user1']
		user2 = request.POST['user2']
		return HttpResponseRedirect(user1+'/'+user2)
	else:
		return render(request,'compare_form.html')
	
