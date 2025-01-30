from django.shortcuts import render,redirect
from bs4 import BeautifulSoup
import requests
from . import models
from urllib.parse import urljoin
# Create your views here.


def scrape(request):
    if request.method == 'POST':
        url = request.POST.get('search')

        page = requests.get(url)
        soup = BeautifulSoup(page.text,'html.parser')
        
        data =[]
        for link in soup.find_all('a'):
            data.append({link.string:link.get('href')})


        return render(request,'scrape.html',{'data':data})
    return render(request,'scrape.html',)
    

def check_images(url):
    try:
        response = requests.get(url,headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code ==200:
            return True
        else:
            return False
    except:
        return False

def image_scrape(request):
    if request.method == 'POST':
        url = request.POST.get('search')
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        images = soup.find_all('img')

        data = []
        for image in images:
            img_src = image.get('src')
            if check_images(img_src):       
                data.append(img_src) 
            else:
                full_url = urljoin(url, img_src) 
                data.append(full_url)
        return render(request, 'image_scrape.html', {'data': data})

    return render(request, 'image_scrape.html')