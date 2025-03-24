from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileForm
from .models import Profile
import random
import string
import qrcode
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import io
from io import BytesIO
import uuid
import secrets  # Import the secrets module
from .models import ImageUpload, SentEmail, ReplyImage
from .forms import RegisterForm, LoginForm, ImageUploadForm, SentEmailForm, PasswordForm
from .models import ImageUpload, SentEmail
from django.contrib.auth import get_user_model
from myapp.models import Profile
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import RegisterForm



def generate_qr(data):
    qr = qrcode.make(data)
    qr_io = io.BytesIO()
    qr.save(qr_io, format='PNG')
    qr_io.seek(0)
    return qr_io



User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a profile with a secret key
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('upload')  # Redirect to profile page after registration
    else:
        form = RegisterForm()
    
    return render(request, 'myapp/register.html', {'form': form})
# Login View





def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('upload')
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html', {'form': form})



def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


# Image Upload View
@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)
            uploaded_image.user = request.user
            uploaded_image.save()
            messages.success(request, 'Image uploaded successfully!')
            return redirect('send_email')
    else:
        form = ImageUploadForm()
    return render(request, 'myapp/upload.html', {'form': form})



# Send Image Email
@login_required
def send_image_email(request):
    usernames = User.objects.all()
    images = ImageUpload.objects.all()
    
    if request.method == 'POST':
        selected_username = request.POST.get('username')
        selected_image_id = request.POST.get('image_id')
        subject = request.POST.get('subject')

        selected_user = get_object_or_404(User, username=selected_username)
        user_email = selected_user.email
        image = get_object_or_404(ImageUpload, id=selected_image_id)

        # Auto-generate a secure random password
        password = secrets.token_urlsafe(8)

        # Store the generated password with the image object
        image.qr_password = password
        image.save()

        # Generate QR code with the password
        qr_image = generate_qr(password)

        # Store image ID in session
        request.session['last_image_id'] = image.id

        save_email_history(request.user, image, user_email, password)


        # Create and send email
        email = EmailMessage(
            subject,
            'Scan the attached QR code to retrieve your password.',
            settings.EMAIL_HOST_USER,
            [user_email]
        )
        email.attach('qr_code.png', qr_image.getvalue(), 'image/png')
        email.send()

        messages.success(request, 'Email with QR code sent successfully!')
        return redirect('verify_qr')  # No image_id in the URL

    return render(request, 'myapp/send_email.html', {'usernames': usernames, 'images': images})



@login_required
def verify_qr(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            entered_password = form.cleaned_data['password']

            # Fetch the image associated with the entered password from SentEmail
            sent_email = SentEmail.objects.filter(secret_key=entered_password).first()

            if sent_email:
                # Fetch the image associated with the password from ImageUpload
                image = ImageUpload.objects.filter(qr_password=entered_password).first()
                if image:
                    messages.success(request, 'Password correct! Image displayed.')
                    return render(request, 'myapp/display_image.html', {'image': image})
                else:
                    messages.error(request, 'No image found for the entered password.')
            else:
                messages.error(request, 'Incorrect password. Please try again.')
    else:
        form = PasswordForm()

    return render(request, 'myapp/enter_password.html', {'form': form})



def save_email_history(user,sent_at, recipient_email, password):
    SentEmail.objects.create(
        user=user,
        sent_at=timezone.now() ,  # Access the image file field directly
        recipient_email=recipient_email,
        secret_key=password
    )

# views.py

@login_required
def email_history(request):
    sent_emails = SentEmail.objects.filter(user=request.user)
    return render(request, 'myapp/email_history.html', {'sent_emails': sent_emails})

@login_required
def delete_key(request, key_id):
    sent_email = get_object_or_404(SentEmail, id=key_id, user=request.user)
    image = sent_email.image  # Get the related image object

    # Check if the image has a secret_key field and clear it
    if hasattr(image, 'secret_key'):
        image.secret_key = ""  # Clear the secret key
        image.save()           # Save the updated image

    # Delete the sent email record
    sent_email.delete()

    messages.success(request, 'Secret key and email record deleted successfully!')
    return redirect('email_history')  # Corrected redirect



@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'myapp/profile.html', {'profile': profile})


from django.shortcuts import render


