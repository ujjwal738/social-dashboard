# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from .forms import RegisterForm
# from django.contrib import messages

# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Account created successfully.")
#             return redirect('login')
#     else:
#         form = RegisterForm()
#     return render(request, 'accounts/register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('profile')
#         else:
#             messages.error(request, 'Invalid credentials')
#     return render(request, 'accounts/login.html')

# @login_required
# def profile_view(request):
#     return render(request, 'accounts/profile.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import tweepy
import requests

def fetch_tweets(username):
    api_key = 'your_api_key'
    api_secret = 'your_api_secret'
    access_token = 'your_access_token'
    access_token_secret = 'your_access_token_secret'

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        tweets = api.user_timeline(screen_name=username, count=5, tweet_mode='extended')
        return [{'text': tweet.full_text, 'created_at': tweet.created_at} for tweet in tweets]
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return []

def fetch_facebook_posts(user_access_token):
    url = f"https://graph.facebook.com/me/posts"
    params = {
        'access_token': user_access_token,
        'fields': 'message,created_time'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        print("Facebook API Error:", response.json())
        return []


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully.")
        return redirect('login')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required
def dashboard_view(request):
    twitter_posts = fetch_tweets(username='your_twitter_username')  # or dynamically from user profile
    facebook_access_token = 'your_test_facebook_user_access_token'  # 🔁 Replace this with a valid token
    facebook_posts = fetch_facebook_posts(facebook_access_token)  # ✅ Correct

    context = {
        'twitter_posts': twitter_posts,
        'facebook_posts': facebook_posts
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


# Optional - only if you want to use /profile/
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
