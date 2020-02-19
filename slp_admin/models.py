from django.db import models
from djongo.models import EmbeddedModelField, ArrayModelField
from django.core.validators import RegexValidator


class Address(models.Model):
    """Embedded model to store address of user"""
    add_line1 = models.CharField(max_length=255, blank=False, null=False)
    add_line2 = models.CharField(max_length=255, blank=False, null=False)
    city = models.CharField(max_length=255, blank=False, null=False)
    state = models.CharField(max_length=255, blank=False, null=False)
    country = models.CharField(max_length=255, blank=False, null=False)
    zip_code = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class Contractor(models.Model):
    """Model to store contractors details"""
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=10, blank=False, null=False, validators=[RegexValidator(r'^\d{0,10}$')],
                               unique=True)
    profile_photo = models.ImageField(upload_to='images/contractor/')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class ReferredUser(models.Model):
    """Referred User model to store its users details."""
    user_id = models.ForeignKey('SlpUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class SlpUser(models.Model):
    """User model to save user details"""
    choices = (
        ('Block', 'Block'),
        ('Unblock', 'Unblock')
    )
    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    password = models.CharField(max_length=20, blank=False, null=False)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    phone = models.CharField(max_length=10, blank=False, null=False)
    address = EmbeddedModelField(model_container=Address)
    company = models.CharField(max_length=255, blank=False, null=False)
    is_deleted = models.BooleanField(default=False)
    refer_code = models.CharField(max_length=255, unique=True, blank=False, null=False)
    referred_by = models.CharField(max_length=255, blank=False, null=False)
    referred_to = ArrayModelField(model_container=ReferredUser)
    status = models.CharField(max_length=20, choices=choices, default="Unblock")
    points = models.IntegerField(blank=False, null=False, default=0)
    profile_photo = models.ImageField(upload_to='images/users')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class SlpAdmin(models.Model):
    """Admin model to save slp_admin details"""
    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    phone = models.CharField(max_length=10, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class Merchant(models.Model):
    """Merchant model for create merchant"""
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, blank=False, null=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    statuses = (
        ('Block', 'Block'),
        ('Unblock', 'Unblock'),
    )
    status = models.CharField(max_length=50, choices=statuses, default='Unblock')
    address = EmbeddedModelField(model_container=Address)
    company = models.CharField(max_length=255, blank=False, null=False)


class Contest(models.Model):
    """represents contest table in database"""
    choices = (
        ('Upcoming', 'Upcoming'),
        ('Running', 'Running'),
        ('Completed', 'Completed')
    )

    name = models.CharField(max_length=255)
    details = models.TextField()
    points = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/contests/')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=choices)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """provides string representation of contest model"""
        return self.name


class Banner(models.Model):
    """represents banner table in database"""
    choices = (
        ('ON', 'ON'),
        ('OFF', 'OFF')
    )

    company_name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    image = models.ImageField(upload_to='images/banners/')
    status = models.CharField(max_length=10, choices=choices)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """provides string representation of contest model"""
        return self.company_name


class Product(models.Model):
    pass


class Batch(models.Model):
    """Model for create Batch"""
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    start_date = models.DateField()
    start_time = models.TimeField()


class QRCode(models.Model):
    """QR code create and list model"""
    choices = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    )
    merchant = models.ForeignKey('Merchant', on_delete=models.CASCADE)
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=choices, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class Dispute(models.Model):
    """Raise dispute by user, model"""
    choices = (
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved')
    )
    user = models.ForeignKey('SlpUser', on_delete=models.CASCADE)
    QR_code = models.ForeignKey('QRCode', on_delete=models.CASCADE)
    message = models.TextField(null=False, blank=False)
    action = models.CharField(max_length=255, choices=choices, default='Pending')
    dispute_raised_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class Reward(models.Model):
    """Rewards model to store rewards and its points"""
    QR_code = models.ForeignKey("QRCode", on_delete=models.CASCADE)
    user = models.ForeignKey('SlpUser', on_delete=models.CASCADE)
    points = models.IntegerField()


class Job(models.Model):
    """Model to create jobs"""
    choices = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    )
    job_name = models.CharField(max_length=255, blank=False, null=False)
    job_status = models.CharField(max_length=10, choices=choices, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    """Task model to store task details"""
    choices = (
        ('Todo', 'Todo'),
        ('Running', 'Running'),
        ('Completed', 'Completed')
    )
    title = models.CharField(max_length=255, blank=False, null=False)
    user = models.ForeignKey('SlpUser', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    description = models.TextField(blank=False, null=True)
    status = models.CharField(max_length=50, default='Todo', choices=choices)
    attachments = models.FileField(upload_to='tasks/')
    additional_points = models.IntegerField(null=True, blank=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


def validate_file_extension(value):
    """"Validator function for video extension"""
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mkv', '.mov', '.avi', '.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class Category(models.Model):
    """"Represents Category in Table"""
    name = models.CharField(max_length=255, unique=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name


class Video(models.Model):
    """"Represents Video details in Table"""

    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    video = models.FileField(upload_to="videos/", validators=[validate_file_extension])
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    """"Represents Quiz details in Table"""

    name = models.CharField(max_length=255, unique=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    points = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    """"Represents Question details in Table"""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.question
