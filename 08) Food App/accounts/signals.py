
from .models import User,UserProfile 
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('userprofile is created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print('userprofile is updated')
        except:
            UserProfile.objects.create(user=instance)
            print('userprofile is not exist but created')

@receiver(pre_save,sender=User)
def pre_save_profile_received(sender,instance,**kwargs):
    print(instance.username, 'this is being saved')

# post_save.connect(post_save_create_profile_receiver,sender=User)
