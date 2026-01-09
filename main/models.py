from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager


# ✅ CUSTOM USER
class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    telegram_code = models.CharField(max_length=10, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return self.username


# ✅ CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ✅ COURSE
class Course(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="courses"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="courses/")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ✅ CONTENT (LESSONS)
class Content(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to="contents/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


def get_embed_url(self):
    url = self.video_url

    if not url:
        return None

    # ✅ Agar allaqachon embed bo‘lsa
    if "youtube.com/embed/" in url:
        return url

    # ✅ fallback
    return url


# ✅ COURSE PURCHASE
class CoursePurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.IntegerField()
    receipt = models.ImageField(upload_to="receipts/", null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.course.title}"


# ✅ USER COURSE (SUBSCRIPTIONS)
class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.username} -> {self.course.title}"


# ✅ COMMENT
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"


# ✅ LIKE
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "content")

    def __str__(self):
        return f"{self.user.username} liked {self.content.title}"


# ✅ TEACHER
class Teacher(models.Model):
    full_name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    image = models.ImageField(upload_to="teachers/")

    def __str__(self):
        return self.full_name


# ✅ EVENT
class Event(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    short_description = models.TextField()
    image = models.ImageField(upload_to="events/")
    date = models.DateField()
    duration_hours = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.title} ({self.date})"


# ✅ CONTACT MESSAGE
class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    reply = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"


# ✅ TELEGRAM
class UserTelegram(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.chat_id}"
    