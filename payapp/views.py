from django.shortcuts import render, HttpResponse


# Create your views here.
def home(request):
	return render(request, "./home.html")


def register(request):
	if request.method == 'POST':
		pass
	else:
		return render(request, "./register.html")


def login(request):
	if request.method == 'POST':
		pass
	else:
		return render(request, "./login.html")
