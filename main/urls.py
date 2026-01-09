from django.urls import path
from .views import (
    home,
    login_view,
    register_view,
    logout_view,
    course_list,
    course_detail,
    lesson_detail,
    contact_view,
    subscribe_course,
    buy_course, 
    payment_page, 
    payment_success, 
    profile_view, 
    admin_dashboard, 
)

urlpatterns = [
    # Home
    path("", home, name="home"),
    # Auth
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    # Courses
    path("courses/", course_list, name="course_list"),
    path("courses/<int:course_id>/", course_detail, name="course_detail"),
    # Category filtering — birinchi turishi SHART
    path("category/<int:category_id>/", home, name="home_by_category"),
    path("contact/", contact_view, name="contact"),
    # Lesson
    path("lesson/<int:lesson_id>/", lesson_detail, name="lesson_detail"),
    path(
        "courses/<int:course_id>/subscribe/", subscribe_course, name="subscribe_course"
    ),
    # ✅ Sotib olish oqimi
    path("buy-course/<int:course_id>/", buy_course, name="buy_course"),
    path("payment/<int:course_id>/", payment_page, name="payment_page"),
    path("payment-success/", payment_success, name="payment_success"),
    # ✅ Foydalanuvchi profili
    path("profile/", profile_view, name="profile"),
    path("admin-panel/", admin_dashboard, name="admin_dashboard"),
]
