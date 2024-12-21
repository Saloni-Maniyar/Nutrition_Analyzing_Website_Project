

const api_key = '2a60e0e9342048258e5f38b358b758fa';
const foodForm = document.getElementById("foodForm");

// Function to render the chart
 async function renderNutritionChart(calories, protein, carbs, fat, fiber, sugars, sodium, cholesterol) {
    console.log("In renderNutritionChart");
    let nutritionResultDiv = document.querySelector("#nutritionResult");
    nutritionResultDiv.parentElement.classList.remove("d-none");

    const ctx = document.getElementById('NutritionChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (window.nutritionChart) {
        window.nutritionChart.destroy();
    }

    // Create the chart
    window.nutritionChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Calories', 'Protein (g)', 'Carbs (g)', 'Fat (g)', 'Fiber (g)', 'Sugar (g)', 'Sodium (mg)', 'Cholesterol (mg)'],
            datasets: [{
                label: 'Nutritional Values Per Serving',
                data: [calories, protein, carbs, fat, fiber, sugars, sodium, cholesterol],
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384', '#36A2EB'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Display the card containing the chart
    document.getElementById('nutritionCard').classList.remove('d-none');
}

 // Function to fetch food ID
async function fetchFoodId(food) {
    console.log("In fetch food ID");
    const baseurl = "https://api.spoonacular.com/recipes/complexSearch";
    let url = `${baseurl}?apiKey=${api_key}&query=${food}&cuisine=Indian`;

    try {
        let response = await axios.get(url);
        console.log("Complex search =", response);
        let results = response.data.results;

        // If no Indian results found, search globally
        if (results.length === 0) {
            console.log("No Indian cuisine results found. Searching globally...");
            url = `${baseurl}?apiKey=${api_key}&query=${food}`;
            response = await axios.get(url);
            console.log("Complex search global =", response);
            results = response.data.results;
        }

        // If no results found in both Indian and global search
        if (results.length === 0) {
            console.log("No results found in our database.");
            return null;
        }

        // Split the food query into words for matching
        const searchWords = food.toLowerCase().split(" ");

        // Find the exact match based on the title
        const matchedFood = results.find(item =>
            searchWords.every(word => item.title.toLowerCase().includes(word))
        );

        // If exact match found, return its ID; otherwise, return the first item's ID
        if (matchedFood) {
            console.log("Matched Food ID:", matchedFood.id);
            return matchedFood.id;
        } else {
            console.log("No exact match found. Returning first result ID:", results[0].id);
            return results[0].id;
        }
    } catch (error) {
        console.error("Error fetching data:", error);
        return null;
    }
}

// Function to fetch nutrition data
async function fetchNutritionData(id,food_Entered) {
    console.log("parameter 2 food user entered:",food_Entered)
    console.log("In fetch nutrition");
    console.log("ID =", id);

    if (!id) {
        console.log("Invalid food ID. Cannot fetch nutrition data.");
        showErrorMessage("No data found for the entered food item.");
        return;
    }

    try {
        const baseurl = "https://api.spoonacular.com/recipes";
        const url = `${baseurl}/${id}/information/?apiKey=${api_key}&includeNutrition=true`;
        let response = await axios.get(url);
        console.log("Recipe API =", response);
        const nutritionData = response.data.nutrition;

        console.log("Nutrition Data:", nutritionData);

        // Calculate the nutritional values for one serving
        const servings = response.data.servings || 1; // Default to 1 serving if not specified
        const caloriesPerServing = nutritionData.nutrients.find(n => n.name === "Calories")?.amount / servings || 0;
        const proteinPerServing = nutritionData.nutrients.find(n => n.name === "Protein")?.amount / servings || 0;
        const carbsPerServing = nutritionData.nutrients.find(n => n.name === "Carbohydrates")?.amount / servings || 0;
        const fatPerServing = nutritionData.nutrients.find(n => n.name === "Fat")?.amount / servings || 0;
        const fiberPerServing = nutritionData.nutrients.find(n => n.name === "Fiber")?.amount / servings || 0;
        const sugarsPerServing = nutritionData.nutrients.find(n => n.name === "Sugar")?.amount / servings || 0;
        const sodiumPerServing = nutritionData.nutrients.find(n => n.name === "Sodium")?.amount / servings || 0;
        const cholesterolPerServing = nutritionData.nutrients.find(n => n.name === "Cholesterol")?.amount / servings || 0;

        // Call the function to render the chart
        await renderNutritionChart(
            caloriesPerServing,
            proteinPerServing,
            carbsPerServing,
            fatPerServing,
            fiberPerServing,
            sugarsPerServing,
            sodiumPerServing,
            cholesterolPerServing
        );
        console.log("Nutrition data rendered successfully!");
        const food_name = response.data.title;  // Get the name of the food item
        console.log("Food Name:", food_name);
        console.log("food user enterd:",food_Entered)
        await saveNutritionDataToDatabase(food_Entered, {
            calories: caloriesPerServing,
            protein: proteinPerServing,
            carbs: carbsPerServing,
            fat: fatPerServing,
            fiber: fiberPerServing,
            sugars: sugarsPerServing,
            sodium: sodiumPerServing,
            cholesterol: cholesterolPerServing
        }); 
        console.log("Nutrition data saved to the database!");
       
    } catch (error) {
        console.error("Error fetching data:", error);
        showErrorMessage("Unable to fetch nutrition data. Please try again later.");
    }
}

// Function to save nutrition data to the database
async function saveNutritionDataToDatabase(foodName, nutritionData) {
    console.log("in save nutrition data outside try");
    try {
        console.log("in save nutrition data");
        const response = await axios.post('/save_nutrition/', {
            food_name: foodName,
            calories: nutritionData.calories,
            protein: nutritionData.protein,
            carbs: nutritionData.carbs,
            fat: nutritionData.fat,
            fiber: nutritionData.fiber,
            sugars: nutritionData.sugars,
            sodium: nutritionData.sodium,
            cholesterol: nutritionData.cholesterol
        }, {
            headers: {
                'Content-Type': 'application/json'  // Add this header to specify JSON format
            }
        });

        console.log("Response",response);
        console.log("Response.data=",response.data);
        console.log("response.data.success",response.data.success);
        console.log("response.data.message=",response.data.message)

        if (response.data.success) {
            console.log("Nutrition data saved successfully!");
        } else {
            console.error("Error saving data:", response.data.message);
        }
    } catch (error) {
        console.error("Error during save operation:", error);
    }
}


// Function to show an error message in the nutrition card
function showErrorMessage(message) {
    console.log("in show error message");
    const nutritionResult = document.getElementById('nutritionResult');
    nutritionResult.innerHTML = `
        <div class="alert alert-danger text-center" role="alert">
            <i class="bi bi-exclamation-triangle-fill"></i> ${message}
        </div>
    `;
}

// Event listener for form submission
if (foodForm) {
    let userInput = document.getElementById("foodInput");
    foodForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevents form submission
        let userInputValue = userInput.value.trim();
        console.log("Input =", userInputValue);

        if (!userInputValue) {
            console.log("Input is empty. Enter a food name.");
            showErrorMessage("Please enter a food name.");
            return;
        }

        let matchedFoodId = await fetchFoodId(userInputValue); // Get the ID of the food matched from user input
        console.log("Matched ID =", matchedFoodId);

        if (matchedFoodId) {
            await fetchNutritionData(matchedFoodId,userInputValue); // Fetch and display nutrition data
        } else {
            console.log("No matched food found. Please try a different search.");
            showErrorMessage("No data found for the entered food item.");
        }
    });
}
 
