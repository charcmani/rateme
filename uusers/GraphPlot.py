import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

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

