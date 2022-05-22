from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from users.models import *
from users.serializers import *
from post.models import *

# Create your views here.
