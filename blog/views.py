from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView,CreateAPIView, ListAPIView,UpdateAPIView,RetrieveAPIView,RetrieveUpdateDestroyAPIView
from .serializers import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from rest_framework import serializers, viewsets
from rest_framework import status,permissions
import xlwt
from django.http import HttpResponse
from rest_framework.authtoken.models import Token

class InventoryApiView(APIView):

    def get(self, request):
        posts = Inventory.objects.all()
        serializer = InventorySerializer(posts,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):

        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request,username=username,password=password)
        data = {}
        if user is not None:
            login(request,user)
            token = Token.objects.get_or_create(user=user)
            data['status'] = "success"
            data['token'] = token.key
        else:
            data['status'] = "error"
        return  Response(data)


class PostListView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()


 
class PostDetailApiView(RetrieveAPIView):
    serializer_class = PostSerializer
    # queryset = Post.objects.all()
    # lookup_field = "pk"
    def get_object(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return post

class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #permission_classes = (permissions.IsAdminUser,)


class DeletePostView(DestroyAPIView):
    serializer_class = PostSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.filter(id=self.kwargs['pk'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status':"Object successfully deleted"})


class UpdatePostView(UpdateAPIView):
    serializer_class = PostSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.filter(id=self.kwargs['pk'])
        return queryset

    def perform_update(self, serializer):
        instance = self.get_object()
        modified_instance = serializer.save()


class PostDetailView(RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'pk'
    serializer_class = PostSerializer
    queryset = Post.objects.all()


# all presented in the same class
class PostViewSet(viewsets.ViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_object(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return post

    def delete(self, request, pk=None):
        instance = self.get_object()    
        instance.delete()
        return Response({'status':200})

    def create(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Post.objects.create(**serializer.validated_data)    
            return Response(
                serializer.validated_data, status=status.HTTP_201_CREATED
                )

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request,pk):
        instance = self.get_object()
        serializer =  self.serializer_class(instance, data=request.data, partial=False)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:    
            return Response({'status':200})

    def list(self,request):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts,many=True)
        return Response(serializer.data)



# export data to excel for django


def export_posts_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['title', 'slug', 'body' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Post.objects.all().values_list('title', 'slug', 'body')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response