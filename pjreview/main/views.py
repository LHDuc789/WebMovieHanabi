from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Avg
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Count
from django.contrib import messages
from django.db.models.functions import ExtractYear



# Create your views here.
def home(request):
    allProducts = Product.objects.all().order_by('-release_date')[:6] #select * from Product
    Sort_by_liked = Product.objects.all().annotate(like_count=Count('liked')).order_by('-like_count','-averageRating')[:3] #sort by liked limit number 3
    Sort_by_view = Product.objects.all().order_by('-product_views')[:3] #select * from Product
    context = {
        "products": allProducts,
        "sort_liked": Sort_by_liked,
        "sort_by_view": Sort_by_view,
    }
    return render(request,'main/index.html',context) 

def search_product(request):
    allProducts = None
    query = request.GET.get("title")
    allProducts = Product.objects.filter(name__icontains=query).order_by('-release_date')
    paginator = Paginator(allProducts, 6) # Show 6 contacts per page.
    page_number = request.GET.get('page')
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    
    context = {
        "query" :  query,
        "products": queryset,
    }
    return render(request,'main/search.html',context)

def sort_like_average(request):
    Sort_by_liked = Product.objects.all().annotate(like_count=Count('liked')).order_by('-like_count','-averageRating')
    paginator = Paginator(Sort_by_liked, 6) # Show 6 contacts per page.
    page_number = request.GET.get('page')
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    
    context = {
        "products": queryset,
    }
    return render(request,'main/sort_like_average.html',context) 

def sort_views(request):
    Sort_by_view = Product.objects.all().order_by('-product_views') #select * from Product
    paginator = Paginator(Sort_by_view, 6) # Show 6 contacts per page.
    page_number = request.GET.get('page')
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    
    context = {
        "products": queryset,
    }
    return render(request,'main/sort_views.html',context) 

def allProducts(request):
    allProducts = Product.objects.all().order_by('-release_date') #select * from Product
    paginator = Paginator(allProducts, 6) # Show 6 contacts per page.
    page_number = request.GET.get('page')
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    
    context = {
        "products": queryset,
    }
    return render(request,'main/allProducts.html',context) 


def sort_year(request, year):
    sort_year = Product.objects.annotate(year=ExtractYear('release_date')).filter(year = year)

    paginator = Paginator(sort_year, 6) # Show 6 contacts per page.
    page_number = request.GET.get('page')
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "sort_year": queryset,
        "year":year,
    }
    return render(request,'main/sort_year.html',context) 

#detail page

def liked_user(request, id):
    Sort_by_value = Like.objects.filter(user=request.user, value="Thích")
    paginator = Paginator(Sort_by_value, 6) # Show 6 contacts per page.
    page_number = request.GET.get('page')
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "sort_by_value": queryset,
    }
    return render(request,'main/liked_user.html',context)

def detail(request, id):
    product = Product.objects.get(id=id) #select * from Product where id=id
    reviews = Review.objects.filter(product=id).order_by("-date") #-comment if descending
    average = reviews.aggregate(Avg('rating'))["rating__avg"]
    typeproduct= TypeProduct.objects.filter(product=id)
    if average == None:
        average = 0
    average = round(average,2)
    Product.objects.filter(id=id).update(averageRating=average)
    num_ep= Video.objects.filter(product=id).count()
    context = {
        "product": product,
        "reviews": reviews,
        "average": average,
        "num_ep" : num_ep,
        "type_product": typeproduct,
    }
    return render(request,'main/details.html',context)

   
def watch_movie(request, id, ep):
    product = Product.objects.get(id=id)
    reviews = Review.objects.filter(product=id).order_by("-date") #-comment if descending
    product.product_views = product.product_views + 1
    product.save()
    video = Video.objects.filter(product=id).get(ep=ep)
    num_ep= Video.objects.filter(product=id).count()
    num_eps=[]
    for i in range(num_ep):
        num_eps.append(i+1)
    context = {
        "video": video,
        "num_eps": num_eps,
        "product": product,
        "num_ep" : num_ep,
        "reviews": reviews,
    }
    return render(request, 'main/watch.html', context)

