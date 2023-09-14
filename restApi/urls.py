from rest_framework import routers
from django.urls import path, include
from .views import log_list_fbv, log_dtl_fbv, LogListCbv, LogDtlCbv, LogListMix, LogDtlMix, LogListGen, LogDtlGen, \
    LogViewSet, LogModelViewSet, LogReadViewSet

router = routers.SimpleRouter()
# router = routers.DefaultRouter()


# log_list = LogViewSet.as_view({
#     'get':'list',
#     'post':'create'
# })

# router.register(r'log', LogViewSet)
router.register(r'logModelview', LogModelViewSet)
router.register(r'logReadview', LogReadViewSet)

urlpatterns = [
    path('fbv/', log_list_fbv),
    path("fbv/<int:pk>", log_dtl_fbv),
    path('cbv/', LogListCbv.as_view()),
    path("cbv/<int:pk>", LogDtlCbv.as_view()),
    path("mixin/", LogListMix.as_view()),
    path("mixin/<int:pk>", LogDtlMix.as_view()),
    path("generics/", LogListGen.as_view()),
    path("generics/<int:pk>", LogDtlGen.as_view()),
    # path('', include(router.urls))
]

urlpatterns += router.urls
