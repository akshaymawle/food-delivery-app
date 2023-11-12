import streamlit as st

# Sample data for food items
food_items = {
    1: {"Name": "Tandoori Chicken", "Quantity": "4 pieces", "Price": 240, "Discount": 0, "Stock": 50},
    2: {"Name": "Vegan Burger", "Quantity": "1 piece", "Price": 320, "Discount": 10, "Stock": 30},
    3: {"Name": "Truffle Cake", "Quantity": "500gm", "Price": 900, "Discount": 5, "Stock": 20}
}

# Sample data for user profiles
users = {}

# Sample data for user orders
orders = []

# Function to add a new food item
def add_food_item(name, quantity, price, discount, stock):
    food_id = max(food_items.keys()) + 1
    food_items[food_id] = {"Name": name, "Quantity": quantity, "Price": price, "Discount": discount, "Stock": stock}

# Function to edit food items
def edit_food_item(food_id, name, quantity, price, discount, stock):
    if food_id in food_items:
        food_items[food_id] = {"Name": name, "Quantity": quantity, "Price": price, "Discount": discount, "Stock": stock}

# Function to remove a food item
def remove_food_item(food_id):
    if food_id in food_items:
        del food_items[food_id]

# Function to register a new user
def register_user(full_name, phone_number, email, address, password):
    user_id = len(users) + 1
    users[user_id] = {"FullName": full_name, "PhoneNumber": phone_number, "Email": email, "Address": address, "Password": password}
    return user_id

# Function to authenticate a user
def authenticate_user(email, password):
    for user_id, user_data in users.items():
        if user_data["Email"] == email and user_data["Password"] == password:
            return user_id
    return None

# Function to place a new order
def place_order(user_id, selected_items):
    user_order = {"UserID": user_id, "Items": selected_items}
    orders.append(user_order)

# Streamlit UI
st.title("Food Ordering App")

# Admin Section
if st.button("Admin"):
    st.subheader("Food Items")
    for food_id, item_data in food_items.items():
        st.write(f"FoodID: {food_id}, Name: {item_data['Name']}, Quantity: {item_data['Quantity']}, "
                 f"Price: {item_data['Price']}, Discount: {item_data['Discount']}, Stock: {item_data['Stock']}")

    st.subheader("Add New Food Item")
    name = st.text_input("Name:")
    quantity = st.text_input("Quantity:")
    price = st.number_input("Price:")
    discount = st.number_input("Discount:")
    stock = st.number_input("Stock:")

    if st.button("Add Food"):
        add_food_item(name, quantity, price, discount, stock)
        st.success("Food item added successfully!")

    st.subheader("Edit Food Item")
    food_id_to_edit = st.number_input("Enter FoodID to edit:")
    if food_id_to_edit in food_items:
        new_name = st.text_input("New Name:", value=food_items[food_id_to_edit]["Name"])
        new_quantity = st.text_input("New Quantity:", value=food_items[food_id_to_edit]["Quantity"])
        new_price = st.number_input("New Price:", value=food_items[food_id_to_edit]["Price"])
        new_discount = st.number_input("New Discount:", value=food_items[food_id_to_edit]["Discount"])
        new_stock = st.number_input("New Stock:", value=food_items[food_id_to_edit]["Stock"])

        if st.button("Edit Food"):
            edit_food_item(food_id_to_edit, new_name, new_quantity, new_price, new_discount, new_stock)
            st.success("Food item edited successfully!")

    st.subheader("Remove Food Item")
    food_id_to_remove = st.number_input("Enter FoodID to remove:")
    if st.button("Remove Food"):
        remove_food_item(food_id_to_remove)
        st.success("Food item removed successfully!")

# User Section
elif st.button("User"):
    st.subheader("User Registration")
    full_name = st.text_input("Full Name:")
    phone_number = st.text_input("Phone Number:")
    email = st.text_input("Email:")
    address = st.text_input("Address:")
    password = st.text_input("Password:", type="password")

    if st.button("Register"):
        user_id = register_user(full_name, phone_number, email, address, password)
        st.success("Registration successful! Please log in.")

    st.subheader("User Login")
    login_email = st.text_input("Email:")
    login_password = st.text_input("Password:", type="password")

    if st.button("Log In"):
        user_id = authenticate_user(login_email, login_password)
        if user_id:
            st.success("Login successful!")

            # User functionalities after login
            option = st.selectbox("Choose an option:", ["Place New Order", "Order History", "Update Profile"])

            if option == "Place New Order":
                st.subheader("Place New Order")
                st.write("Select food items from the list:")
                for food_id, item_data in food_items.items():
                    st.checkbox(f"{item_data['Name']} ({item_data['Quantity']}) [INR {item_data['Price']}]")

                if st.button("Place Order"):
                    selected_items = [food_items[food_id] for food_id in food_items if
                                      st.checkbox(f"{food_items[food_id]['Name']} ({food_items[food_id]['Quantity']}) [INR {food_items[food_id]['Price']}]")]
                    place_order(user_id, selected_items)
                    st.success("Order placed successfully!")

            elif option == "Order History":
                st.subheader("Order History")
                user_orders = [order for order in orders if order["UserID"] == user_id]
                for order in user_orders:
                    st.write(f"Order ID: {orders.index(order) + 1}")
                    for item in order["Items"]:
                        st.write(f"{item['Name']} ({item['Quantity']}) [INR {item['Price']}]")
                    st.write("--------------")

            elif option == "Update Profile":
                st.subheader("Update Profile")
                new_full_name = st.text_input("New Full Name:", value=users[user_id]["FullName"])
                new_phone_number = st.text_input("New Phone Number:", value=users[user_id]["PhoneNumber"])
                new_email = st.text_input("New Email:", value=users[user_id]["Email"])
                new_address = st.text_input("New Address:", value=users[user_id]["Address"])
                new_password = st.text_input("New Password:", type="password", value=users[user_id]["Password"])

                if st.button("Update Profile"):
                    users[user_id]["FullName"] = new_full_name
                    users[user_id]["PhoneNumber"] = new_phone_number
                    users[user_id]["Email"] = new_email
                    users[user_id]["Address"] = new_address
                    users[user_id]["Password"] = new_password
                    st.success("Profile updated successfully!")

        else:
            st.error("Invalid email or password. Please try again.")
