from django.shortcuts import render
from . import callGoogleAPI
# Create your views here.
def index(request):
	if request.body:
		websites = request.POST.getlist('websites')
		callGoogleAPI.CallClist(websites)
		return render(request, "Add_new_contest/index.html")

	#return render(request, "Add_new_contest/index1.html")	

	context = {
		"WEBSITES": [
			"atcoder.jp",
			"leetcode.com",
			"codingcompetitions.withgoogle.com",
			"codeforces.com",
			"topcoder.com"	
		],
	}
	#print(request.body)
	return render(request, "Add_new_contest/index.html", context)