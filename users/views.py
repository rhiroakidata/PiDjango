from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers as srl
from django.forms.models import model_to_dict

from .models import User
from .serializers import *

import bcrypt, json

@api_view(['GET', 'POST'])
def users_list(request):
    """
 List  customers, or create a new customer.
 """
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        users = User.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(users, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = UserSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({
            'data': serializer.data , 
            'count': paginator.count, 
            'numpages' : paginator.num_pages, 
            'nextlink': '/api/users/?page=' + str(nextPage), 
            'prevlink': '/api/users/?page=' + str(previousPage)
        })

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = bcrypt.hashpw(request.data['password'].encode('utf-8'), bcrypt.gensalt(14))
            serializer.save(password=password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def users_detail(request, pk):
    """
    Retrieve, update or delete a customer by id/pk.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['POST'])
def login(request):
    print('Entrei')
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']
 
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            password = password.encode('utf-8')
            hashed = user.password

            if bcrypt.checkpw(password, hashed):
                # {'user': user, 'token': token}
                token = Token.objects.create(user=user)

                data = {'token': str(token), 'user': model_to_dict(user)}
 
                data['user']['date_joined'] = data['user']['date_joined'].strftime('%Y-%m-%d %H:%M:%S')
                data['user']['picture'] = data['user']['picture'].url if data['user']['picture'] else ''

                return Response(json.dumps(data), status=status.HTTP_200_OK, content_type="application/json")

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        else: 
            return Response(status=status.HTTP_404_NOT_FOUND)