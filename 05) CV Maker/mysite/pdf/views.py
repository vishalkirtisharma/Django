from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from . import forms
from . import models
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
from django.views.generic import ListView,CreateView
# Create your views here.


# class

# def accept(request):
#     form  = forms.ProfileForm()

#     if request.method == 'POST':
#         form = forms.ProfileForm(request.POST)
#         if form.is_valid():
#             form.save(commit=False)
#             # form.cleaned_data['skill'] = form.cleaned_data['skill'].spilit(', ') 
#             messages.success(request, 'Profile saved successfully for user: {}'.format(form.cleaned_data['name']))

#             form  = forms.ProfileForm()
#             return render(request, 'pdf/accept.html',{'form':form})
#     else:

#         return render(request, 'pdf/accept.html',{'form':form})



from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import ProfileModel
from . import forms

class AcceptView(CreateView):
    model = ProfileModel
    form_class = forms.ProfileForm
    template_name = 'pdf/accept.html'
    success_url = reverse_lazy('pdf:accept')  # Redirect to the same page after success (can be modified)

    def form_valid(self, form):
        # Save the form, but don't commit to the database yet
        profile = form.save(commit=False)

        # Process the skill data (e.g., split the comma-separated skills into a list)
        profile.skill = profile.skill.split(', ')  # Fixing typo 'spilit' to 'split'

        # Save the profile object to the database
        profile.save()

        # Display a success message
        messages.success(self.request, f'Profile saved successfully for user: {profile.name}')

        # Redirect to the success URL
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle invalid form, re-render with errors
        print(form.errors)
        return super().form_invalid(form)
    

def resume(request,pk):
    user =get_object_or_404(models.ProfileModel,pk=pk)
    template = loader.get_template('pdf/resume.html')
    html = template.render(context={'user':user})
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
        }
    pdf = pdfkit.from_string(html,False,options=options)
    respose = HttpResponse(pdf,content_type = 'application/pdf')
    respose['Content-Disposition'] = 'attachment' 
    filename="resume.pdf"
    return respose






# def all(request):
#     user_all = models.ProfileModel.objects.all()
#     return render(request,'pdf/list.html',{'user_all':user_all})


class all(ListView):
    model = models.ProfileModel
    template_name = 'pdf/list.html'
    context_object_name = 'user_all'


 