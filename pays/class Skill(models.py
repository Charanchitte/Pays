class Skill(models.Model):
    skill = models.CharField(max_length=256,help_text='Enter your skills')
    def  _str_(self):
        return self.skill

    
class Professional(models.Model):
    
    username = models.CharField(max_length=20, unique = True, help_text='Enter your username')
    name = models.CharField(max_length=20, help_text='Enter your name')
    email = models.EmailField(max_length=254,unique = True, help_text='Enter your mail id')
    password = models.CharField(max_length=20, help_text='Set the Password')
    skills=models.ForeignKey('Skill',on_delete=models.SET_NULL,null=True)
    up_for_work=models.CharField(max_length=3,help_text='Are you up for work')
    response_time=models.CharField(max_length=20)
    member_since=models.DateField(auto_now=True)
    Last_delivary=models.DateField(auto_now=True)
    expert_in=models.CharField(max_length=30)
    no_works=models.IntegerField(default=0)
    rating=models.IntegerField( default=1,validators=[MaxValueValidator(5), MinValueValidator(1)])
    def  _str_(self):
        return self.name
