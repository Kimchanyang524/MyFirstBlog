from django.db import models
from django.utils.translation import gettext as _
from accounts.models import User


class Post(models.Model):
    title = models.CharField(_("제목"), max_length=50)
    content = models.TextField(_("내용"))
    head_image = models.ImageField(
        _("메인 이미지"), upload_to="blog/images/%Y/%m/%d/", blank=True
    )
    file_upload = models.FileField(
        _("파일"), upload_to="blog/files/%Y/%m/%d/", blank=True
    )
    created_at = models.DateTimeField(_("작성일자"), auto_now_add=True)
    updated_at = models.DateTimeField(_("수정일자"), auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    tags = models.ManyToManyField("Tag", blank=True, verbose_name="태그")
    view_count = models.PositiveIntegerField(verbose_name="조회수", default=0)
    likes_count = models.PositiveIntegerField(verbose_name="좋아요", default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="원본 포스트"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    message = models.TextField(_("메시지"))
    created_at = models.DateTimeField(_("작성일자"), auto_now_add=True)
    updated_at = models.DateField(_("수정일자"), auto_now=True)

    def __str__(self):
        return self.message


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="태그 이름")

    def __str__(self):
        return self.name


class Likes(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="포스트 아이디")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")

    def __str__(self):
        return self.name
