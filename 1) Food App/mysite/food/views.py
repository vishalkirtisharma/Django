from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from . import models
from django.template import loader
from . import forms

from django.views.generic import ListView,DetailView,CreateView

# Create your views here.

# def index(request):
#     food_item = models.Item.objects.all()
#     template = loader.get_template('food/index.html')
#     # return render(request, 'index.html', {'food_item': food_item})
#     context = {'item_list':food_item,}
#     return HttpResponse(template.render(context,request))


class IndexView(ListView):
    model = models.Item
    template_name = 'food/index.html'
    context_object_name = 'item_list'

class ItemDetailView(DetailView):
    model = models.Item
    template_name = 'food/details.html'
    context_object_name = 'item'


# def detail(request,id):
#     item = get_object_or_404(models.Item,id=id)
#     return render(request,'food/details.html',{'item':item})

class CreateItemView(CreateView):
    model = models.Item
    fields = ('item_name','item_desc','item_price','image')
    template_name = 'food/item_form.html'
    context_object_name = 'form'
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["user_name"] = self.request.user 
    #     print(self.request.user)
    #     return context
    
    def form_valid(self, form):
        print(self.request.user)
        form.instance.user_name = self.request.user
        return super().form_valid(form)
    


def create_item(request):
    form  = forms.ItemForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('food:index')
    
    return render(request,'food/item_form.html',{'form':form})

    
def update_item(request,id):
    item = get_object_or_404(models.Item,id=id)
    form = forms.ItemForm(request.POST or None,instance=item)
    
    if form.is_valid():
        form.save()
        return redirect('food:index')
    
    return render(request,'food/item_form.html',{'form':form,'item':item})
    

def delete_item(request,id):
    item = get_object_or_404(models.Item,id=id)

    if request.method == 'POST':
        item.delete()
        return redirect('food:index')
    return render(request,'food/item-delete.html',{'item':item})