from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import authenticate


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return f"{self.username} ({self.email})"

    def auth(self, user):
        """
        Authenticate the user with username and password.
        """
        users = CustomUser.objects.filter(username=user.email, password=user.password)
        return authenticate(email=user.email, password=user.password, username=user.username) and users is not None


class Chats(models.Model):
    id = models.AutoField(primary_key=True)
    to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_chats')
    by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_chats')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Chat from {self.by.username} to {self.to.username} : {self.message} at {self.timestamp}"


class ChatRooms(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user1_rooms')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user2_rooms')
    name = models.CharField(max_length=550, blank=True, null=True)
    chats = models.ManyToManyField(Chats, related_name='chat_rooms', blank=True)

    def __str__(self):
        return f"Chat Room between {self.user1.username} and {self.user2.username}"
