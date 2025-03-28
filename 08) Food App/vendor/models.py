from django.db import models
from accounts.models import User,UserProfile
from accounts.utills import send_notification

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

