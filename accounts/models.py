from django.db import models


# =================================================
# USER
# =================================================

class User(models.Model):

    full_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    mobile = models.CharField(max_length=15)

    password = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


# =================================================
# LOST ITEM
# =================================================

class LostItem(models.Model):

    STATUS_CHOICES = [
        ("lost", "Lost"),
        ("possible_match", "Possible Match"),
        ("recovered", "Recovered"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    item_name = models.CharField(max_length=100)

    category = models.CharField(max_length=50)

    location = models.CharField(max_length=100)

    lost_date = models.DateField()

    description = models.TextField()

    image = models.ImageField(
        upload_to="lost_items/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="lost"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.item_name


# =================================================
# FOUND ITEM
# =================================================

class FoundItem(models.Model):

    STATUS_CHOICES = [
        ("found", "Found"),
        ("returned", "Returned"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    item_name = models.CharField(max_length=100)

    category = models.CharField(max_length=50)

    location = models.CharField(max_length=100)

    found_date = models.DateField()

    description = models.TextField()

    image = models.ImageField(
        upload_to="found_items/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="found"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.item_name


# =================================================
# NOTIFICATION
# =================================================

class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.message


# =================================================
# LIKE
# =================================================

class Like(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    lost_item = models.ForeignKey(
        LostItem,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    found_item = models.ForeignKey(
        FoundItem,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.full_name} liked a post"


# =================================================
# COMMENT
# =================================================

class Comment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    lost_item = models.ForeignKey(
        LostItem,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    found_item = models.ForeignKey(
        FoundItem,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.full_name} commented"


# =================================================
# CONNECTION
# =================================================

class Connection(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_connections"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_connections"
    )

    status = models.CharField(
        max_length=20,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender.full_name} -> {self.receiver.full_name}"


# =================================================
# ANNOUNCEMENT
# =================================================

class Announcement(models.Model):

    title = models.CharField(max_length=200)

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.title


# =================================================
# REPORT USER
# =================================================

class ReportUser(models.Model):

    REASON_CHOICES = [
        ("fake_information", "Fake Information"),
        ("fraud", "Fraud or Scam"),
        ("harassment", "Harassment"),
        ("inappropriate_behavior", "Inappropriate Behavior"),
        ("suspicious_activity", "Suspicious Activity"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("reviewed", "Reviewed"),
        ("resolved", "Resolved"),
    ]

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reports_made"
    )

    reported_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reports_received"
    )

    reason = models.CharField(
        max_length=50,
        choices=REASON_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.reporter.full_name} reported "
            f"{self.reported_user.full_name}"
        )

