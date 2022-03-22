from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from pyparsing import line

# Create your models here.
class Numeron(models.Model):
    # number_str = models.IntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(9999)]
    # )
    # 4桁の入力しか認めない
    number_str = models.CharField(max_length=4, validators=[MinLengthValidator(4)])
    line_id = models.CharField(max_length=300)

    def __str__(self):
        return self.number_str
