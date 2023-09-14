from django.urls import path
from .views import RegisterView, LoginView, ProfileView

urlpatterns = [
    #사용자등록
    path('register/', RegisterView.as_view()),
    #로그인
    path('login/', LoginView.as_view()),
    #프로파일조회 - user 확장모델
    path('profile/<int:pk>/', ProfileView.as_view()),
    # path('profile/', ProfileView.as_view())
]
