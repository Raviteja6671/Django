from django.shortcuts import render
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from basic.models import student
from basic.models import Users
from django.conf import settings
import jwt
from django.contrib.auth.hashers import make_password,check_password

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

# Health check endpoint
def health(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        return JsonResponse({"status": "ok", "db": "connected"})
    except Exception as e:
        return JsonResponse({"status": "error", "db": str(e)})



# POST - Create new student
@csrf_exempt
def add_student(request):
    print(request.method)
    if request.method == "POST":
        data = json.loads(request.body)  
        email = data.get("email")
        # Check if email already exists
        if student.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)
        # Create new student
        stu = student.objects.create(
            name=data.get("name"),
            age=data.get("age"),
            email=email
        )
        return JsonResponse({"status": "success", "id": stu.id}, status=201)

# GET - Retrieve all students
    elif request.method == "GET":
        result = list(student.objects.values())
        return JsonResponse({"status": "success", "data": result}, status=200)

# DELETE - Delete student by ID
    elif request.method == "DELETE":
        data = json.loads(request.body)
        ref_id = data.get("id")
        try:
            deleting_data = student.objects.filter(id=ref_id).values().first()
            if not deleting_data:
                return JsonResponse({"error": "Student not found"}, status=404)
            student.objects.get(id=ref_id).delete()
            return JsonResponse({
                "status": "deleted",
                "deleted_data": deleting_data
            }, status=200)
        except student.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)

# PUT - Full update (update all fields)
    elif request.method == "PUT":
        data = json.loads(request.body)
        ref_id = data.get("id")
        try:
            stu = student.objects.get(id=ref_id)
        except student.DoesNotExist:
            return JsonResponse({'error': "Student not found"}, status=404)
        # Check if new email already exists
        new_email = data.get("email")
        if student.objects.filter(email=new_email).exclude(id=ref_id).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)
        stu.name = data.get("name", stu.name)
        stu.age = data.get("age", stu.age)
        stu.email = data.get("email", stu.email)
        stu.save()
        updated_data = student.objects.filter(id=ref_id).values().first()
        return JsonResponse({"status": "full update success", "updated_data": updated_data}, status=200)

# PATCH - Partial update (only update specific fields)
    elif request.method == "PATCH":
        data = json.loads(request.body)
        ref_id = data.get("id")
        try:
            stu = student.objects.get(id=ref_id)
        except student.DoesNotExist:
            return JsonResponse({'error': "Student not found"}, status=404)
        # Update only fields provided in the request
        if "name" in data:
            stu.name = data["name"]
        if "age" in data:
            stu.age = data["age"]
        if "email" in data:
            new_email = data["email"]
            # Check if email already exists
            if student.objects.filter(email=new_email).exclude(id=ref_id).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)
            stu.email = new_email
        stu.save()
        updated_data = student.objects.filter(id=ref_id).values().first()
        return JsonResponse({"status": "partial update success", "updated_data": updated_data}, status=200)

    return JsonResponse({'error': "Unsupported method"}, status=405)



# 11/11/2025 task operations

def get_all_students(request):
    students = student.objects.all()
    data = list(students.values())
    return JsonResponse(data, safe=False)

def get_student_by_id(request, id):
    try:
        s = student.objects.get(id=id)
        data = {'id': s.id, 'name': s.name, 'age': s.age, 'email': s.email}
        return JsonResponse(data)
    except student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

def filter_students_age_gte_20(request):
    students = student.objects.filter(age__gte=20)
    data = list(students.values())
    return JsonResponse(data, safe=False)

def filter_students_age_lte_25(request):
    students = student.objects.filter(age__lte=25)
    data = list(students.values())
    return JsonResponse(data, safe=False)

def get_unique_ages(request):
    ages = student.objects.values_list('age', flat=True).distinct()
    return JsonResponse(list(ages), safe=False)

def count_total_students(request):
    total = student.objects.count()
    return JsonResponse({'total_students': total})


def job1(request):
    return JsonResponse({"message":"You have successfully applied for job1"},status=200)

def job2(request):
    return JsonResponse({"Message":"you have successfully applied for job2"},status=200)



# 18/11/2025 class

@csrf_exempt               #POST OPERATION
def signUp(request):
    if request.method == "POST":
        data = request.json_data   # <-- use this

        username = data.get("username")
        email = data.get("email")
        password =make_password(data.get("password"))

        if not username or not email or not password:
            return JsonResponse({"Message": "All fields are required"}, status=400)

        user = Users.objects.create(
            username=username,
            email=email,
            password=password
        )

        return JsonResponse({"Message": "User Registered", "id": user.id}, status=200)

    return JsonResponse({"Message": "Invalid Request Method"}, status=405)


@csrf_exempt                              # GET OPERATION
def getUsers(request):
    if request.method == "GET":
        users = Users.objects.all()

        data = []
        for user in users:
            data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "password": user.password   # If you want to hide password, tell me
            })

        return JsonResponse({"users": data}, status=200)

    return JsonResponse({"Message": "Invalid Request Method"}, status=405)



@csrf_exempt                            # DELETE OPERATION
def deleteUser(request, id):
    if request.method == "DELETE":
        try:
            user = Users.objects.get(id=id)
            user.delete()
            return JsonResponse({"Message": "User Deleted Successfully", "id": id}, status=200)
        except Users.DoesNotExist:
            return JsonResponse({"Message": "User Not Found"}, status=404)

    return JsonResponse({"Message": "Invalid Request Method"}, status=405)


# @csrf_exempt
# def login(request):
#     if request.method=="POST":
#         data=request.POST
#         print(data)
#         username=data.get('username')
#         password=data.get("password")
#         try:
#             user=Users.objects.get(username=username)
#             if check_password(password,user.password):
#                 token="a json web token"

#                 return JsonResponse({"status":"successfully Loggedin","token":token},status=200)
#             else:
#                 return JsonResponse({"status":"failure","message":"invalid password"},status=400)
#         except Users.DoesNotExist:
#             return JsonResponse({"status":"failure","message":"user not found"},status=400)
@csrf_exempt
def login(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        try:
            user = Users.objects.get(username=username)
            if password == user.password:  # plain-text compare
                #token = "a json web token"
                paylaod={"user":username,"email":user.email,"id":user.id}
                token=jwt.encode({"username":username},settings.SECRET_KEY,algorithm="HS256")
                return JsonResponse({"status": "successfully Loggedin", "token": token}, status=200)
            else:
                return JsonResponse({"status": "failure", "message": "invalid password"}, status=400)
        except Users.DoesNotExist:
            return JsonResponse({"status": "failure", "message": "user not found"}, status=400)


@csrf_exempt
def check(request):
    hashed="pbkdf2_sha256$1000000$oWRnje0wvfd1GDEWVxl1cH$ISOcbGnboV91VHZ9hLKmh+kOIwxLHACntmEfaRKMd+4="
    ipdata=request.POST
    print(ipdata)
    #hashed=make_password(ipdata.get('ip'))
    x=check_password(ipdata.get("ip"),hashed)
    print(x)
    return JsonResponse({"status":"success","data":x},status=200)


