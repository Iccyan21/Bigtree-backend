from . import views
from django.urls import path, include

urlpatterns = [
    path('login', views.LoginView.as_view()),  # ログイン処理
    path('register', views.RegisterView.as_view()),  # 新規登録処理
    path('confirm', views.ConfirmView.as_view()),  # アカウント承認処理
    path('data', views.DataView.as_view()),  # ユーザー情報取得処理
    # path('follow', views.UserFollowingViewSet.as_view()),  # ユーザーフォロー機能
    # path('unfollow/<int:pk>', views.UserUnFollowViewSet.as_view()),  # フォロー解除機能

]