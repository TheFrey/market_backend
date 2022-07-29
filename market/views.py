from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from .forms import LoginForm, UserRegistrationForm, CommentForm, SearchForm
from django.contrib.auth import authenticate, login


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirect_to=product_list)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'market/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    comments = product.comments.filter(active=True)
    rating_list = [int(comment.rating) for comment in comments]

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.user = request.user
            new_comment.save()
    else:
        new_comment = 0
        comment_form = CommentForm()
    if len(rating_list) > 0:
        rating = round(sum(rating_list) / len(rating_list), 2)
    else:
        rating = 0
    cart_product_form = CartAddProductForm()
    return render(request,
                  'market/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'comments': comments,
                   'comment_form': comment_form,
                   'rating': rating,
                   'new_comment': new_comment
                   })


def product_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET, initial={'price_up': 100, 'price_down': 0})
        if form.is_valid():
            query = form.cleaned_data['query']
            category = form.cleaned_data['category']
            price_up = form.cleaned_data['price_up']
            price_down = form.cleaned_data['price_down']
            results = Product.objects.filter(name__icontains=query, category__name=category)
    return render(request,
                  'market/product/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
