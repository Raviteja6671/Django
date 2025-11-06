from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

def sample(request):
    return HttpResponse('hello world')

def sample1(request):
    return HttpResponse('WelCome to Django')

def sampleInfo(request):
    data={"name":"raviteja","age":"22","city":"hyd"}
    # data=[4,6,8]
    return JsonResponse(data)

def dynamicResponse(request):
    name=request.GET.get("name"," Raviteja")
    city=request.GET.get("city","Hyderabad")
    return HttpResponse(f"Hello {name} From {city} !")

def add(request):
    a = int(request.GET.get('a', 8))
    b = int(request.GET.get('b', 9))
    return HttpResponse(f"Addition: {a + b}")

def sub(request):
    a = int(request.GET.get('a', 12))
    b = int(request.GET.get('b', 5))
    return HttpResponse(f"Subtraction: {a - b}")

def mul(request):
    a = int(request.GET.get('a', 18))
    b = int(request.GET.get('b', 4))
    return HttpResponse(f"Multiplication: {a * b}")

def div(request):
    a = int(request.GET.get('a', 8))
    b = int(request.GET.get('b', 6))  # Avoid division by zero default
    try:
        result = a / b
    except ZeroDivisionError:
        return HttpResponse("Error: Division by zero")
    return HttpResponse(f"Division: {result}")
