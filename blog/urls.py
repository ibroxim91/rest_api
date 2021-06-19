
from django.urls import path
from .views import *
from .xlsx import *

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'posts', PostViewSet,basename="posts")
router.register(r'ecxel', MyExcelViewSet,basename="ecxel")


app_name = "blog"

posts_list = PostViewSet.as_view({
    'get': 'list',
})
post_detail = PostViewSet.as_view({
    'get': 'retrieve',
})
post_create = PostViewSet.as_view({
    'post':'create'
})
post_delete = PostViewSet.as_view({
    'delete':'delete'
})
post_update = PostViewSet.as_view({
    'put':'update'
})

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )
urlpatterns = [
   
    path('inventory',InventoryApiView.as_view(),name='inventory' ),
    path('list',PostListView.as_view(),name='posts_2' ),
    path('detail/<int:pk>',PostDetailView.as_view(),name='detail' ),
    path('create',PostCreateView.as_view(),name='create' ),
    path('export',export_posts_xls,name='export_posts_xls' ),

    path('',posts_list,name='posts_list' ),
    path('users',UsersApiView.as_view() ,name='users_list' ),
    path('<int:pk>',post_detail,name='post_detail' ),
    path('create/post',post_create,name='post_create' ),
    path('delete/<int:pk>',post_delete,name='post_delete' ),
    path('update/<int:pk>',post_update,name='post_update' ),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('pdf/',generate_pdf,name='pdf' ),
]

urlpatterns += router.urls