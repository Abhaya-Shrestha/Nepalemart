import datetime

from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.utils.text import slugify


# Create your models here.
class Slider(models.Model):
    DISCOUNT_DEAL = (
        ('HOT DEALS', 'HOT DEALS'),
        ('New Arrivals', 'New Arrivals'),
    )

    Image = models.ImageField(upload_to='media/slider_imgs')
    Discount_Deal = models.CharField(choices=DISCOUNT_DEAL, max_length=100)
    SALE = models.IntegerField()
    Brand_Name = models.CharField(max_length=200)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200)

    def __str__(self):
        return self.Brand_Name


class banner_area(models.Model):
    image = models.ImageField(upload_to='media/banner_img')
    Discount_Deal = models.CharField(max_length=100)
    Quote = models.CharField(max_length=100)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.Quote


class Main_category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    main_category = models.ForeignKey(Main_category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " --> " + self.main_category.name


class Sub_category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.category.main_category.name + " --> " + self.category.name + ' --> ' + self.name


class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    total_quantity = models.IntegerField()
    Availability = models.IntegerField()
    featured_image = models.ImageField(upload_to='media/product_img')
    product_name = models.CharField(max_length=500)
    price = models.IntegerField()
    Discount = models.IntegerField()
    tax = models.IntegerField(null=True)
    packing_cost = models.IntegerField(null=True)
    Product_information = RichTextField()
    model_name = models.CharField(max_length=100)
    Categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    Tags = models.CharField(max_length=1000)
    Description = RichTextField()
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)

    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "app_Product"


# slug for product url-----------------------------------------------------------------
def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, Product)


# class Coupon_Code(models.Model):
#     code = models.CharField(max_length=100)
#     discount = models.IntegerField()


class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Image_url = models.ImageField(upload_to='media/product_img')


class Additional_Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    address = models.TextField()
    state = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=14, blank=True)
    email = models.EmailField()
    addition_info = models.TextField(blank=True)
    PayableAmount = models.IntegerField(default='0')

    payment_id = models.CharField(max_length=300, null=True, blank=True)
    paid = models.BooleanField(default=False, null=True)

    date = models.DateTimeField(default=datetime.datetime.today(), blank=True, null=True)

    def __str__(self):
        return self.user.username


class OrdersItem(models.Model):
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.CharField(max_length=300)
    quantity = models.IntegerField(default='0')
    price = models.IntegerField(default='0')
    amount = models.IntegerField(default='0')

    def __str__(self):
        return self.orders.user.username
