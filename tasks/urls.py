from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    UserLoginView,
    choose_winner,
    complete_task,
    create_task,
    home,
    place_bid,
    register,
    task_bids,
    task_detail,
)


urlpatterns = [
    path(
        "",
        home,
        name="home",
    ),

    path(
        "login/",
        UserLoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    path(
        "register/",
        register,
        name="register",
    ),

    path(
        "tasks/new/",
        create_task,
        name="create_task",
    ),

    path(
        "tasks/<int:pk>/",
        task_detail,
        name="task_detail",
    ),

    path(
        "tasks/<int:pk>/bid/",
        place_bid,
        name="place_bid",
    ),

    path(
        "tasks/<int:pk>/bids/",
        task_bids,
        name="task_bids",
    ),

    path(
        "tasks/<int:task_pk>/bids/<int:bid_pk>/winner/",
        choose_winner,
        name="choose_winner",
    ),

    path(
        "tasks/<int:pk>/complete/",
        complete_task,
        name="complete_task",
    ),
]
