from typing import final
import datetime

from django.db import (
    models,
)
from pymodm import (
    MongoModel,
    EmbeddedMongoModel,
    fields,
)

from pymodm.fields import ReferenceField
from pymodm.manager import Manager

from bson.objectid import ObjectId
from .medical_store_model_validation import valid_contact_info, valid_medicine_details

"""
'CharField', 'IntegerField', 'BigIntegerField', 'ObjectIdField',
'BinaryField', 'BooleanField', 'DateTimeField', 'Decimal128Field',
'EmailField', 'FileField', 'ImageField', 'FloatField',
'GenericIPAddressField', 'URLField', 'UUIDField',
'RegularExpressionField', 'JavaScriptField', 'TimestampField',
'DictField', 'OrderedDictField', 'ListField', 'PointField',
'LineStringField', 'PolygonField', 'MultiPointField',
'MultiLineStringField', 'MultiPolygonField', 'GeometryCollectionField',
'EmbeddedDocumentField', 'EmbeddedDocumentListField', 'ReferenceField'
"""


class Transaction(EmbeddedMongoModel):
    """
    1) Transaction model to contain details about transaction
    2) Transactions can be of 2 types Buy or Sell
    3) Embedded inside Medicine Model
    """

    transaction_id = fields.ObjectIdField(
        verbose_name="transaction_id",
        mongo_name="_id",
        primary_key=True,
        default=ObjectId(),
    )
    transaction_type = fields.CharField(
        verbose_name="transaction_type", mongo_name="transaction_type", required=True
    )
    customer_name = fields.CharField(
        verbose_name="customer_name", mongo_name="customer_name", required=True
    )
    customer_contact_number = fields.BigIntegerField(
        verbose_name="customer_contact_number",
        mongo_name="customer_contact_number",
        required=True,
    )
    quantity = fields.IntegerField(
        verbose_name="quantity", mongo_name="quantity", required=True
    )
    transaction_date_time = fields.DateTimeField(
        verbose_name="transaction_date_time",
        mongo_name="transaction_date_time",
        default=datetime.datetime.now(),
    )
    prescription_url = fields.URLField(
        verbose_name="prescription_url", mongo_name="prescription_url"
    )

    class Meta:
        final = True


class Company(EmbeddedMongoModel):
    """
    1) Model contains details about companies (manufacturers of the mdecines)
    2) Embedded inside Shopkeeper Model
    """

    company_name = fields.CharField(
        verbose_name="company_name", mongo_name="_id", primary_key=True, required=True
    )
    company_mr_name = fields.CharField(
        verbose_name="company_mr_name", mongo_name="company_mr_name", required=True
    )
    last_mr_visit = fields.DateTimeField(
        verbose_name="last_mr_visit",
        mongo_name="last_mr_visit",
        default=datetime.datetime.now(),
    )

    class Meta:
        final = True


class Medicine(EmbeddedMongoModel):
    """
    1) Medicine model to contain details about a particular medcine
    2) Embedded inside Shopkeeper Model
    """

    medicine_id = fields.ObjectIdField(
        verbose_name="medicine_id",
        mongo_name="_id",
        primary_key=True,
        default=ObjectId(),
    )
    medicine_name = fields.CharField(
        verbose_name="medicine_name", mongo_name="medicine_name", required=True
    )
    manufacturer_name = fields.CharField(
        verbose_name="manufacturer_name", mongo_name="manufacturer_name", required=True
    )
    expiry_date = fields.DateTimeField(
        verbose_name="expiry_date", mongo_name="expiry_date", required=True
    )
    dose_in_mg = fields.IntegerField(
        verbose_name="dose_in_mg", mongo_name="dose_in_mg", required=True
    )
    medicine_cost_price = fields.FloatField(
        verbose_name="medicine_cost_price",
        mongo_name="medicine_cost_price",
        required=True,
    )
    medicine_selling_price = fields.FloatField(
        verbose_name="medicine_selling_price",
        mongo_name="medicine_selling_price",
        required=True,
    )
    quantity_in_stock = fields.IntegerField(
        verbose_name="quantity_in_stock", mongo_name="quantity_in_stock", default=0
    )
    quantity_sold_since_last_mr_visit = fields.IntegerField(
        verbose_name="quantity_sold_since_last_mr_visit",
        mongo_name="quantity_sold_since_last_mr_visit",
        default=0,
    )
    medicine_description = fields.CharField(
        verbose_name="medicine_description",
        mongo_name="medicine_description",
        min_length=0,
        max_length=500,
    )
    transactions = fields.EmbeddedDocumentListField(Transaction)

    class Meta:
        final = True
        ignore_unknown_fields = True


class Shopkeeper(MongoModel):
    """
    1) Shopkeeper Model to store details of shop along with shopkeeper
    2) Main Mongo Model
    """

    shopkeeper_id = fields.ObjectIdField(
        verbose_name="shopkeeper_id",
        mongo_name="_id",
        primary_key=True,
        default=ObjectId(),
    )
    shopkeeper_name = fields.CharField(
        verbose_name="shopkeeper_name", mongo_name="shopkeeper_name", required=True
    )
    email = fields.EmailField(verbose_name="email", mongo_name="email", required=True)
    password = fields.CharField(
        verbose_name="password", mongo_name="password", required=True
    )
    shopkeeper_contact_number = fields.BigIntegerField(
        verbose_name="shopkeeper_contact_number",
        mongo_name="shopkeeper_contact_number",
        required=True,
    )
    shop_address = fields.CharField(
        verbose_name="shop_address", mongo_name="shop_address"
    )
    is_verfied = fields.BooleanField(
        verbose_name="is_verfied", mongo_name="is_verified", default=False
    )
    verification_token = fields.CharField(
        verbose_name="verification_token",
        mongo_name="verification_token",
        default=None,
        blank=True,
    )
    verification_token_expiry_time = fields.DateTimeField(
        verbose_name="verification_token_expiry_time",
        mongo_name="verification_token_expiry_time",
        default=datetime.datetime.now(),
        blank=True,
    )
    company_tie_ups = fields.EmbeddedDocumentListField(Company, blank=True)
    medicines = fields.EmbeddedDocumentListField(Medicine, blank=True)

    objects = Manager()

    def clean(self):
        valid_contact_info(self.shopkeeper_contact_number)
        valid_medicine_details(self.medicines)

    class Meta:
        final = True
        collection_name = "Shopkeepers"
