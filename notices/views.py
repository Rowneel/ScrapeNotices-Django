from django.http import JsonResponse
from django.shortcuts import redirect, render
import requests
import ssl
import re
import certifi 
from bs4 import BeautifulSoup as bs
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from .models import Notice
# Create your views here.


def scrap_notices():
    url = "https://iost.tu.edu.np/notices"
    
    r = requests.get(url,verify=False)
    soup = bs(r.content,"html.parser")
    posts =[]
    for _ in range(3):
        notices = soup.findAll("div",attrs={"class":"recent-post-wrapper shdow"})
        for notice in notices:
            date_str = notice.find('span',attrs={"id":"nep_month"}).contents[0]
            date = datetime.strptime(date_str,'%Y-%m-%d').date()
            link = notice.find('a')['href']
            title = notice.find('h5').contents[0]
            req = requests.get(link,verify=False)
            souppdf = bs(req.content,"html.parser")

            pattern = re.compile(r'/notices/(\d+)$')

            # Search for the pattern in the URL
            match = pattern.search(link)
            if match:
                # Extract the number from the first capturing group
                number = match.group(1)

            # links = souppdf.find_all('a', href=re.compile('https://portal.tu.edu.np/notice/'))
            # pdf = links[1]["href"]
            pdf = souppdf.find(href=re.compile(f'https://portal.tu.edu.np/notice/{number}'))["href"]
            data = {"date":date,"title":title,"pdf":pdf}
            posts.append(data)
        np = soup.find('a',rel="next")["href"]
        r = requests.get(np,verify=False)
        soup = bs(r.content,"html.parser")
    return posts



def update_notices(request):
    if request.method == 'POST':
        posts = scrap_notices()
        for post in posts:
            date = post['date']
            title = post['title']
            existing_post = Notice.objects.filter(date=date,title=title).first()
            if existing_post:
                pass
            else:
                new_post = Notice(
                    title = post['title'],
                    date = post['date'],
                    pdf = post['pdf']
                )
                new_post.save()
        return redirect('index')
    return render("error.html")


def index(request):

    posts = Notice.objects.all().order_by('-date')
    
    p = Paginator(posts, 6)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj}
    # sending the page object to index.html
    return render(request, 'index.html', context)
    # return render(request, 'index.html',context)