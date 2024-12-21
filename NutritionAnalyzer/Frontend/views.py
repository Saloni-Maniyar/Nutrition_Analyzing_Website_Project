from django.shortcuts import redirect, render 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout 
from django.http import JsonResponse
from .models import NutritionAnalysis
import json 
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def home(request):
    return render(request, 'index.html')


@login_required
def profile(request):
    print(f"Session Data: {request.session.items()}")  # Debugging session datas
    print(f"Logged-in user: {request.user}")  # Check what is returned for request.user
    user = request.user  # Get the current logged-in user
    print(f"User data before update: {user.name}, {user.email}, {user.age}, {user.weight}, {user.gender}, {user.activity_level}")
    
    if request.method == 'POST':
        # Get the updated data from the form
        updated_name = request.POST['name']
        updated_email = request.POST['email']
        updated_age = request.POST['age']
        updated_weight = request.POST['weight']
        updated_gender = request.POST['gender']
        updated_activity_level = request.POST['activity_level']

        # Debugging prints to check the values received from the form
        print(f"Received form data: Name: {updated_name}, Email: {updated_email}, Age: {updated_age}, Weight: {updated_weight}, Gender: {updated_gender}, Activity Level: {updated_activity_level}")

        # Update the user object with the new values
        user.name = updated_name
        user.age = updated_age
        user.weight = updated_weight
        user.gender = updated_gender
        user.activity_level = updated_activity_level

        # Save the updated user data to the database
        user.save()

        # Debugging print to confirm the update
        print(f"User data after update: {user.name}, {user.email}, {user.age}, {user.weight}, {user.gender}, {user.activity_level}")
        
        # Display a success message and redirect to the profile page
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')  # Redirect to the same page to see updated data

    return render(request, 'Profile.html', {'user': user})

def analyze(request):
    # You can pass context here if needed, for now, it will just render the page
    return render(request, 'Analyze.html')

def track(request):
    # You can pass context here if needed, for now, it will just render the page
    return render(request, 'Track.html') 





def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        age = request.POST['age']
        weight = request.POST['weight']
        gender = request.POST['gender']
        activity_level = request.POST['activity_level']

         # Debug message: Check received POST data
        print(f"Received data - Name: {name}, Email: {email}, Age: {age}, Weight: {weight}, Gender: {gender}, Activity Level: {activity_level}")
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            print(f"Passwords do not match for user: {email}")
            return redirect('register')
          

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            print(f"Email already registered: {email}")
            return redirect('register')
           

        # Hash the password and create the user
        hashed_password = make_password(password)
        User.objects.create(
            name=name,
            email=email,
            password=hashed_password,
            age=age,
            weight=weight,
            gender=gender,
            activity_level=activity_level
        )
        messages.success(request, 'Registration successful! Please log in.')
        print(f"User {email} registered successfully")
        return redirect('login')  # Redirect to login page after successful registration

    return render(request, 'Register.html')  # Render registration form


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        print(f"Attempting login for email: {email}")
        
        # Authenticate user using the custom user model
        try:
            # Retrieve the user from the custom User model
            user = User.objects.get(email=email) 
            print(f"user={user}")
            
            # Check if the provided password matches the hashed password
            if check_password(password, user.password):
                login(request, user)  # Log the user in
                messages.success(request, 'Login successful!')
                print("Authentication successful")
                # return redirect('home')  # Redirect to home page after successful login
                return render(request, 'index.html', {'user': user})
            else:
                messages.error(request, 'Invalid credentials')
                print("Authentication failed - wrong password")
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials')
            print("Authentication failed - user does not exist")
        
        return redirect('login')  # Return to the login page if authentication fails
    
    return render(request, 'login.html')  # Render the login form

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    print(f"User logged out") 
    return redirect('home')  # Redirect to login page after logout 

#Analyzed Data
# @csrf_exempt
# @login_required 
# def save_nutrition_data(request):
#     if request.method == 'POST':
#         # Parse the JSON data sent from the frontend
#         try:
#             data = json.loads(request.body)
            
#             # Extract nutrition details
#             food_name = data.get('food_name')
#             calories = data.get('calories')
#             protein = data.get('protein')
#             carbs = data.get('carbs')
#             fat = data.get('fat')
#             fiber = data.get('fiber')
#             sugars = data.get('sugars')
#             sodium = data.get('sodium')
#             cholesterol = data.get('cholesterol')

#             # Create and save the NutritionData instance
#             NutritionAnalysis.objects.create(
#                 user=request.user,
#                 food_name=food_name,
#                 calories=calories,
#                 protein=protein,
#                 carbs=carbs,
#                 fat=fat,
#                 fiber=fiber,
#                 sugars=sugars,
#                 sodium=sodium,
#                 cholesterol=cholesterol
#             )

#             return JsonResponse({'success': True, 'message': 'Nutrition data saved successfully.'})

#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)})

#     return JsonResponse({'success': False, 'message': 'Invalid request method.'})



@csrf_exempt
@login_required
def save_nutrition_data(request):
    print("user in save nutrition=",request.user)
    if request.method == 'POST':
        # Check if the content type is JSON
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)  # Parse the JSON body
                
                # Extract nutrition details from the parsed data
                food_name = data.get('food_name')
                calories = data.get('calories')
                protein = data.get('protein')
                carbs = data.get('carbs')
                fat = data.get('fat')
                fiber = data.get('fiber')
                sugars = data.get('sugars')
                sodium = data.get('sodium')
                cholesterol = data.get('cholesterol')

                # Save the nutrition data to the database
                nutrition_data= NutritionAnalysis.objects.create(
                    user=request.user,
                    food_name=food_name,
                    calories=calories,
                    protein=protein,
                    carbs=carbs,
                    fat=fat,
                    fiber=fiber,
                    sugars=sugars,
                    sodium=sodium,
                    cholesterol=cholesterol
                )
                print(f"Nutrition data saved successfully: {nutrition_data.food_name} - {nutrition_data.calories} calories")

                return JsonResponse({'success': True, 'message': 'Nutrition data saved successfully.'})

            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})

        else:
            return JsonResponse({'success': False, 'message': 'Invalid content type. Expected JSON.'})
        
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
