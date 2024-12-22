def calculate_bmr(user):
    """
    Calculate the Basal Metabolic Rate (BMR) for the user based on their activity level.
    The formula is based on the Harris-Benedict equation.
    """
    # Assuming 'user' has 'gender', 'weight', 'height', 'age', and 'activity_level' attributes
    if user.gender == 'male':
        bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age + 5
    else:
        bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age - 161

    # Set activity level multipliers
    activity_multipliers = {
        'Sedentary': 1.2,          # Little or no exercise
        'Lightly Active': 1.375,   # Light exercise or sports 1-3 days per week
        'Moderately Active': 1.55, # Moderate exercise or sports 3-5 days per week
        'Very Active': 1.725       # Hard exercise or sports 6-7 days per week
    }

    # Get the activity level multiplier based on the user's activity level
    activity_multiplier = activity_multipliers.get(user.activity_level, 1.2)  # Default to Sedentary if not found

    # Calculate the daily calorie needs
    daily_calories = bmr * activity_multiplier

    return daily_calories
