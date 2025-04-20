from django.db import models
from accounts.models import User,UserProfile
from accounts.utills import send_notification
from datetime import time

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile,related_name='user_profile',on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,blank=True,unique=True)
    vender_licence =models.ImageField(upload_to='vendor/licence')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.vendor_name


    def save(self,*args,**kwargs):
        if self.pk is not None:
            # update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved':self.is_approved
                }
                if self.is_approved == True:
                
                    # send email to admin
                    mail_subject = 'Your Restaurent has been approved'
                    send_notification(mail_subject,mail_template,context)
                else:
                    mail_subject = 'You are not eligible for food menu in market place'
                    send_notification(mail_subject,mail_template,context)
                    # send email to admin
                    pass

        return super(Vendor,self).save(*args,**kwargs)
    
    def is_open(self,*args,**kwargs):
        from datetime import datetime,date

        today = date.today().isoweekday()
        current_opening_hours = OpeningHours.objects.filter(vendor=self,day=today)
        current_time = datetime.now().strftime('%H : %M: %S')

        
        is_open=None

        for i in  current_opening_hours:
            start = str( datetime.strptime(i.from_hour,'%I:%M %p').time())
            end = str (datetime.strptime(i.to_hour,'%I:%M %p').time())
            if current_time > start and current_time < end:
                is_open = True
                break
            else:
                is_open = False
        return is_open

DAYS = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday')
]



HOURS_OF_DAYS = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p') ) for h in range(24) for m in [0, 30] ]

class OpeningHours(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    day =  models.IntegerField(choices=DAYS)
    from_hour =   models.CharField(choices=HOURS_OF_DAYS,max_length=10,blank=True)
    to_hour =   models.CharField(choices=HOURS_OF_DAYS,max_length=10,blank=True)
    is_closed = models.BooleanField(default=False)


    class Meta:
        verbose_name = "Opening Hours"
        ordering = ('day','-from_hour')
        unique_together = ('vendor','day','from_hour','to_hour')
    
    def __str__(self):
        return self.get_day_display()