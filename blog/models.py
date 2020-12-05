from django.db import models

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    description = models.CharField(max_length=500,default='')
    body = models.TextField()

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]
    
class Photo(models.Model):
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/',blank=True,null=True)

class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    body = models.CharField('댓글',max_length=150)#제일 첫번째 parameter로 '댓글'을 추가해주면 해당 field의 label값으로 body가 아닌 '댓글'이 붙게 된다.
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body