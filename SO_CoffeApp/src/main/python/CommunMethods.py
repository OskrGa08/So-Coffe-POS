import tkinter as tk

# Sample data (replace with your actual data)
products = {
    "Product 1": 10.00,
    "Product 2": 15.50,
    "Product 3": 22.99
}

# Function to create buttons for each product
def create_product_buttons():
    for product_name, price in products.items():
        button = tk.Button(frame1, text=product_name, command=lambda product_name=product_name: add_to_cart(product_name))
        button.pack(side=tk.LEFT, padx=5, pady=5)

# Function to add selected product to the cart frame (frame2)
def add_to_cart(product_name):
    product_price = products[product_name]
    cart_label = tk.Label(frame2, text=f"{product_name}: ${product_price:.2f}")
    cart_label.pack()

# Create the main window
window = tk.Tk()
window.title("Punto de Venta")

# Create two frames for product buttons and cart items
frame1 = tk.Frame(window)
frame1.pack(side=tk.TOP, pady=10)

frame2 = tk.Frame(window)
frame2.pack(side=tk.TOP, pady=10)

# Create and display product buttons
create_product_buttons()

# Calculate and display total (replace with actual calculation logic)
total_label = tk.Label(frame2, text="Total: $0.00")
total_label.pack()

# Run the main event loop
window.mainloop()
