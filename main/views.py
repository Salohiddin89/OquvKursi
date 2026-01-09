import requests
import random
import string
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import (
    Course,
    Content,
    UserCourse,
    Category,
    Teacher,
    Event,
    Comment,
    ContactMessage,
    CoursePurchase,
)

User = get_user_model()


# ✅ HOME
def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    categories = Category.objects.all()
    teachers = Teacher.objects.all()
    events = Event.objects.all()
    courses = Course.objects.all()

    return render(
        request,
        "index.html",
        {
            "courses": courses,
            "categories": categories,
            "teachers": teachers,
            "events": events,
        },
    )


# ✅ TELEGRAM CONNECT
@login_required
def connect_telegram(request):
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    request.user.telegram_code = code
    request.user.save()
    return render(request, "connect_telegram.html", {"code": code})


# ✅ BUY COURSE CONFIRM PAGE
@login_required
def buy_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, "confirm_purchase.html", {"course": course})


# ✅ PAYMENT PAGE
@login_required
def payment_page(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        receipt = request.FILES.get("receipt")

        CoursePurchase.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            receipt=receipt,
        )

        return redirect("payment_success")

    return render(request, "payment_page.html", {"course": course})


# ✅ PAYMENT SUCCESS
def payment_success(request):
    return render(request, "courses/payment_success.html")


# ✅ LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Login yoki parol noto‘g‘ri!")

    return render(request, "auth/login.html")


# ✅ REGISTER
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if password != confirm:
            messages.error(request, "Parollar mos emas!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu username band!")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        login(request, user)
        return redirect("home")

    return render(request, "auth/register.html")


# ✅ LOGOUT
def logout_view(request):
    logout(request)
    return redirect("login")


# ✅ COURSE LESSONS
@login_required
def course_lessons(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    has_access = UserCourse.objects.filter(user=request.user, course=course).exists()

    if not has_access:
        return redirect("buy_course", course_id=course.id)

    lessons = course.lessons.all()
    return render(request, "lessons.html", {"course": course, "lessons": lessons})


# ✅ COURSE LIST
@login_required
def course_list(request, category_id=None):
    if category_id:
        courses = Course.objects.filter(category_id=category_id)
    else:
        courses = Course.objects.all()

    categories = Category.objects.all()

    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses,
            "categories": categories,
            "selected_category": category_id,
        },
    )


# ✅ LESSON DETAIL + COMMENTS
@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Content, id=lesson_id)

    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            Comment.objects.create(user=request.user, content=lesson, text=text)
            return redirect("lesson_detail", lesson_id=lesson.id)

    comments = lesson.comments.all().order_by("-created_at")

    return render(
        request,
        "courses/lesson_detail.html",
        {"lesson": lesson, "comments": comments},
    )


# ✅ CONTACT MESSAGE
@csrf_exempt
@login_required
def contact_view(request):
    if request.method == "POST":
        msg = request.POST.get("message")
        ContactMessage.objects.create(user=request.user, message=msg)
        return redirect("home")

    return render(request, "contact.html")


# ✅ SUBSCRIBE COURSE
@login_required
def subscribe_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    UserCourse.objects.get_or_create(user=request.user, course=course)
    return redirect("course_detail", course_id=course.id)


# ✅ COURSE DETAIL
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_subscribed = UserCourse.objects.filter(user=request.user, course=course).exists()

    lessons = course.lessons.all() if is_subscribed else []

    return render(
        request,
        "courses/course_detail.html",
        {"course": course, "is_subscribed": is_subscribed, "lessons": lessons},
    )


# ✅ PROFILE PAGE (3 TAB)
@login_required
def profile_view(request):
    user = request.user
    tab = request.GET.get("tab", "courses")

    purchases = CoursePurchase.objects.filter(
        user=user, is_confirmed=True
    ).select_related("course")

    messages_list = ContactMessage.objects.filter(user=user).order_by("-created_at")

    success = None

    if request.method == "POST" and tab == "settings":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")

        avatar = request.FILES.get("avatar")
        if avatar:
            user.avatar = avatar

        user.save()
        success = "Profil muvaffaqiyatli yangilandi!"

    return render(
        request,
        "profile.html",
        {
            "user_obj": user,
            "tab": tab,
            "purchases": purchases,
            "messages": messages_list,
            "success": success,
        },
    )


@login_required
def admin_dashboard(request):
    context = {
        "courses_count": Course.objects.count(),
        "users_count": User.objects.count(),
        "messages_count": ContactMessage.objects.count(),
        "purchases_count": CoursePurchase.objects.count(),
    }
    return render(request, "admin_dashboard.html", context)
