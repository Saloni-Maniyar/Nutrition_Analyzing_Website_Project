from django.shortcuts import redirect, render 
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Frontend.utils import calculate_bmr
from .models import User, NutritionAnalysis
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout 
from django.http import JsonResponse
import json 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.utils import timezone

# Create your views here.
@never_cache
def home(request):
    return render(request, 'index.html')

# Define the About Us view
def about(request):
    return render(request, 'about.html') 

def contact(request):
    return render(request, 'contact.html')

@login_required
def profile(request):
    print(f"Session Data: {request.session.items()}")  # Debugging session data
    print(f"Logged-in user: {request.user}")  # Check what is returned for request.user
    user = request.user  # Get the current logged-in user
    print(f"User data before update: {user.name}, {user.email}, {user.age}, {user.weight}, {user.height}, {user.gender}, {user.activity_level}")
    
    if request.method == 'POST':
        # Get the updated data from the form
        updated_name = request.POST['name']
        updated_email = request.POST['email']
        updated_age = request.POST['age']
        updated_weight = request.POST['weight']
        updated_height = request.POST['height']  # Added height
        updated_gender = request.POST['gender']
        updated_activity_level = request.POST['activity_level']

        # Debugging prints to check the values received from the form
        print(f"Received form data: Name: {updated_name}, Email: {updated_email}, Age: {updated_age}, Weight: {updated_weight}, Height: {updated_height}, Gender: {updated_gender}, Activity Level: {updated_activity_level}")

        # Update the user object with the new values
        user.name = updated_name
        user.age = updated_age
        user.weight = updated_weight
        user.height = updated_height  # Update height
        user.gender = updated_gender
        user.activity_level = updated_activity_level

        # Save the updated user data to the database
        user.save()

        # Debugging print to confirm the update
        print(f"User data after update: {user.name}, {user.email}, {user.age}, {user.weight}, {user.height}, {user.gender}, {user.activity_level}")
        
        # Display a success message and redirect to the profile page
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')  # Redirect to the same page to see updated data

    return render(request, 'Profile.html', {'user': user})


def analyze(request):
    return render(request, 'Analyze.html')


def track(request):
    return render(request, 'Track.html') 


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        age = request.POST['age']
        weight = request.POST['weight']
        height = request.POST['height']  # Added height
        gender = request.POST['gender']
        activity_level = request.POST['activity_level']

        print(f"Received data - Name: {name}, Email: {email}, Age: {age}, Weight: {weight}, Height: {height}, Gender: {gender}, Activity Level: {activity_level}")
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            print(f"Passwords do not match for user: {email}")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            print(f"Email already registered: {email}")
            return redirect('register')

        hashed_password = make_password(password)
        User.objects.create(
            name=name,
            email=email,
            password=hashed_password,
            age=age,
            weight=weight,
            height=height,  # Include height
            gender=gender,
            activity_level=activity_level
        )
        messages.success(request, 'Registration successful! Please log in.')
        print(f"User {email} registered successfully")
        return redirect('login')

    return render(request, 'Register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        print(f"Attempting login for email: {email}")
        
        try:
            user = User.objects.get(email=email) 
            print(f"user={user}")
            
            if check_password(password, user.password):
                login(request, user)
                messages.success(request, 'Login successful!')
                print("Authentication successful")
                return render(request, 'index.html', {'user': user})
            else:
                messages.error(request, 'Invalid credentials')
                print("Authentication failed - wrong password")
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials')
            print("Authentication failed - user does not exist")
        
        return redirect('login')
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    print(f"User logged out") 
    return redirect('home')


@csrf_exempt
@login_required
def save_nutrition_data(request):
    print("user in save nutrition=", request.user)
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                
                food_name = data.get('food_name')
                calories = data.get('calories')
                protein = data.get('protein')
                carbs = data.get('carbs')
                fat = data.get('fat')
                fiber = data.get('fiber')
                sugars = data.get('sugars')
                sodium = data.get('sodium')
                cholesterol = data.get('cholesterol')

                nutrition_data = NutritionAnalysis.objects.create(
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

# @login_required
# def fetch_nutrition_data(request):
#     try:
#         # Fetch today's nutrition data for the logged-in user
#         user_nutrition_data = NutritionAnalysis.get_today_data(request.user)  # Using the class method to get today's data
        
#         # Print the fetched data to check if it's fetched correctly
#         print("Fetched data:", user_nutrition_data)

#         # Process the fetched data into a response format
#         nutrition_data_response = [{
#             'food_name': entry.food_name,
#             'calories': entry.calories,
#             'protein': entry.protein,
#             'carbs': entry.carbs,
#             'fat': entry.fat,
#             'fiber': entry.fiber,
#             'sugars': entry.sugars,
#             'sodium': entry.sodium,
#             'cholesterol': entry.cholesterol
#         } for entry in user_nutrition_data]

#         print("Processed data:", nutrition_data_response)
#         # Return the response
#         return JsonResponse({
#             'success': True,
#             'nutrition_data': nutrition_data_response
#         })

#     except Exception as e:
#         return JsonResponse({'success': False, 'message': str(e)})



@login_required
def fetch_nutrition_data(request):
    try:
        # Fetch today's nutrition data for the logged-in user
        user_nutrition_data = NutritionAnalysis.get_today_data(request.user)  # Using the class method to get today's data
        
        # Calculate the total calories consumed today
        total_calories_consumed = sum(entry.calories for entry in user_nutrition_data)

        # Calculate the daily calorie requirement using the utility function
        daily_calorie_requirement = calculate_bmr(request.user)

        # Calculate the remaining calories needed
        remaining_calories = daily_calorie_requirement - total_calories_consumed

        # Process the fetched data into a response format
        nutrition_data_response = [
            {
                'food_name': entry.food_name,
                'calories': entry.calories,
                'protein': entry.protein,
                'carbs': entry.carbs,
                'fat': entry.fat,
                'fiber': entry.fiber,
                'sugars': entry.sugars,
                'sodium': entry.sodium,
                'cholesterol': entry.cholesterol
            }
            for entry in user_nutrition_data
        ]

        # Return the response
        return JsonResponse({
            'success': True,
            'daily_calorie_requirement': daily_calorie_requirement,
            'total_calories_consumed': total_calories_consumed,
            'remaining_calories': remaining_calories,
            'nutrition_data': nutrition_data_response
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})