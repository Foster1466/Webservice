from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
import math
from datetime import time

# Create your views here.

@api_view(['POST'])
def processReceipt(request):
    try:
        # Deserialize the JSON data from the request body
        serializer = ReceiptSerializer(data=request.data)
        if serializer.is_valid():
            # Calculate the points based on the given rules
            receipt = serializer.save()
            points = 0
            retailer_name = receipt.retailer
            purchase_date = receipt.purchaseDate  
            purchase_time = receipt.purchaseTime
            total = float(receipt.total)
            item_count = len(receipt.items)

            # Rule 1 one point for every alphanumeric char
            points+= sum(1 for char in retailer_name if char.isalnum())

            # Rule 2 50 point if total is round dollar amount with no cents
            if total==round(total):
                points+=50
            
            # Rule 3 25 points if the total is a multiple of 0.25.
            if total%0.25==0:
                points+=25
            
            # Rule 4 5 points for every two items on the receipt
            points+= (item_count//2)*5

            # Rule 5 If the trimmed length of the item description is a multiple of 3, 
            # multiply the price by 0.2 and round up to the nearest integer. 
            # The result is the number of points earned.
            for item in receipt.items:
                description = item['shortDescription'].strip()
                price = float(item['price'])
                if len(description)%3==0:
                    points+= math.ceil(price*0.2)
            
            # Rule 6 6 points if the day in the purchase date is odd.
            if purchase_date.day%2!=0:
                points+=6
            
            # Rule 7 10 points if the time of purchase is after 2:00pm and before 4:00pm
            if time(14,0) <= purchase_time <= time(16,0):
                points+=10
            
            # Update the receipt with the calculated points
            receipt.points = points
            receipt.save()

            # Return the response with the generated receipt ID
            response_data = {'id': str(receipt.id)}
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    except:
        return Response({'error':'The receipt is invalid'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getPoints(request, pk):
    try:
        # Get the receipt by its id, prepare the response data and return points
        receipt = Receipt.objects.get(pk = pk)          
        response_data = {'points': receipt.points}
        return Response(response_data, status=status.HTTP_200_OK)
    except:
        return Response({'error':'No receipt found for that id'}, status=status.HTTP_404_NOT_FOUND)