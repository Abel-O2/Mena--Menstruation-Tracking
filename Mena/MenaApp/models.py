from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Period(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    day = models.IntegerField()

class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    mood = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.mood} on {self.date}"

class CyclePhase(models.Model):
    PHASE_CHOICES = [
        ('menstruation', 'Menstruation'),
        ('follicular', 'Follicular'),
        ('ovulation', 'Ovulation'),
        ('luteal', 'Luteal'),
    ]

    name = models.CharField(max_length=50, choices=PHASE_CHOICES)
    start_day = models.IntegerField()
    end_day = models.IntegerField()
    symptoms = models.TextField()
    description = models.TextField(null=True, blank=True)
    mood = models.TextField()

    def __str__(self):
        return self.name
    
class Lesson(models.Model):
    PHASE_CHOICES = [
        ('menstruation', 'Menstruation'),
        ('follicular', 'Follicular'),
        ('ovulation', 'Ovulation'),
        ('luteal', 'Luteal'),
    ]

    phase = models.CharField(max_length=50, choices=PHASE_CHOICES)
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return f"{self.phase}: {self.title}"


class Comment(models.Model):
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Symptoms(models.Model):
    phase = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phase
    

class Calendar(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title


