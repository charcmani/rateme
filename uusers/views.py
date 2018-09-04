from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy,reverse
from django.views import generic
from .forms import NewEntry,ChangeDp
from .models import Entry,UserDetail
from datetime import datetime
import matplotlib.pyplot as plt
import os
 

#helper functions
def poltPieChart(labels,sizes,username):
	#colors
	colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99'] 
	fig1, ax1 = plt.subplots()
	patches, texts, autotexts = ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90)
	for text in texts:
	    text.set_color('grey')
	for autotext in autotexts:
	    autotext.set_color('grey')
	# Equal aspect ratio ensures that pie is drawn as a circle
	ax1.axis('equal')  
	plt.tight_layout()
	mainPath=os.getcwd()
	path=os.getcwd()+'/MEDIA'
	os.chdir(path)
	name = username+'.png'
	plt.savefig(name)
	os.chdir(mainPath)
	return name
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
		if True:
			print("HEREDB")
			userbase = UserDetail()
			entry = Entry()
			userPresent = Entry.objects.filter(username=request.user.username)
			if len(userPresent)==0:
				userbase.username = request.user.username
				userbase.save()
			entry.username = UserDetail.objects.get(username=request.user.username)
			entry.movie = int(request.POST['movie'])
			entry.lectures = int(request.POST['lecture'])
			entry.self_study = int(request.POST['self_study'])
			entry.exercise = int (request.POST['exercise'])
			entry.went_out = int(request.POST['went_out'])
			entry.sleep = int(request.POST['sleep'])
			now = datetime.now()
			same_day_entry = Entry.objects.filter(
				time_stamp__day=now.day,
				time_stamp__month=now.month,
				time_stamp__year=now.year,
				username=request.user.username)
			print (len(same_day_entry))
			if (entry.movie+entry.lectures+entry.self_study+entry.exercise+entry.went_out+entry.sleep)<=24 and len(same_day_entry)==0:
				userbase = UserDetail.objects.get(username=request.user.username)
				userbase.totSleep+=entry.sleep
				userbase.totMovie+=entry.movie
				userbase.totExercise+=entry.exercise
				userbase.totStudy+=entry.self_study
				userbase.totLectures+=entry.lectures
				userbase.totWent+=entry.went_out
				userbase.logs +=1
				userbase.score = userbase.totStudy+userbase.totWent+userbase.totLectures+userbase.totExercise+userbase.totMovie+userbase.totSleep
				labels=['Movies','Lectures','Self_Study','Exercise','WentOut','Sleep']

				sizes = [userbase.totMovie,userbase.totLectures,userbase.totStudy,userbase.totExercise,
				userbase.totWent,userbase.totSleep]
				print(sizes)
				userbase.pie = poltPieChart(labels,sizes,request.user.username)
				userbase.save()
				entry.save()
				return HttpResponseRedirect(reverse('index'))
			elif len(same_day_entry)!=0:
				return HttpResponse("Only One jornoul per day , Shant reh bhadve")
			else:
				return HttpResponse("YOU MESSED UP")
	else:
		curNewEntry = NewEntry()
	return render(request,'new_entry.html')

def leaderBoard(request):
	userLogPair = (0,0)
	board=UserDetail.objects.values_list('username', 'rating')
	rankings=[]
	for x in board:
		rankings.append((x[1],x[0]))
	rankings=sorted(rankings,reverse=True)
	return render(request,'leaderboard.html',{'userdata':rankings})



def  report(request):
	if request.user.is_authenticated:
		username = request.user.username
		path = UserDetail.objects.get(username=request.user.username)
		print(path.pie)
		return render(request,'report.html',{'path':path})
	else:
		return HttpResponseRedirect(reverse('login'))


def profile(request,user):
	print(user)
	data=user
	print(data)
	try:
		userbase = UserDetail.objects.get(username=user)
	except UserDetail.DoesNotExist:
		return HttpResponse("User Does Not Exist")
	#dum = UserDetail.objects.get(username=username)
	#print (len(userbase))
	
	return render(request,'profile.html',{'data':userbase})
	
def compare(request,user1,user2):
	try:
		player1 = UserDetail.objects.get(username=user1)
		player2 = UserDetail.objects.get(username=user2)
	except UserDetail.DoesNotExist:
		return HttpResponse("Compare between Valid Users")
	winner=[]   #0 for tie 1 for player1 and 2 for player2
	#attributes=['totMovie','totWent','totLectures','totExercise','totWent','totSleep','logs']
	if player1.totMovie>player2.totMovie:
		winner.append(user1)
	elif player2.totMovie>player1.totMovie:
		winner.append(user2)
	else:
		winner.append('tie')
	if player1.totWent>player2.totWent:
		winner.append(user1)
	elif player2.totWent>player1.totWent:
		winner.append(user2)
	else:
		winner.append('tie')
	if player1.totLectures>player2.totLectures:
		winner.append(user1)
	elif player2.totLectures>player1.totLectures:
		winner.append(user2)
	else:
		winner.append('tie')
	if player1.totStudy>player2.totStudy:
		winner.append(user1)
	elif player2.totStudy>player1.totStudy:
		winner.append(user2)
	else:
		winner.append('tie')
	if player1.totSleep>player2.totSleep:
		winner.append(user1)
	elif player2.totSleep>player1.totSleep:
		winner.append(user2)
	else:
		winner.append('tie')
	if player1.totExercise>player2.totExercise:
		winner.append(user1)
	elif player2.totExercise>player1.totExercise:
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
		curUser = UserDetail.objects.get(username=x[0])
		newRating=max(0,(totRating-x[2])+400*(wins-loss)/games)
		print(newRating)
		curUser.rating=newRating
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
	
