from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from movies_data import MOVIES
from comedy_movies import COMEDY_MOVIES
from database import Database

# Combine all movies
ALL_MOVIES = MOVIES + COMEDY_MOVIES

app = Flask(__name__)
app.secret_key = 'smartpick_secret_key_2024'  # Change this in production
db = Database()

from jobs_data import JOBS_DATABASE as JOBS

from recipes_data import RECIPES_DATABASE as RECIPES

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db.authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            return redirect(url_for('smart_pick'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        if len(password) < 6:
            return render_template('register.html', error='Password must be at least 6 characters')
        
        if db.create_user(username, email, password):
            return render_template('register.html', success='Account created successfully! Please login.')
        else:
            return render_template('register.html', error='Username or email already exists')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('smart_pick'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = {
        'id': session['user_id'],
        'username': session['username'],
        'email': session['email']
    }
    
    movie_history = db.get_user_movie_history(session['user_id'])
    basket_items = db.get_user_basket(session['user_id'])
    
    return render_template('profile.html', user=user, movie_history=movie_history, basket_items=basket_items)

@app.route('/')
def smart_pick():
    user = None
    if 'user_id' in session:
        user = {
            'id': session['user_id'],
            'username': session['username'],
            'email': session['email']
        }
    return render_template('smart_pick.html', user=user)

@app.route('/movies')
def movies():
    user = None
    if 'user_id' in session:
        user = {
            'id': session['user_id'],
            'username': session['username'],
            'email': session['email']
        }
    years = sorted(set(movie['year'] for movie in ALL_MOVIES), reverse=True)
    return render_template('movies.html', movies=ALL_MOVIES, years=years, user=user)

@app.route('/watch-movie', methods=['POST'])
def watch_movie():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login to track movies'}), 401
    
    movie_id = request.json.get('movie_id')
    movie_title = request.json.get('movie_title')
    
    if movie_id and movie_title:
        db.add_movie_to_history(session['user_id'], movie_id, movie_title)
        return jsonify({'success': True, 'message': 'Movie added to your watch history!'})
    
    return jsonify({'error': 'Invalid movie data'}), 400

@app.route('/jobs')
def jobs():
    user = None
    if 'user_id' in session:
        user = {
            'id': session['user_id'],
            'username': session['username'],
            'email': session['email']
        }
    all_skills = sorted(set(skill for skills in JOBS.values() for skill in skills))
    return render_template('jobs.html', jobs=JOBS, all_skills=all_skills, user=user)

@app.route('/grocery')
def grocery():
    user = None
    if 'user_id' in session:
        user = {
            'id': session['user_id'],
            'username': session['username'],
            'email': session['email']
        }
    return render_template('grocery.html', recipes=RECIPES, user=user)

@app.route('/recommend')
def recommend():
    genre = request.args.get('genre', '')
    year = request.args.get('year', '')
    
    filtered_movies = ALL_MOVIES
    if genre:
        filtered_movies = [movie for movie in filtered_movies if movie['genre'].lower() == genre.lower()]
    if year:
        filtered_movies = [movie for movie in filtered_movies if str(movie['year']) == year]
    
    return jsonify({'genre': genre, 'year': year, 'movies': filtered_movies})

@app.route('/match-jobs', methods=['POST'])
def match_jobs():
    user_skills = set(request.json.get('skills', []))
    matching_jobs = [job for job, skills in JOBS.items() if user_skills.intersection(skills)]
    return jsonify({'jobs': matching_jobs})

def categorize_ingredients(ingredients):
    categories = {
        'Fresh Produce': ['Onion', 'Tomato', 'Garlic', 'Ginger', 'Bell Peppers', 'Potatoes', 'Lettuce', 'Cucumber', 'Carrots', 'Celery', 'Spinach', 'Cauliflower', 'Eggplant', 'Peas', 'Lemon', 'Lime', 'Cilantro', 'Mint', 'Green Chili', 'Broccoli', 'Cabbage', 'Mushrooms'],
        'Meat & Seafood': ['Chicken', 'Fish', 'Mutton', 'Prawns', 'Minced Meat', 'Bacon', 'Ground Chicken', 'Lamb', 'Beef', 'Pork', 'Shrimp', 'Salmon', 'Tuna'],
        'Dairy & Eggs': ['Milk', 'Butter', 'Cream', 'Yogurt', 'Cheese', 'Parmesan Cheese', 'Mozzarella Cheese', 'Feta Cheese', 'Paneer', 'Ghee', 'Eggs', 'Heavy Cream', 'Sour Cream'],
        'Grains & Cereals': ['Rice', 'Basmati Rice', 'Brown Rice', 'Wheat Flour', 'All Purpose Flour', 'Bread', 'Pasta', 'Noodles', 'Quinoa', 'Oats', 'Barley'],
        'Legumes & Pulses': ['Chickpeas', 'Lentils', 'Kidney Beans', 'Black Beans', 'Urad Dal', 'Moong Dal', 'Toor Dal', 'Chana Dal', 'Masoor Dal'],
        'Spices & Seasonings': ['Salt', 'Black Pepper', 'Cumin', 'Turmeric', 'Garam Masala', 'Coriander', 'Red Chili Powder', 'Paprika', 'Oregano', 'Basil', 'Thyme', 'Bay Leaves', 'Cardamom', 'Cinnamon', 'Cloves'],
        'Oils & Condiments': ['Cooking Oil', 'Olive Oil', 'Coconut Oil', 'Mustard Oil', 'Sesame Oil', 'Vinegar', 'Soy Sauce', 'Tomato Sauce', 'Ketchup', 'Mayonnaise', 'Mustard'],
        'Pantry Staples': ['Sugar', 'Brown Sugar', 'Honey', 'Coconut Milk', 'Tomato Paste', 'Baking Powder', 'Baking Soda', 'Vanilla Extract', 'Cornstarch', 'Breadcrumbs'],
        'Frozen & Canned': ['Frozen Peas', 'Frozen Corn', 'Canned Tomatoes', 'Coconut Milk Can', 'Tomato Puree', 'Chicken Broth', 'Vegetable Broth'],
        'Other': []
    }
    
    categorized = {cat: [] for cat in categories.keys()}
    
    for ingredient in ingredients:
        placed = False
        for category, items in categories.items():
            if any(item.lower() in ingredient.lower() for item in items):
                categorized[category].append(ingredient)
                placed = True
                break
        if not placed:
            categorized['Other'].append(ingredient)
    
    return {k: v for k, v in categorized.items() if v}

def add_quantities(ingredients, persons=4):
    # Base quantities for 4 people
    base_quantities = {
        # Grains & Cereals
        'Rice': {'amount': 2, 'unit': 'cups', 'category': 'grain'},
        'Basmati Rice': {'amount': 2, 'unit': 'cups', 'category': 'grain'},
        'Flour': {'amount': 2, 'unit': 'cups', 'category': 'grain'},
        'Wheat Flour': {'amount': 2, 'unit': 'cups', 'category': 'grain'},
        'All Purpose Flour': {'amount': 2, 'unit': 'cups', 'category': 'grain'},
        'Pasta': {'amount': 1, 'unit': 'lb', 'category': 'grain'},
        'Bread': {'amount': 1, 'unit': 'loaf', 'category': 'grain'},
        
        # Proteins
        'Chicken': {'amount': 2, 'unit': 'lbs', 'category': 'protein'},
        'Chicken Breast': {'amount': 2, 'unit': 'lbs', 'category': 'protein'},
        'Fish': {'amount': 1.5, 'unit': 'lbs', 'category': 'protein'},
        'Mutton': {'amount': 2, 'unit': 'lbs', 'category': 'protein'},
        'Minced Meat': {'amount': 1, 'unit': 'lb', 'category': 'protein'},
        'Prawns': {'amount': 1, 'unit': 'lb', 'category': 'protein'},
        'Eggs': {'amount': 8, 'unit': 'pieces', 'category': 'protein'},
        
        # Vegetables
        'Onion': {'amount': 4, 'unit': 'medium', 'category': 'vegetable'},
        'Tomato': {'amount': 6, 'unit': 'medium', 'category': 'vegetable'},
        'Potatoes': {'amount': 2, 'unit': 'lbs', 'category': 'vegetable'},
        'Garlic': {'amount': 1, 'unit': 'bulb', 'category': 'vegetable'},
        'Ginger': {'amount': 100, 'unit': 'grams', 'category': 'vegetable'},
        'Bell Peppers': {'amount': 3, 'unit': 'pieces', 'category': 'vegetable'},
        'Green Chili': {'amount': 10, 'unit': 'pieces', 'category': 'vegetable'},
        'Spinach': {'amount': 1, 'unit': 'bunch', 'category': 'vegetable'},
        'Cauliflower': {'amount': 1, 'unit': 'medium head', 'category': 'vegetable'},
        'Carrots': {'amount': 1, 'unit': 'lb', 'category': 'vegetable'},
        'Peas': {'amount': 1, 'unit': 'cup', 'category': 'vegetable'},
        'Lemon': {'amount': 4, 'unit': 'pieces', 'category': 'vegetable'},
        
        # Dairy
        'Milk': {'amount': 2, 'unit': 'cups', 'category': 'dairy'},
        'Yogurt': {'amount': 1, 'unit': 'cup', 'category': 'dairy'},
        'Butter': {'amount': 200, 'unit': 'grams', 'category': 'dairy'},
        'Ghee': {'amount': 200, 'unit': 'grams', 'category': 'dairy'},
        'Cream': {'amount': 1, 'unit': 'cup', 'category': 'dairy'},
        'Paneer': {'amount': 400, 'unit': 'grams', 'category': 'dairy'},
        'Cheese': {'amount': 200, 'unit': 'grams', 'category': 'dairy'},
        
        # Legumes
        'Lentils': {'amount': 2, 'unit': 'cups', 'category': 'legume'},
        'Dal': {'amount': 2, 'unit': 'cups', 'category': 'legume'},
        'Chickpeas': {'amount': 2, 'unit': 'cups', 'category': 'legume'},
        'Kidney Beans': {'amount': 2, 'unit': 'cups', 'category': 'legume'},
        'Urad Dal': {'amount': 1, 'unit': 'cup', 'category': 'legume'},
        
        # Oils & Liquids
        'Oil': {'amount': 500, 'unit': 'ml', 'category': 'oil'},
        'Cooking Oil': {'amount': 500, 'unit': 'ml', 'category': 'oil'},
        'Olive Oil': {'amount': 250, 'unit': 'ml', 'category': 'oil'},
        'Coconut Oil': {'amount': 200, 'unit': 'ml', 'category': 'oil'},
        'Coconut Milk': {'amount': 2, 'unit': 'cans', 'category': 'liquid'},
        
        # Spices (small quantities)
        'Salt': {'amount': 2, 'unit': 'tsp', 'category': 'spice'},
        'Pepper': {'amount': 1, 'unit': 'tsp', 'category': 'spice'},
        'Turmeric': {'amount': 2, 'unit': 'tsp', 'category': 'spice'},
        'Cumin': {'amount': 2, 'unit': 'tsp', 'category': 'spice'},
        'Coriander': {'amount': 2, 'unit': 'tsp', 'category': 'spice'},
        'Garam Masala': {'amount': 2, 'unit': 'tsp', 'category': 'spice'},
        'Red Chili': {'amount': 1, 'unit': 'tsp', 'category': 'spice'},
        
        # Pantry
        'Sugar': {'amount': 1, 'unit': 'cup', 'category': 'pantry'},
        'Baking Powder': {'amount': 2, 'unit': 'tsp', 'category': 'pantry'},
        'Vanilla': {'amount': 1, 'unit': 'tsp', 'category': 'pantry'},
    }
    
    # Calculate multiplier based on person count
    multiplier = persons / 4.0
    
    result = []
    for ingredient in ingredients:
        matched = False
        for key, data in base_quantities.items():
            if key.lower() in ingredient.lower():
                # Calculate quantity based on person count
                base_amount = data['amount']
                unit = data['unit']
                category = data['category']
                
                # Apply different scaling for different categories
                if category == 'spice':
                    # Spices don't scale linearly
                    scaled_amount = base_amount * (1 + (multiplier - 1) * 0.5)
                elif category == 'oil':
                    # Oil scales moderately
                    scaled_amount = base_amount * (1 + (multiplier - 1) * 0.7)
                else:
                    # Most ingredients scale linearly
                    scaled_amount = base_amount * multiplier
                
                # Format the amount nicely
                if scaled_amount < 1 and unit not in ['pieces', 'tsp', 'tbsp']:
                    formatted_amount = f"{scaled_amount:.1f}"
                elif scaled_amount.is_integer():
                    formatted_amount = f"{int(scaled_amount)}"
                else:
                    formatted_amount = f"{scaled_amount:.1f}"
                
                result.append(f"{formatted_amount} {unit} {ingredient}")
                matched = True
                break
        
        if not matched:
            # Default quantities for unmatched ingredients
            result.append(f"As needed - {ingredient}")
    
    return result

@app.route('/generate-list', methods=['POST'])
def generate_list():
    selected_recipes = request.json.get('recipes', [])
    persons = request.json.get('persons', 4)
    all_ingredients = set()
    
    for recipe in selected_recipes:
        if recipe in RECIPES:
            all_ingredients.update(RECIPES[recipe])
    
    ingredients_with_qty = add_quantities(sorted(list(all_ingredients)), persons)
    categorized = categorize_ingredients(ingredients_with_qty)
    
    # Save to user's basket if logged in
    if 'user_id' in session and selected_recipes:
        for recipe in selected_recipes:
            if recipe in RECIPES:
                db.add_to_basket(session['user_id'], recipe, RECIPES[recipe], persons)
    
    # Generate cooking tips based on person count
    tips = [
        f"💡 Shopping for {persons} people - check expiry dates for bulk items.",
        f"💡 Prep all ingredients before cooking for {persons} people - it saves time!",
        "💡 Store fresh herbs in water like flowers to keep them fresh longer.",
        "💡 Buy spices in small quantities - they lose flavor over time.",
        f"💡 Consider batch cooking for {persons} people to save time during the week.",
        "💡 Fresh ingredients taste better - buy vegetables and meat closer to cooking day.",
        "💡 Keep a well-stocked pantry with basics like oil, salt, and spices."
    ]
    
    import random
    tip = random.choice(tips)
    
    return jsonify({
        'categorized_ingredients': categorized,
        'total_count': len(ingredients_with_qty),
        'persons': persons,
        'tip': tip,
        'saved_to_basket': 'user_id' in session
    })

@app.route('/clear-basket', methods=['POST'])
def clear_basket():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    db.clear_user_basket(session['user_id'])
    return jsonify({'success': True, 'message': 'Basket cleared successfully!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)