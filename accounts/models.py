from django.db import models
import hashlib
from datetime import timedelta

from django.utils import timezone

class User(models.Model):
    # UserIDがなかったので追加,これはUser自身が自由に変更できる
    UserID = models.CharField('UserID', max_length=15, unique=True, null=False)
    name = models.CharField('name',max_length=32,unique=True)
    email = models.EmailField(max_length=32)
    bio = models.CharField(max_length=1024)
    password = models.CharField(max_length=256)
    # 元々がChar型でしたがImage専用のFieldに変更しました
    # ProfileImage = models.ImageField(upload_to='images', verbose_name='ProfileImage', null=True, blank=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    block_users = models.ManyToManyField('self', through='UserBlock')
    follow_users = models.ManyToManyField('self', through='UserFollow')
    # public_posts = models.ManyToManyField('Post', through='PublicPost')

    def __str__(self):
        return self.UserID
    # ここは元々はfull_nameでかえしていましたがfull_nameの値がない為、仮置きでUserIDかえしときます
    
def in_30_days():
    return timezone.now() + timedelta(days=30)

# アクセストークン
class AccessToken(models.Model):
    # ひもづくユーザー
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # アクセストークン(max_lengthが40に設定されている理由は、トークンはsha1でハッシュ化した文字列を設定するため)
    token = models.CharField(max_length=40)
    # アクセス日時
    access_datetime = models.DateTimeField(default=in_30_days)

    def str(self):
        # メールアドレスとアクセス日時、トークンが見えるように設定
        dt = timezone.localtime(self.access_datetime).strftime("%Y/%m/%d %H:%M:%S")
        return self.user.UserID + '(' + dt + ') - ' + self.token

    @staticmethod
    def create(user: User):
        # ユーザの既存のトークンを取得
        if AccessToken.objects.filter(user=user).exists():
            # トークンがすでに存在している場合は削除
            AccessToken.objects.get(user=user).delete()

        # トークン作成（UserID + Password + システム日付のハッシュ値とする）
        dt = timezone.now()
        str = user.UserID + user.password + dt.strftime('%Y%m%d%H%M%S%f')
        hash = hashlib.sha1(str.encode('utf-8')).hexdigest()

        # トークンをDBに追加
        token = AccessToken.objects.create(
            user=user,
            token=hash,
            access_datetime=dt)

        return token
    
class UserBlock(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='src_blockuser')
    block = models.ForeignKey(User, on_delete=models.PROTECT, related_name='trg_blockuser')

    def __str__(self):
        return self.full_name
    
class UserFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='src_followuser')
    follow = models.ForeignKey(User, on_delete=models.PROTECT, related_name='trg_followuser')
    is_permit = models.BooleanField()

    def str(self):
        return self.user
# Create your models here.
