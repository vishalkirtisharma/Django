from django.shortcuts import render,get_object_or_404
from . import models
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator

# Create your views here.



def index(request):
    products = models.ProductsModel.objects.all()

    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        products = products.filter(title__icontains=item_name)
    

    paginator = Paginator(products,12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)



    return render(request, 'shop/index.html', {'products': products})


# class IndexView(ListView):
#     model = models.ProductsModel
#     template_name = 'shop/index.html'
#     context_object_name = 'products'
#     paginate_by = 2  # Specify number of items per page

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         item_name = self.request.GET.get('item_name')
#         if item_name:
#             queryset = queryset.filter(title__icontains=item_name)
#         return queryset


def detail(request,id):
    product = get_object_or_404(models.ProductsModel,id=id) 
    return render(request,'shop/details.html',{'product':product})


def checkout(request):
    if request.method == 'POST':
        items = request.POST.get('items')
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
   

        # You can save the order details to the database here, if needed
        order = models.OrderModel(item=items,name=name, address=address, phone=phone, city=city)
        order.save()    


    return render(request,'shop/checkout.html')