def like_product(request, id):
    user = request.user
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_obj= Product.objects.get(id=product_id)
        if user in product_obj.liked.all():
            product_obj.liked.remove(user)
        else:
            product_obj.liked.add(user)
        like, created = Like.objects.get_or_create(user=user, product_id=product_id)
        
        if not created:
            if like.value == 'Thích':
                like.value = 'Bỏ Thích'
            else:
                like.value = 'Thích'
        like.save()
    return redirect("main:detail",id)

#add to the database
def add_product(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method=='POST':
                form = ProductForm(request.POST or None)
                if form.is_valid():
                    data=form.save(commit=False)
                    data.save()
                    return redirect("main:home")
            else:
                form = ProductForm()
            return render(request,'main/addproduct.html',{"form": form, "controller": "Thêm Sản Phẩm"})
        else:
            #if not admin
            return redirect("main:home")
    #if not login
    return redirect("accounts:login")

#edit and update to the database
def edit_product(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            product = Product.objects.get(id=id)
            if request.method=='POST':
                form= ProductForm(request.POST or None, instance=product)
                if form.is_valid():
                    data=form.save(commit=False)
                    data.save()
                    return redirect("main:detail",id)
            else:
                form= ProductForm(instance=product)
            return render(request,'main/addproduct.html',{"form": form, "controller": "Chỉnh Sửa Sản Phẩm"})
        else:
            #if not admin
            return redirect("main:detail",id)
    #if not login
    return redirect('accounts:login')

#delete and save to database
def delete_product(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            product = Product.objects.get(id=id)
            product.delete()
            return redirect("main:home")
        else:
            #if not admin
            return redirect("main:detail",id)
    #if not login
    return redirect('accounts:login')

def add_review(request,id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        if request.method=="POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST["comment"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.product = product
                data.save()
                return redirect('main:detail',id)
            else:
                messages.info(request, 'Bình Luận Không Được Để Trống !!!')
                return redirect('main:detail',id)
        else:
            form = ReviewForm()
        return render(request,'main/details.html',{"form": form})
    else:
        return redirect('accounts:login')

def edit_review(request,product_id,review_id):
    if request.user.is_authenticated:
        product=Product.objects.get(id=product_id)
        review=Review.objects.get(product=product, id=review_id)
        
        #check user login
        if request.user == review.user:
            #grant permission
            if request.method=="POST":
                form = ReviewForm(request.POST, instance = review)
                if form.is_valid():
                    data=form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = "Đánh giá chỉ cho phép trong phạm vi từ 0 đến 10. Vui lòng sửa lại."
                        return render(request,'main/editreview.html',{"error": error, "form": form})
                    else:
                        data.save()
                        return redirect("main:detail", product_id)
            else:
                form = ReviewForm(instance=review)
            return render(request,"main/editreview.html", {"form": form})
        else:
            return redirect("main:detail",product_id)
    else:
        return redirect("accounts:login")
    
def delete_review(request,product_id,review_id):
    if request.user.is_authenticated:
        product=Product.objects.get(id=product_id)
        review=Review.objects.get(product=product, id=review_id)
        
        #check user login
        if request.user == review.user:
            #grant permission
            review.delete()
        return redirect("main:detail",product_id)
    else:
        return redirect("accounts:login")
                
        
        
def list_of_types(request):
    allTypes = ListType.objects.all()
    context={
        "list_types": allTypes,
    }
    return render(request,"main/list_of_types.html", context)


def sort_by_type(request,name):
    by_type_name = TypeProduct.objects.filter(listtypes__name=name).first()
    by_type = TypeProduct.objects.filter(listtypes__name=name).order_by('-product__release_date')
    paginator = Paginator(by_type, 6) # Show 6 contacts per page.
    page_number = request.GET.get('page')
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    
    context={
        "sort_by_type": queryset,
        "by_type_name": by_type_name,
    }
    return render(request,"main/typeproduct.html", context)
