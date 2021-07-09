from medical_store.models.medical_stores import Shopkeeper
from django.shortcuts import (
    render,
)
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
import datetime
import uuid
import cryptocode
import jwt

ENCRIPTION_KEY = os.environ.get("SECRET_KEY")


@api_view(["POST"])
def signup(request):
    shopkeeper_name = request.body.get("shopkeeper_name")
    email = request.body.get("email")
    password = request.body.get("password")
    confirmPassword = request.body.get("confirmPassword")
    shopkeeper_contact_number = request.body.get("shopkeeper_contact_number")
    shop_address = request.body.get("shop_address")
    is_verfied = False
    company_tie_ups = []
    medicines = []
    verification_token_expiry_time = datetime.datetime.now() + datetime.timedelta(
        hours=1
    )
    verification_token = uuid.uuid4()
    if password != confirmPassword:
        return Response(
            data={"message": "Password and Confirm Password Does Not match"}, status=401
        )

    encoded_password = cryptocode.encrypt(password, ENCRIPTION_KEY)

    shopkeeper = Shopkeeper(
        shopkeeper_name=shopkeeper_name,
        email=email,
        password=encoded_password,
        shopkeeper_contact_number=shopkeeper_contact_number,
        shop_address=shop_address,
        is_verfied=is_verfied,
        verification_token=verification_token,
        verification_token_expiry_time=verification_token_expiry_time,
        company_tie_ups=company_tie_ups,
        medicines=medicines,
    )
    shopkeeper.save()
    # SEND EMAIL TO USER EMAIL_ID


# @api_view(["GET"])
# def verify(request, shopkeeper_id, token):

#     try:
#         profile = Shopkeeper.objects.get(
#             {
#                 "$and": {
#                     "shopkeeper_id": shopkeeper_id,
#                     "token": token,
#                     "verification_token_expiry_time": {"$gt": datetime.datetime.now()},
#                 }
#             }
#         )
#         profile.is_verfied = True
#         profile.verification_token_expiry_time = None
#         profile.verification_token = None
#         profile.save()
#     except Shopkeeper.DoesNotExist:
#         return Response({"message": "Time Invalid"}, 403)


# @api_view("POST")
# def login(request):
#     email = request.body.get("email")
#     password = request.body.get("password")

#     try:
#         profile = Shopkeeper.objects.get(
#             {
#                 "email": email,
#             }
#         )
#         decoded_password = cryptocode.decrypt(profile.password, ENCRIPTION_KEY)
#         if decoded_password != password:
#             return Response({"message": "Invalid Password,Shopkeeper Not Found"}, 404)
#         encoded_jwt = jwt.encode(
#             {"shopkeeper_id": profile.shopkeeper_id}, ENCRIPTION_KEY, algorithm="HS256"
#         )
#         return Response({"Authorization": "Bearer " + encoded_jwt}, 200)
#     except Shopkeeper.DoesNotExist:
#         return Response({"message": "Invalid Credentials,Shopkeeper Not Found"}, 404)
