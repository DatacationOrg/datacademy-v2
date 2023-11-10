"""File containing your first REST API!"""

from datacademy.modules import Module05
from fastapi import FastAPI

# DO NOT EDIT: Initialize module and load customers
module = Module05()
customers = module.load_customers()

# DO NOT EDIT: Initialize FastAPI
app = FastAPI()


"""
API GET requests
"""


# Example GET request
@app.get("/get-customer/{customer_id}")
def get_customer(customer_id: int) -> dict[str, str]:
    """Get a customer by its ID.

    Args:
        customer_id (int): Customer ID.

    Returns:
        dict[str, str]: Customer details.
    """
    if customer_id not in customers:
        return {"Error": "Customer does not exists yet."}
    return customers[customer_id]


# TODO: Create GET request with end point: "/get-customer-by-name/{last_name}"
@app.get("/get-customer-by-name/{last_name}")
def get_customer_by_name(last_name: str) -> dict[str, str]:
    """Get a customer by name.

    Args:
        last_name (str): Last name.

    Returns:
        dict[str, str]: Customer details.
    """
    for customer_id in customers:
        if customers[customer_id]["last_name"] == last_name:
            return customers[customer_id]

    return {"Error": f"Customer with last name: '{last_name}' does not exists"}


# TODO: Create GET request with end point: "/get-customers/"
@app.get("/get-customers/")
def get_customers(skip: int = 0, limit: int = 3) -> dict[int, dict[str, str]]:
    """Get all customers.

    Args:
        skip (int, optional): Records to skip. Defaults to 0.
        limit (int, optional): Limit number of returned customers to. Defaults to 3.

    Returns:
        dict[int, dict[str, str]]: Dictionary of customer id to customer details.
    """
    return {i: customers[i] for i in range(skip, min(skip + limit, len(customers)))}


"""
API POST requests
"""


# Example POST request
@app.post("/create-customer/{customer_id}")
def create_customer(customer_id: int, first_name: str, last_name: str, address: str) -> dict[str, str]:
    """Create a new customer.

    Args:
        customer_id (int): Customer ID.
        first_name (str): First name.
        last_name (str): Last name.
        address (str): Address.

    Returns:
        dict[str, str]: Customer details.
    """
    if customer_id in customers:
        return {"Error": f"customerId already used, next id available is: {max(customers.keys())+1}."}

    if (customer_id - max(customers.keys())) > 1:
        return {"Error": f"customerId do not fit neatly together, next id available is: {max(customers.keys())+1}."}

    customers[customer_id] = {"first_name": first_name, "last_name": last_name, "address": address}
    return customers[customer_id]


# TODO: Create POST request with end point: "/create-customer-auto-increment/"
@app.post("/create-customer-auto-increment/")
def create_customer_auto_increment(first_name: str, last_name: str, address: str) -> dict[str, str]:
    """Create a new customer using auto-increment.

    Args:
        first_name (str): First name.
        last_name (str): Last name.
        address (str): Address.

    Returns:
        dict[str, str]: Customer details.
    """
    customer_id = max(customers.keys()) + 1

    customers[customer_id] = {"first_name": first_name, "last_name": last_name, "address": address}
    return customers[customer_id]


"""
API PUT requests
"""


@app.put("/update-customer-address/{customer_id}")
def update_customer_address(customer_id: int, address: str) -> dict[str, str]:
    """Update the address of a customer.

    Args:
        customer_id (int): Customer ID.
        address (str): Customer address.

    Returns:
        dict[str, str]: Updated customer.
    """
    if customer_id not in customers:
        return {"Error": "Customer does not exists."}

    customers[customer_id]["address"] = address
    return customers[customer_id]


# TODO: Create PUT request with end point: "/update-customer-address-by-name/"
@app.put("/update-customer-address-by-name/")
def update_customer_address_by_name(first_name: str, last_name: str, address: str) -> dict[str, str]:
    """Update a customer's address by name.

    Args:
        first_name (str): First name.
        last_name (str): Last name.
        address (str): Address.

    Returns:
        dict[str, str]: Customer details.
    """
    for customer_id in customers:
        if customers[customer_id]["first_name"] == first_name and customers[customer_id]["last_name"] == last_name:
            customers[customer_id]["address"] = address

            return customers[customer_id]

    return {"Error": f"No customer named {first_name} {last_name} exists."}


"""
API DELETE requests
"""


@app.delete("/delete-customer/{customer_id}")
def delete_customer(customer_id: int) -> dict[str, str]:
    """Delete a customer.

    Args:
        customer_id (int): Customer ID.

    Returns:
        dict[str, str]: Error or success message.
    """
    if customer_id not in customers:
        return {"Error": "Customer does not exists."}

    del customers[customer_id]
    return {"Message": f"Customer {customer_id} deleted successfully."}


# TODO: Create DELETE request with end point: "/delete-customer-by-name/"
@app.delete("/delete-customer-by-name/")
def delete_customer_by_name(first_name: str, last_name: str) -> dict[str, str]:
    """Delete a customer by name.

    Args:
        first_name (str): First name.
        last_name (str): Last name.

    Returns:
        dict[str, str]: Customer details.
    """
    for customer in customers:
        if customers[customer]["first_name"] == first_name and customers[customer]["last_name"] == last_name:
            del customers[customer]
            return {"Message": f"Customer {first_name} {last_name} deleted successfully."}

    return {"Error": "The customer you are trying to delete does not exist."}
