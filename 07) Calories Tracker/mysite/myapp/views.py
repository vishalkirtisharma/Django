from django.shortcuts import render,get_object_or_404,redirect
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.






def index(request):
    food_item = models.FoodModel.objects.all()

    # Get the current user
    user = request.user
    print(user)
    # If the user is authenticated, filter their consumed food items
    if user.is_authenticated:
        consume_food_item = models.Consume.objects.filter(user=user)
        
        if request.method == 'POST':
            food_consumed = request.POST.get('food_consumed')
            
            # Get the food item or return a 404 if not found
            food_consumed = get_object_or_404(models.FoodModel, name=food_consumed)
            
            # Create a new consumption entry for the user
            consume = models.Consume(food_consumed=food_consumed, user=user)
            consume.save()
        return render(request, 'index.html', {
            'foods': food_item,
            'consume_food': consume_food_item,
        })
    else:
        return redirect('login')



def delete(request, id):
    consume = get_object_or_404(models.Consume, id=id)
    if request.method =="POST":
        consume.delete()
        return redirect('index')
    
    return render(request,'delete.html',{'food':consume})


def register(request):
    form = UserCreationForm()
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        form.save()
        return redirect('login')
    
    return render(request,'register.html',{'form':form})
