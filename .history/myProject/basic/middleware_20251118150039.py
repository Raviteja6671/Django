from django.http import JsonResponse
import re

class basicMiddleware:
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
        self.get_response=get_response
    def __call__(self, request):
        if(request.path == "/signup/"):
            username=request.get("username","")
            #checks user name empty or not
            if not username:
                return JsonResponse({"error":"Username is Required"},status=400)
            if len(username)<3 or len(username)>20:
                return JsonResponse({"Error":"username should conatim only 3 to 20 characters"},status=400)
            if username[0] in "._" or username[-1] in "._":
                return JsonResponse({"error":"Username should not starts or ends with . or _"},status=400)
            if not re.match(r"^[a-z A-Z 0-9]+$",username):
                return JsonResponse({"Error":"username shouls contain the letters,Numbers,dot,underscore"},status=400)
            if ".." in username or "__" in username:
                return JsonResponse({"Error":"Username should be cannot have .. or "},status=400)
        return self.get_response(request)