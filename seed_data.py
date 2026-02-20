import os
import django

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fooddelivery.settings')
django.setup()

from products.models import Product

# ---------------------- UPDATED ITEMS ----------------------

items = [
    # ------------------ Pizza Ghar ------------------
    {'name': 'Classic Burger', 'res': 'Pizza Ghar', 'cat': 'Burger', 'price': 150, 'img': 'burger.png'},
    {'name': 'Cheese Loaded Burger', 'res': 'Pizza Ghar', 'cat': 'Burger', 'price': 180, 'img': 'burger.png'},
    {'name': 'Chicken Crunch Burger', 'res': 'Pizza Ghar', 'cat': 'Burger', 'price': 200, 'img': 'burger.png'},
    {'name': 'Veggie Delight Pizza', 'res': 'Pizza Ghar', 'cat': 'Pizza', 'price': 250, 'img': 'pizza.png'},
    {'name': 'Spicy Chicken Pizza', 'res': 'Pizza Ghar', 'cat': 'Pizza', 'price': 350, 'img': 'pizza.png'},
    {'name': 'Margherita Special', 'res': 'Pizza Ghar', 'cat': 'Pizza', 'price': 220, 'img': 'pizza.png'},
    {'name': 'Chicken Steamed Momo', 'res': 'Pizza Ghar', 'cat': 'Momo', 'price': 120, 'img': 'momo.png'},
    {'name': 'Buff Juicy Momo', 'res': 'Pizza Ghar', 'cat': 'Momo', 'price': 130, 'img': 'momo.png'},
    {'name': 'Crispy French Fries', 'res': 'Pizza Ghar', 'cat': 'Snacks', 'price': 100, 'img': 'fries.png'},
    {'name': 'Chilled Cold Drink', 'res': 'Pizza Ghar', 'cat': 'Beverage', 'price': 60, 'img': 'drink.png'},

    # ------------------ Mantra Thakali ------------------
    {'name': 'Chicken Thali Set', 'res': 'Mantra Thakali', 'cat': 'Meal', 'price': 350, 'img': 'thali_food.png'},
    {'name': 'Mutton Thali Deluxe', 'res': 'Mantra Thakali', 'cat': 'Meal', 'price': 450, 'img': 'thali_food.png'},
    {'name': 'Veg Thali Combo', 'res': 'Mantra Thakali', 'cat': 'Meal', 'price': 250, 'img': 'thali_food.png'},
    {'name': 'Traditional Dal Bhat', 'res': 'Mantra Thakali', 'cat': 'Meal', 'price': 200, 'img': 'thali_food.png'},
    {'name': 'Dhido', 'res': 'Mantra Thakali', 'cat': 'Side Dish', 'price': 120, 'img': 'dhido.png'},
    {'name': 'Fresh Sel Roti', 'res': 'Mantra Thakali', 'cat': 'Dessert', 'price': 100, 'img': 'selroti.png'},

    # ------------------ Naivedya ------------------
    {'name': 'Chicken Chowmein Special', 'res': 'Naivedya', 'cat': 'Noodles', 'price': 140, 'img': 'chowmein.png'},
    {'name': 'Veg Chowmein Delight', 'res': 'Naivedya', 'cat': 'Noodles', 'price': 120, 'img': 'chowmein.png'},
    {'name': 'Buff Momo Plate', 'res': 'Naivedya', 'cat': 'Momo', 'price': 130, 'img': 'momo.png'},
    {'name': 'Grilled Chicken Sekuwa', 'res': 'Naivedya', 'cat': 'Grill', 'price': 300, 'img': 'sekuwa.png'},
    {'name': 'Spicy Paneer Chili', 'res': 'Naivedya', 'cat': 'Snacks', 'price': 220, 'img': 'paneer.png'},
    {'name': 'Crispy Spring Roll', 'res': 'Naivedya', 'cat': 'Snacks', 'price': 150, 'img': 'springroll.png'},
    {'name': 'Sweet Lassi Glass', 'res': 'Naivedya', 'cat': 'Beverage', 'price': 90, 'img': 'lassi.png'},

    # ------------------ Star Cafe ------------------
    {'name': 'Chocolate Cream Cake', 'res': 'Star Cafe', 'cat': 'Dessert', 'price': 180, 'img': 'cake.png'},
    {'name': 'Vanilla Fresh Cake', 'res': 'Star Cafe', 'cat': 'Dessert', 'price': 170, 'img': 'cake.png'},
    {'name': 'Soft Cupcake', 'res': 'Star Cafe', 'cat': 'Dessert', 'price': 90, 'img': 'cupcake.png'},
    {'name': 'Glazed Donut Ring', 'res': 'Star Cafe', 'cat': 'Dessert', 'price': 80, 'img': 'donut.png'},
    {'name': 'Chocolate Brownie Bite', 'res': 'Star Cafe', 'cat': 'Dessert', 'price': 120, 'img': 'brownie.png'},
    {'name': 'Thick Milkshake', 'res': 'Star Cafe', 'cat': 'Beverage', 'price': 150, 'img': 'milkshake.png'},
    {'name': 'Creamy Ice Cream Cup', 'res': 'Star Cafe', 'cat': 'Dessert', 'price': 100, 'img': 'icecream.png'},

    # ------------------ 365 Cafe ------------------
    {'name': 'Classic Cappuccino', 'res': '365 Cafe', 'cat': 'Coffee', 'price': 140, 'img': 'coffee.png'},
    {'name': 'Smooth Latte', 'res': '365 Cafe', 'cat': 'Coffee', 'price': 150, 'img': 'coffee.png'},
    {'name': 'Strong Espresso Shot', 'res': '365 Cafe', 'cat': 'Coffee', 'price': 120, 'img': 'coffee.png'},
    {'name': 'Iced Cold Coffee', 'res': '365 Cafe', 'cat': 'Coffee', 'price': 160, 'img': 'coffee.png'},
    {'name': 'Club Sandwich Special', 'res': '365 Cafe', 'cat': 'Snacks', 'price': 220, 'img': 'sandwich.png'},
    {'name': 'Veg Loaded Sandwich', 'res': '365 Cafe', 'cat': 'Snacks', 'price': 180, 'img': 'sandwich.png'},
    {'name': 'Creamy White Pasta', 'res': '365 Cafe', 'cat': 'Snacks', 'price': 250, 'img': 'pasta.png'},
    {'name': 'Fresh Fruit Smoothie', 'res': '365 Cafe', 'cat': 'Beverage', 'price': 170, 'img': 'smoothie.png'},

    # ------------------ Mokshya ------------------
    {'name': 'Special Chicken Biryani', 'res': 'Mokshya', 'cat': 'Rice', 'price': 300, 'img': 'biryani.png'},
    {'name': 'Veg Dum Biryani', 'res': 'Mokshya', 'cat': 'Rice', 'price': 250, 'img': 'biryani.png'},
    {'name': 'Veg Fried Rice', 'res': 'Mokshya', 'cat': 'Rice', 'price': 180, 'img': 'friedrice.png'},
    {'name': 'Homestyle Chicken Curry', 'res': 'Mokshya', 'cat': 'Curry', 'price': 280, 'img': 'curry.png'},
    {'name': 'Roti Meal Set', 'res': 'Mokshya', 'cat': 'Meal', 'price': 200, 'img': 'roti.png'},
    {'name': 'Paneer Butter Masala', 'res': 'Mokshya', 'cat': 'Curry', 'price': 260, 'img': 'paneer.png'},
    {'name': 'Tandoori Chicken Full', 'res': 'Mokshya', 'cat': 'Grill', 'price': 400, 'img': 'tandoori.png'},
    {'name': 'Mineral Water Bottle', 'res': 'Mokshya', 'cat': 'Beverage', 'price': 30, 'img': 'water.png'},
]

# ---------------------- SEED FUNCTION ----------------------

def seed_data():
    # STEP 1: DELETE OLD DATA
    print("Deleting old product data...")
    Product.objects.all().delete()
    print("Database cleared.")

    # STEP 2: LOAD NEW DATA
    print("Seeding new data... Please wait.")
    count = 0
    for item in items:
        Product.objects.create(
            name=item['name'],
            restaurant=item['res'],
            category=item['cat'],
            price=item['price'],
            image=f"images/{item['img']}",
            rating=5.0,
            available=True,
            description=f"Best {item['name']} from {item['res']}. Freshly prepared and delivered hot!"
        )
        count += 1

    print(f"Successfully added {count} new items to the database!")

if __name__ == "__main__":
    seed_data()