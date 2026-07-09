from django.db import models
import re
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="category/")

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    contact = models.CharField(max_length=10)
    address = models.TextField()
    photo = models.ImageField(upload_to="users/")

    def clean(self):
        errors = {}

        # USERNAME
        username = self.username.strip() if self.username else ""
        if not username:
            errors['username'] = "Username required"
        elif not re.match(r'^[A-Za-z ]+$', username):
            errors['username'] = "Only alphabets allowed"
        elif len(username) < 4:
            errors['username'] = "Min 4 characters required"

        # EMAIL
        if not self.email.lower().endswith("@gmail.com"):
            errors['email'] = "Only Gmail allowed"
        else:
            if User.objects.filter(email=self.email).exclude(id=self.id).exists():
                errors['email'] = "User already exists — Go Login"
    
        # PASSWORD
        pwd = self.password
        if len(pwd) < 8 or len(pwd) > 15:
            errors['password'] = "Password 8–15 characters"

        if not re.search(r'[A-Z]', pwd):
            errors['password'] = "At least 1 capital letter"

        if not re.search(r'[a-z]', pwd):
            errors['password'] = "At least 1 small letter"

        if not re.search(r'[0-9]', pwd):
            errors['password'] = "At least 1 number"

        if not re.search(r'[@#$%^&*]', pwd):
            errors['password'] = "At least 1 special character"

        # CONTACT
        if not re.match(r'^[6-9]\d{9}$', self.contact):
            errors['contact'] = "Invalid mobile number"

        # ADDRESS
        if not self.address.strip():
            errors['address'] = "Address required"

        # PHOTO
        if self.photo:
            if not self.photo.name.lower().endswith(('.jpg','.jpeg','.png')):
                errors['photo'] = "Only JPG, PNG allowed"
            if self.photo.size > 2 * 1024 * 1024:
                errors['photo'] = "Max size 2MB"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    old_price = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.product.name
    
class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=5)
    stock = models.IntegerField()

    class Meta:
        unique_together = ['product', 'size']

    def __str__(self):
        return f"{self.product.name} - {self.size}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=5, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    price = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField()
    order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

