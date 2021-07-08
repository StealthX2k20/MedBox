# Prechecks to ensure data validity in model

from pymodm.errors import ValidationError
import datetime


def valid_transaction_details(transactions):
    """
    Desc:
        Function to validate if details of transactions are valid or not
    Args:
        List of transations
    Return:
        Void, but raises error if any transaction detail is invalid
    """
    transaction_types = ["buy", "sell"]
    for transaction in transactions:
        if transaction["transaction_type"] not in transaction_types:
            raise ValidationError("Invalid transaction type")
        valid_contact_info(transaction["customer_contact_number"])
        if transaction["quantity"] <= 0:
            raise ValidationError("Quantity in transaction must be a positive integer")


def valid_medicine_details(medicines):
    """
    Desc:
        Function to validate if details of medicines are valid or not
    Args:
        List of medicines
    Return:
        Void, but raises error if any medicine detail is invalid
    """
    for medicine in medicines:
        medicine = medicine.to_son().to_dict()
        if medicine["expiry_date"] <= datetime.datetime.now():
            raise ValidationError("Medicine already expired or expiring today")
        if medicine["medicine_cost_price"] <= 0:
            raise ValidationError("Medicine costprice must be a positive integer")
        if medicine["medicine_selling_price"] <= 0:
            raise ValidationError("Medicine selling must be a positive integer")
        if medicine["dose_in_mg"] < 0:
            raise ValidationError("Medicine dose must be a positive integer")
        if medicine["quantity_in_stock"] < 0:
            raise ValidationError("Medicine quantities must be a non-negative integer")
        if medicine["quantity_sold_since_last_mr_visit"] < 0:
            raise ValidationError(
                "Medicine quantity sold since last MR visit must be a non-negative integer"
            )
        if medicine.get("transactions"):
            valid_transaction_details(medicine["transactions"])


def valid_contact_info(contact_number):
    """
    Desc:
        Function to validate if contact number is valid or not
    Args:
        An integer denoting the contact number
    Return:
        Void, but raises error if contact number is invalid
    """
    if contact_number < 0 or len(str(contact_number)) != 10:
        raise ValidationError("Invalid contact info")
