from django.db import models
from django.contrib.auth import get_user_model
import uuid
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

User = get_user_model()
# Create your models here.


class Campaign(models.Model):
    campaign_choices = [
        ('Child Education', 'child education'),
        ('Child Healthcare', 'child healthcare')
    ]


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/proofs/', null=False, blank=False)
    title = models.CharField(max_length=100, null=False, default=None)
    phone_number = models.CharField(max_length=50, null=False)
    goals = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=10)
    amount_raised = models.DecimalField(null=False, default=0,decimal_places=2, max_digits=10 )
    campaign_purpose = models.CharField(max_length=50, choices=campaign_choices, null=False , default='Child Education')
    created_at = models.DateTimeField(auto_now_add=True)

    def resize_image(self):
        """
        Resize image to a standard size (e.g., 600x400)
        """
        try:
            img = Image.open(self.image)  # Open the image file
            img = img.convert('RGB')  # Convert image to RGB if it's in another mode
            img = img.resize((600, 400), Image.Resampling.LANCZOS)  # Resize to 600x400

            # Save the resized image back to the file field
            image_io = BytesIO()
            img.save(image_io, format='JPEG')
            image_io.seek(0)

            # Create a new InMemoryUploadedFile from the resized image
            self.image = InMemoryUploadedFile(image_io, None, self.image.name, 'image/jpeg', image_io.tell(), None)
            print(self.image.name)
        except Exception as e:
            print(f"Error resizing image: {e}")
            pass  # Handle the error as you see fit (e.g., fallback, logging)

    def save(self, *args, **kwargs):
        # Resize image before saving to database
        if self.image:
            self.resize_image()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
    
    def progress(self):
        #Calculate the progress of the campaign as a percentage
        if self.goals > 0:
            print(self.amount_raised)
            return round(self.amount_raised / self.goals) * 100
        return 0
        
    def current_amount(self):
        return (donation.amount for donation in self.donation.all())
    

class Donation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    donation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    donated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    message = models.CharField(max_length=100, null=True, default='')
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    

    def __str__(self):
        return f"{self.user.username} donated to {self.campaign.title}"
    

class Withdrawal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True)
    transaction_ref_num = models.CharField(null=True, max_length=16)
    account_number = models.IntegerField(null=True)
    account_name = models.CharField(null=True, max_length=50)

