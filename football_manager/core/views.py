from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Player, MatchPerformance, Product
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, PlayerForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse

# Home View
def home(request):
    return render(request, 'core/home.html')

# Shop View
def shop(request):
    return render(request, 'core/shop.html')

# About Us View
def about_us(request):
    return render(request, 'core/about.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

# Sign Up View
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

# View to display all players
@login_required
def player_list(request):
    query = request.GET.get('q', '')
    team = request.GET.get('team', '')
    position = request.GET.get('position', '')

    players = Player.objects.all()

    if query:
        players = players.filter(name__icontains=query)
    if team:
        players = players.filter(team__icontains=team)
    if position:
        players = players.filter(position__icontains=position)

    paginator = Paginator(players, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # For dropdown filter options
    teams = Player.objects.values_list('team', flat=True).distinct()
    positions = Player.objects.values_list('position', flat=True).distinct()

    context = {
        'page_obj': page_obj,
        'query': query,
        'team': team,
        'position': position,
        'teams': teams,
        'positions': positions,
    }

    return render(request, 'core/player_list.html', context)

# View to add a new player
@login_required
def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_list')  # Redirect to the player list after adding the player
    else:
        form = PlayerForm()
    
    return render(request, 'core/add_player.html', {'form': form})

def edit_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('player_list')
    else:
        form = PlayerForm(instance=player)
    return render(request, 'core/edit_player.html', {'form': form})

def delete_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    player.delete()
    return redirect('player_list')

@login_required
def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    performances = player.performances.order_by('date')

    labels = [perf.date.strftime('%b %d') for perf in performances]
    goals = [perf.goals for perf in performances]
    assists = [perf.assists for perf in performances]

    context = {
        'player': player,
        'labels': labels,
        'goals': goals,
        'assists': assists
    }
    return render(request, 'core/player_detail.html', context)

@login_required
def compare_players(request):
    # Get all players
    players_qs = Player.objects.all()

    # Get all distinct teams and positions
    teams = players_qs.values_list('team', flat=True).distinct()
    positions = players_qs.values_list('position', flat=True).distinct()

    # Get the selected filters
    team_filter = request.GET.get('team')
    position_filter = request.GET.get('position')
    query = request.GET.get('q', '')

    # Filter players based on selected filters
    if team_filter:
        players_qs = players_qs.filter(team=team_filter)
    if position_filter:
        players_qs = players_qs.filter(position=position_filter)
    if query:
        players_qs = players_qs.filter(name__icontains=query)

    # Get selected players (from the multiple select box)
    selected_players = request.GET.getlist('players')

    # Initialize error message
    error_message = None

    # Convert selected_players to integers (if any) for comparison
    selected_players = list(map(int, selected_players)) if selected_players else []

    # Check if compare button was clicked and validate selection
    if 'compare' in request.GET:
        if len(selected_players) < 2:
            error_message = "You must select 2 or more players to compare."

    # If selected players exist and no error, filter by those players
    if selected_players and not error_message:
        players = players_qs.filter(id__in=selected_players)
    else:
        players = players_qs

    # Extract the stats for the comparison chart
    names = [player.name for player in players] if players else []
    goals = [player.goals for player in players] if players else []
    assists = [player.assists for player in players] if players else []
    matches = [player.matches_played for player in players] if players else []

    context = {
        'players': players,
        'teams': teams,
        'positions': positions,
        'selected_players': selected_players,
        'names': names,
        'goals': goals,
        'assists': assists,
        'matches': matches,
        'team_filter': team_filter,
        'position_filter': position_filter,
        'query': query,
        'error_message': error_message,
    }

    return render(request, 'core/compare_players.html', context)

def product_list(request):
    category = request.GET.get('category', 'all')
    
    if category == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category=category)
    
    return render(request, 'core/product_list.html', {
        'products': products,
        'active_category': category
    })

def search_view(request):
    query = request.GET.get('query', '')
    if query:
        # Filter products based on the query (search term)
        products = Product.objects.filter(name__icontains=query)
    else:
        # If no query, show all products
        products = Product.objects.all()

    return render(request, 'your_template_name.html', {'products': products, 'query': query})

def shop_view(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', 'all')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category != 'all':
        products = products.filter(category=category)

    context = {
        'products': products,
        'category': category,
        'categories': CATEGORIES,
    }
    return render(request, 'core/shop.html', context)
