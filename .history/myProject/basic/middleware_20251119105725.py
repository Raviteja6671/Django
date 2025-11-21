from django.http import JsonResponse
import re
import json

class BasicMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        print(request,"hello")
        if(request.path=="/student/"):
            print(request.method,"method")
            print(request.path)
        response=self.get_response(request)
        return response

# class signupMiddleware:
#     def __init__(self,get_response):
#         self.get_response = get_response
#     def __call__(self, request):
#         data = json.loads(request.body)
#         username=data.get('username')
#         email=data.get("email")
#         dob=data.get("dob")
#         password=data.get("pswd")


class basicMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define the list of specific URLs to monitor
        self.target_urls = [
            "/add_stu/",
            "/students/",
            "/student/",
            "/health/",
        ]

    def __call__(self, request):
        path = request.path
        print(f"Incoming request → {path}")

        if path in self.target_urls or path.startswith("/student/"):
            print("Middleware is Active for this URL")
            print(f"Method Used → {request.method}")
            print(f"Full Path → {path}")

            # Exp1 Block POST requests for testing
            if path == "/add_stu/" and request.method == "POST":
                print("⚠️ POST request detected on /add_stu/")
            
            # Exp2 Print user-agent header
            user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")
            print(f"User-Agent: {user_agent}")

        response = self.get_response(request)

        #Exp3 Post-response actions
        if path.startswith("/students/"):
            print("Response successfully returned for student_related URL")

        return response


# 17/11/2025 class task

class SscMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path in ["/job1/", "/job2/"]:
            ssc_result = request.GET.get("ssc", "False")
            if ssc_result != "True":
                return JsonResponse({"error": "you should qualify atleast SSC for applying this job"},status=400)
        return self.get_response(request)


class MedicalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path == "/job1/":
            medical_fit_result = request.GET.get("medically_fit", "False")
            if medical_fit_result != "True":
                return JsonResponse(
                    {"error": "your not Medically fit to apply for this job role"},
                    status=400)
        return self.get_response(request)


class AgeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path in ["/job1/", "/job2/"]:
            age = int(request.GET.get("age", 17))
            if age < 18 or age > 25:
                return JsonResponse(
                    {"error": "age must be in between 18 too 25"},
                    status=400)
        return self.get_response(request)


class UsernameMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/signup/":
            try:
                data = json.loads(request.body)
            except:
                return JsonResponse({"error": "Invalid JSON"}, status=400)

            username = data.get("username", "")
            
            if not username:
                return JsonResponse({"error": "Username is Required"}, status=400)
            if len(username) < 3 or len(username) > 20:
                return JsonResponse({"error": "Username must be 3 to 20 characters"}, status=400)
            if username[0] in "._" or username[-1] in "._":
                return JsonResponse({"error": "Username cannot start or end with . or _"}, status=400)
            if not re.match(r"^[a-zA-Z0-9._]+$", username):
                return JsonResponse({"error": "Username can contain letters, numbers, . and _ only"}, status=400)
            if ".." in username or "__" in username:
                return JsonResponse({"error": "Username cannot have double dots or double underscores"}, status=400)

        return self.get_response(request)



class EmailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/signup/":
            try:
                data = json.loads(request.body)
            except:
                return JsonResponse({"error": "Invalid JSON"}, status=400)

            email = data.get("email", "")

            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            if not re.match(email_regex, email):
                return JsonResponse({"error": "Invalid Email format"}, status=400)

        return self.get_response(request)
    


# class PasswordMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.path == "/signup/":
#             try:
#                 data = json.loads(request.body)
#             except:
#                 return JsonResponse({"error": "Invalid JSON"}, status=400)

#             password = data.get("password", "")

#             password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&._])[A-Za-z\d@$!%*#?&._]{8,}$"

#             if not password:
#                 return JsonResponse({"error": "Password is required"}, status=400)

#             if not re.match(password_regex, password):
#                 return JsonResponse({
#                     "error": "Password must contain 8+ characters, uppercase, lowercase, digit, special char"
#                 }, status=400)

#         return self.get_response(request)



