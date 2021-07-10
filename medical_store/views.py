from bson.objectid import ObjectId
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

ENCRIPTION_KEY = os.environ.get("ENCRIPTION_KEY")


@api_view(["POST"])
def signup(request):
    shopkeeper_name = request.data.get("shopkeeper_name")
    email = request.data.get("email")
    password = request.data.get("password")
    confirmPassword = request.data.get("confirmPassword")
    shopkeeper_contact_number = request.data.get("shopkeeper_contact_number")
    shop_address = request.data.get("shop_address")
    is_verfied = False
    company_tie_ups = []
    medicines = []
    verification_token_expiry_time = datetime.datetime.now() + datetime.timedelta(
        hours=1
    )
    verification_token = uuid.uuid4()

    profile = Shopkeeper.objects.get(
        {
            "email": email,
        }
    )
    if profile:
        return Response({"message": "Email ID Already Exists"}, 400)

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
    return Response({"message": "Success"}, 200)


@api_view(["GET"])
def verify(request, shopkeeper_id, token):
    print(shopkeeper_id)
    try:
        profile = Shopkeeper.objects.get(
            {
                "_id": ObjectId(shopkeeper_id),
            }
        )
        if profile.verification_token != token:
            return Response(data={"message": "Invalid Verification Token"}, status=400)

        if profile.verification_token_expiry_time < datetime.datetime.now():
            return Response(
                data={
                    "message": "Verfication Code Expired",
                },
                status=400,
            )

        profile.is_verfied = True
        profile.verification_token_expiry_time = None
        profile.verification_token = None
        profile.save()

    except Shopkeeper.DoesNotExist:
        return Response({"message": "Invalid User Id"}, 400)

    return Response({"message": "Email Verfied"}, 200)


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        profile = Shopkeeper.objects.get(
            {
                "email": email,
            }
        )
        decoded_password = cryptocode.decrypt(profile.password, ENCRIPTION_KEY)
        if decoded_password != password:
            return Response({"message": "Invalid Password,Shopkeeper Not Found"}, 404)
        encoded_jwt = jwt.encode(
            {"shopkeeper_id": str(profile.shopkeeper_id)},
            ENCRIPTION_KEY,
            algorithm="HS256",
        )
        return Response(
            {"Authorization": "Bearer " + encoded_jwt, "message": "Login Sucessfull"},
            200,
        )
    except Shopkeeper.DoesNotExist:
        return Response({"message": "Invalid Credentials,Shopkeeper Not Found"}, 404)
