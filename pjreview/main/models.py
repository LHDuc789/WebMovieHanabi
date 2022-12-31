from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Product(models.Model):
    name=models.CharField('Tên Sản Phẩm',max_length=300)
    director=models.CharField('Đạo Diễn',max_length=300)
    cast=models.CharField('Diễn Viên Nổi Bật',max_length=800, null=True, blank=True)
    description=models.TextField('Tóm Lược Nội Dung',max_length=5000)
    epnums=models.IntegerField('Số Tập', default=0, null=True, blank=True)
    timeep=models.IntegerField('Thời Lượng', default=0, null=True, blank=True)
    release_date=models.DateField('Ngày Công Chiếu')
    averageRating=models.FloatField('Đánh Giá', default=0.0)
    image=models.URLField('Ảnh Sản Phẩm',default=None, null=True)
    product_views=models.IntegerField('Lượt Xem', default=0, null=True, blank=True)
    liked=models.ManyToManyField(User, default=None, blank=True)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    @property
    def num_likes(self):
        return self.liked.all().count()
    
LIKE_CHOICES = (
        ('Thích','Thích'),
        ('Bỏ Thích','Bỏ Thích'),
)
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Thích', max_length=15)
    
    def __str__(self):
        return str(self.product)
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField('Bình Luận',max_length=1000)
    rating = models.FloatField('Đánh Giá',default=0)
    date = models.DateTimeField(auto_now=True,editable=False)
    
    def __str__(self):
        return self.user.username
    
class Video(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    video = models.FileField(upload_to='video')
    ep = models.IntegerField(default=1, null=True, blank = True)
    
    def __str__(self):
        return self.product.name
    
    def __unicode__(self):
        return self.product.name

class ListType(models.Model):
    name=models.CharField('Thể Loại',max_length=300, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    
class TypeProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    listtypes= models.ForeignKey(ListType, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + '___' + self.listtypes.name
    
    def __unicode__(self):
        return self.product.name