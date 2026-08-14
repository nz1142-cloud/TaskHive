from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .ai import generate_risk_assessment
from .forms import BidForm, RegisterForm, TaskForm
from .models import Bid, Task


def home(request):
    tasks = Task.objects.filter(
        status="Open"
    ).select_related("created_by")

    return render(
        request,
        "tasks/home.html",
        {
            "tasks": tasks,
        },
    )


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully.",
            )

            return redirect("home")

    else:
        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
        },
    )


@login_required
def create_task(request):

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            task.created_by = request.user

            task.save()

            # Generate AI risk assessment.
            task.risk_assessment = generate_risk_assessment(
                task.title,
                task.description,
            )

            task.save(
                update_fields=["risk_assessment"]
            )

            messages.success(
                request,
                "Your task has been posted successfully.",
            )

            return redirect(
                "task_detail",
                pk=task.pk,
            )

    else:
        form = TaskForm()

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
        },
    )


def task_detail(request, pk):

    task = get_object_or_404(
        Task.objects.select_related("created_by"),
        pk=pk,
    )

    bids = task.bids.select_related(
        "freelancer"
    ).all()

    already_bid = False

    if request.user.is_authenticated:
        already_bid = Bid.objects.filter(
            task=task,
            freelancer=request.user,
        ).exists()

    return render(
        request,
        "tasks/task_detail.html",
        {
            "task": task,
            "bids": bids,
            "already_bid": already_bid,
        },
    )


@login_required
def place_bid(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
    )

    if task.status != "Open":
        messages.error(
            request,
            "This task is no longer open for bidding.",
        )

        return redirect(
            "task_detail",
            pk=task.pk,
        )

    if task.created_by == request.user:
        messages.error(
            request,
            "You cannot bid on your own task.",
        )

        return redirect(
            "task_detail",
            pk=task.pk,
        )

    if Bid.objects.filter(
        task=task,
        freelancer=request.user,
    ).exists():

        messages.warning(
            request,
            "You have already placed a bid on this task.",
        )

        return redirect(
            "task_detail",
            pk=task.pk,
        )

    if request.method == "POST":

        form = BidForm(request.POST)

        if form.is_valid():

            bid = form.save(commit=False)

            bid.task = task

            bid.freelancer = request.user

            bid.save()

            messages.success(
                request,
                "Your bid has been submitted.",
            )

            return redirect(
                "task_detail",
                pk=task.pk,
            )

    else:
        form = BidForm()

    return render(
        request,
        "tasks/task_detail.html",
        {
            "task": task,
            "bids": task.bids.select_related(
                "freelancer"
            ),
            "bid_form": form,
            "show_bid_form": True,
            "already_bid": False,
        },
    )


@login_required
def task_bids(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
    )

    if task.created_by != request.user:
        messages.error(
            request,
            "You are not allowed to view these bids.",
        )

        return redirect(
            "task_detail",
            pk=task.pk,
        )

    bids = task.bids.select_related(
        "freelancer"
    ).all()

    return render(
        request,
        "tasks/bids.html",
        {
            "task": task,
            "bids": bids,
        },
    )


@login_required
@transaction.atomic
def choose_winner(request, task_pk, bid_pk):

    task = get_object_or_404(
        Task,
        pk=task_pk,
    )

    bid = get_object_or_404(
        Bid,
        pk=bid_pk,
        task=task,
    )

    if task.created_by != request.user:
        messages.error(
            request,
            "You are not allowed to choose a winner.",
        )

        return redirect(
            "task_detail",
            pk=task.pk,
        )

    if task.status != "Open":
        messages.error(
            request,
            "This task is already assigned or completed.",
        )

        return redirect(
            "task_bids",
            pk=task.pk,
        )

    task.status = "Assigned"

    task.save(
        update_fields=["status"]
    )

    messages.success(
        request,
        f"{bid.freelancer.username} has been selected as the winner.",
    )

    return redirect(
        "task_bids",
        pk=task.pk,
    )


@login_required
def complete_task(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
    )

    if task.created_by != request.user:
        messages.error(
            request,
            "You are not allowed to complete this task.",
        )

        return redirect(
            "task_detail",
            pk=task.pk,
        )

    if task.status != "Assigned":
        messages.error(
            request,
            "Only assigned tasks can be completed.",
        )

        return redirect(
            "task_detail",
            pk=task.pk,
        )

    task.status = "Completed"

    task.save(
        update_fields=["status"]
    )

    messages.success(
        request,
        "Task marked as completed.",
    )

    return redirect(
        "task_detail",
        pk=task.pk,
    )
