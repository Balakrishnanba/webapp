from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random
import string
import secrets
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=64, unique=True, blank=True, null=True)

    def generate_secret_key(self):
        self.secret_key = secrets.token_hex(8)  # Generate a 64-character secret key
        self.save()

# Automatically generate a secret key when a new user profile is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)
        profile.generate_secret_key()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    other_field = models.CharField(max_length=255)

# Image Upload Model
class ImageUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Registered user who uploads the image
    sender_email = models.EmailField(max_length=255, blank=True)  # Store the sender's email
    image = models.ImageField(upload_to='images/')  # Uploaded image file
    image_name = models.CharField(max_length=100, default="Unnamed")  # Name of the image
    subject = models.CharField(max_length=255, default="No Subject")  # Subject of the image
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp
    qr_password = models.CharField(max_length=255, blank=True)  # QR code password

    def __str__(self):
        return f"{self.image_name} - {self.user.username} - {self.sender_email}"

    def generate_password(self):
        """Generate a random alphanumeric password of length 8."""
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        self.qr_password = password
        self.save()
        return password



from django.contrib.auth.models import User
from django.db import models

class SentEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_email = models.EmailField()
    secret_key = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/')
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Email to {self.recipient_email} from {self.user}"



from django.db import models

class ReplyImage(models.Model):
    image = models.ImageField(upload_to='replies/')
    secret_key = models.CharField(max_length=100)

    def __str__(self):
        return self.secret_key





