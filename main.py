from drafter import *
from dataclasses import dataclass

hide_debug_information()
set_website_framed(False)
set_website_title("Your Drafter Website")
set_site_information(
    "Ally Malin",
    """
Order form for ordering cakes for personal business. Ran out of time with API, but intended to link form to google sheets and to add AI generated images of cakes based on their order.
""",
    [],
    [],
    [],
)

set_site_information(
    author="allycm@udel.edu",
    description="""takes orders for cakes.""",
    sources=["none"],
    planning=["none"],
    links=["https://github.com/ud-s24-cs1/website-acbart"]
)

@dataclass
class Item:
    cake_flavor: str
    frosting_flavor: str
    size: str
    quantity: str
    decoration_description: str

@dataclass
class Order:
    name: str
    phone: str
    email: str
    pickup_date: str
    pickup_time: str
    note: str

@dataclass
class State:
    orders: list[Order]
    cart: list[Item]

@route
def index(state: State)->Page:
    """starting page for website"""
    return Page(state, content=[
        "Cakes by Ally",
        "Start by browsing cake options, and then fill out order information after adding cakes to cart.", 
        Button(text="Browse Cake Options", url="/cakes_home"),
        Button(text="Cart", url="/cart"), 
        Button(text="Order Form", url="/order_form")
                                ]
                )
@route
def cakes_home(state: State)->Page:
    return Page(state, content=[
        "Choose cake flavor. It is vanilla by default.",
        SelectBox("cake_flavor", ["Vanilla", "Chocolate", "Marble"], "Vanilla"),
        "All cakes are made with buttercream frosting. Select flavor below. It is vanilla by default.",
        SelectBox("frosting_flavor", ["Strawberry", "Vanilla", "Chocolate"], "Vanilla"),
        "Choose from the size and shape options below. It is 9in round by default.",
        SelectBox("size", ["4in round", "9in round", "small sheetcake", "large sheetcake"], "9in round"), 
        "What quantity would you like? Because of kitchen limitations, the number is capped at 3.",
        SelectBox("quantity", ["1", "2", "3"]),
        "Add any description of decorations below. Is this cake for a specific event or theme? What colors or design do you want?",
        TextBox("description", ""),
        "", 
        Button(text="Add to Cart", url="/add_to_cart"), 
        Button(text="View Cart", url="/cart"), 
        Button(text="Return Home", url="/index")
                                ]
                )

@route
def add_to_cart(state: State, cake_flavor, frosting_flavor, size, quantity, description):
    new_cart=Item(cake_flavor, frosting_flavor, size, quantity, description)
    cart_list=state.cart
    cart_list.append(new_cart)
    return Page(state, content=[
        "Your item/s was added to cart.",
        Button(text="Continue Shopping", url="/cakes_home"),
        Button(text="View Cart", url="/cart"),
        Button(text="Return Home", url="/index")
                                ]
                )

@route
def cart(state: State)->Page:
    """shows users their cart"""
    if state.cart==[]:
        return Page(state, content=[
            "Your cart is empty. Click the button below to browse cakes to add to cart.",
            Button(text="Browse Cakes", url="/cakes_home")
                                    ]
                    )
    else: 
        return Page(state, content=[
            Header("Cart"),
            Table(state.cart),
            Button(text="Checkout", url="/order_form"),
            Button(text="Add Cakes", url="/cakes_home"),
            Button(text="Return to Homepage", url="/index")
                                    ]
                    )
    
@route
def order_form(state: State)->Page:
    """users input their information into website"""
    return Page(state, content=[
        "Customer Information", 
        "Name: (required)",
        TextBox("name", ""),
        "Phone Number: (required)",
        TextBox("phone_number", ""),
        "Email: (required)",
        TextBox("email", ""),
        "Pickup Date: (required)",
        TextBox("date", ""),
        "Pickup Time: (required)",
        TextBox("time", ""),
        "Verify items below:",
        Table(state.cart), 
        "Notes:", 
        TextBox("note", ""),
        "",
        Button(text="Complete Order", url="/order_helper"), 
        Button(text="Cancel", url="/index")
                                ]
                )

@route 
def order_helper(state: State, name: str, phone_number: str, email: str, date: str, time: str, note: str)->Page:
    """helps save user info to state"""
    new_order=Order(name, phone_number, email, date, time, note)
    orders=state.orders
    orders.append(new_order)
    return Page(state, content=[
        "Your order was successfully submitted. Thank you!",
        Button(text="New Order", url="/order_form"),
        Button(text="Home", url="/index")
                                ]
                )

initial_state=State(orders=[], cart=[])
start_server(initial_state)
