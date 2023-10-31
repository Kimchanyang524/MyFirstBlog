from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser


def user_directory_path(instance, filename):
    """
    instance는 모델 인스턴스 (예: User)\n
    filename은 업로드된 파일의 이름
    """
    return f"accounts/images/user_{instance.username}/{filename}"


class User(AbstractUser):
    nickname = models.CharField(_("닉네임"), max_length=50)
    profile_img = models.ImageField(
        _("프로필 사진"), upload_to=user_directory_path, blank=True
    )

    class Meta:
        db_table = "User"
