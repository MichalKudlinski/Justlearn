import os
import profile
import uuid
from email.policy import default

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def profile_pic_image_file_path(instance, filename):
    """Generate file path for new profile pic image"""
    ext = os.path.splittext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'profile_pic', filename)


def exercise_file_path(instance, filename):
    """Generate file path for exercise file"""
    ext = os.path.splittext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'exercise', filename)


def project_file_path(instance, filename):
    """Generate file path for project file"""
    ext = os.pathsplittext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'project', filename)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and  return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return new superuser"""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User in the system.
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        if self.is_staff:
            return self.email
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=255)
    PROFICIENCY_CHOICES = [
        ('JR', 'Junior'),
        ('MD', 'Mid'),
        ('SR', 'Senior')
    ]
    proficiency = models.CharField(
        choices=PROFICIENCY_CHOICES, default='JR', max_length=2)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=510, default='')
    image = models.ImageField(null=True, upload_to=profile_pic_image_file_path)

    def __str__(self):
        return self.user.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Skills connected with proficiency at which they are
    skills = models.ManyToManyField(Skill)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=510, default='')
    image = models.ImageField(null=True, upload_to=profile_pic_image_file_path)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.name


class Advertisement(models.Model):
    title = models.CharField(max_length=255, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    link = models.URLField(default=None)
    description = models.TextField(max_length=510, default='')


class Problem(models.Model):
    title = models.CharField(max_length=255, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    link = models.URLField(default=None)
    description = models.TextField(max_length=510)

# Na bazie ofert mozna robic chaty, tak samo na bazie korepetycji
# oferty jak student odpowiada na ogloszenie i jak nauczyciel odpowiada na problem studenta z oferta wspolpracy


class Offer(models.Model):
    name = models.CharField(max_length=255)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.DO_NOTHING, null=True)
    advertisement = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)


class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=510, default='')
    duration = models.IntegerField(default=60)
    lesson_date = models.DateTimeField(null=True)
    meeting_link = models.URLField(null=True)


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class Reviews(models.Model):
    lessons = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    rating = models.IntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(10)])


class Chat(models.Model):
    participants = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message, blank=True)

    def get_messages(self):
        res = []
        for message in self.messages.all():
            res.append(str(message))
        return res

    def get_participants(self):
        res = []
        for person in self.participants.all():
            res.append(str(person))
        return res


class Exercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    file = models.FileField(upload_to=exercise_file_path)
    timestamp = models.DateTimeField(auto_now_add=True)


class Project(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file = models.FileField(upload_to=project_file_path)
    timestamp = models.DateTimeField(auto_now_add=True)
