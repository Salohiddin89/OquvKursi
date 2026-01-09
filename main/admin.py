from django.utils import timezone
import requests
from django.contrib import admin
from .models import (
    Course,
    Content,
    UserCourse,
    Comment,
    Like,
    User,
    Category,
    Teacher,
    Event,
    ContactMessage,
    UserTelegram,
    CoursePurchase,
)


# -------------------------
#  USER
# -------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "phone_number",
        "age",
        "is_staff",
    )
    search_fields = ("username", "first_name", "last_name", "phone_number")
    list_filter = ("is_staff", "is_superuser")


# -------------------------
#  COURSE
# -------------------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "created_at")
    search_fields = ("title",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)


# -------------------------
#  CONTENT (LESSONS)
# -------------------------
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "created_at")
    list_filter = ("course", "created_at")
    search_fields = ("title", "course__title")
    ordering = ("course", "order")


# -------------------------
#  USER COURSE (SUBSCRIPTIONS)
# -------------------------
@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "subscribed_at")
    list_filter = ("course", "subscribed_at")
    search_fields = ("user__username", "course__title")


# -------------------------
#  COMMENT
# -------------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "created_at")
    list_filter = ("created_at", "content__course")
    search_fields = ("user__username", "content__title", "text")


# -------------------------
#  LIKE
# -------------------------
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "created_at")
    search_fields = ("user__username", "content__title")
    list_filter = ("created_at",)


# -------------------------
#  CATEGORY
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# -------------------------
#  TEACHER
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("full_name", "specialty")
    search_fields = ("full_name", "specialty")


# -------------------------
#  EVENT
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "date", "duration_hours", "price")
    search_fields = ("title", "subject")
    list_filter = ("date",)


BOT_TOKEN = "8218372259:AAFXKY2LjAwHxEID4bhYZJMXcMA7peg9ehw"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "replied_at")
    readonly_fields = ("user", "message", "created_at")

    def save_model(self, request, obj, form, change):
        # ✅ reply maydoni o‘zgarganligini tekshiramiz
        reply_changed = "reply" in form.changed_data

        if reply_changed and obj.reply:
            obj.replied_at = timezone.now()

            try:
                tg = UserTelegram.objects.get(user=obj.user)
                chat_id = tg.chat_id

                text = (
                    f"✅ Admin javobi:\n"
                    f"📩 Sizning xabaringiz:\n{obj.message}\n\n"
                    f"💬 Admin javobi:\n{obj.reply}"
                )

                response = requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    data={"chat_id": chat_id, "text": text},
                )

                print("Telegram response:", response.text)

            except UserTelegram.DoesNotExist:
                print("❗ UserTelegram topilmadi — user botga /start yozmagan.")
            except Exception as e:
                print("❗ Telegramga yuborishda xato:", e)

        super().save_model(request, obj, form, change)


@admin.register(CoursePurchase)
class CoursePurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "amount", "is_confirmed", "created_at")
    readonly_fields = ("user", "course", "amount", "receipt", "created_at")

    def save_model(self, request, obj, form, change):
        if "is_confirmed" in form.changed_data and obj.is_confirmed:
            # ✅ Userga kursni ochib beramiz
            UserCourse.objects.create(user=obj.user, course=obj.course)

        super().save_model(request, obj, form, change)
# -------------------------
#  USER TELEGRAM
@admin.register(UserTelegram)
class UserTelegramAdmin(admin.ModelAdmin):
    list_display = ("user", "chat_id")
    search_fields = ("user__username", "chat_id")
# -------------------------
    list_display = ("user", "chat_id")
    search_fields = ("user__username", "chat_id")   
# -------------------------


@admin.register(UserTelegram)



































                                                                    