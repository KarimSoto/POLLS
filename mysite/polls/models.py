from django.db import models, transaction
import datetime
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth import get_user_model


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    
class Vote(models.Model):
    
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    nombreusuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
 























#class DominoStaff(models.Model):
    #class Meta:  # Corregir "meta" a "Meta"
      #  permissions = [("sell_pizzas", "Puede vender Pizzas")]

#class Repartidor(DominoStaff):
   # class Meta:  # Corregir "meta" a "Meta"
      #  proxy = True
       # permissions = [("deliver_pizzas", "Puede repartir Pizzas")]

#class Cocinero(DominoStaff):
   # class Meta:  # Corregir "meta" a "Meta"
       # proxy = True
       # permissions = [("cook_pizzas", "Puede cocinar Pizzas")]





#class Author(models.Model):
   # id = models.AutoField(primary_key=True)
   # name= models.CharField(max_length=100)
   # age=models.PositiveSmallIntegerField()



#class Book(models.Model):
    #id = models.AutoField(primary_key=True)
    #title= models.CharField(max_length=50)
   # author=models.ForeignKey(Author, on_delete=models.CASCADE, null=False, blank=False, related_name='books')
   # created_at=models.DateTimeField(auto_now_add=True)

   # @classmethod
   # def changes(cls):
     #   with transaction.atomic():
            #codigo
          #  pass
    
   # def __str__(self):
      #  return self.title