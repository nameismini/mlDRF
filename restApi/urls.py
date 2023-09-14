from rest_framework import routers
from django.urls import path, include
from .views import log_list_fbv, log_detail_fbv, LogListCbv, LogDetailCbv

router = routers.SimpleRouter()
# router.register('books', BookViewSet)

urlpatterns = [
    path('fbv/', log_list_fbv),
    path("fbv/<int:pk>", log_detail_fbv),
    path('cbv/', LogListCbv.as_view()),
    path("cbv/<int:pk>", LogDetailCbv.as_view()),
]

urlpatterns += router.urls