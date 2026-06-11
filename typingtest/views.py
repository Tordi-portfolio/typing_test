import json
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import TypingTest

# Word lists by difficulty
EASY_WORDS = [
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
    'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
    'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
    'people', 'year', 'work', 'back', 'use', 'two', 'way', 'could', 'them', 'see',
    'first', 'because', 'over', 'such', 'even', 'most', 'made', 'before', 'through', 'think',
    'where', 'much', 'these', 'than', 'then', 'now', 'look', 'only', 'come', 'been',
    'day', 'did', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new',
    'now', 'old', 'our', 'out', 'own', 'said', 'see', 'she', 'too', 'way',
    'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'
]

MEDIUM_WORDS = [
    'about', 'ability', 'absolute', 'accept', 'according', 'account', 'achieve', 'across',
    'action', 'activity', 'actually', 'address', 'administration', 'affect', 'after', 'again',
    'agency', 'agenda', 'agreement', 'agriculture', 'ahead', 'although', 'always', 'american',
    'among', 'amount', 'analysis', 'analyze', 'ancient', 'animal', 'another', 'answer',
    'anybody', 'anyone', 'anything', 'anywhere', 'apartment', 'apparent', 'appeal', 'appear',
    'appearance', 'application', 'apply', 'approach', 'appropriate', 'approval', 'april', 'approach',
    'architect', 'architecture', 'argument', 'around', 'arrangement', 'arrest', 'arrival', 'arrive',
    'arrow', 'article', 'artist', 'artistic', 'aspect', 'assault', 'assembly', 'asset',
    'assignment', 'assistance', 'assistant', 'associate', 'association', 'assume', 'assumption', 'assurance',
    'atmosphere', 'attach', 'attack', 'attempt', 'attend', 'attendance', 'attention', 'attitude',
    'attorney', 'attract', 'attraction', 'attractive', 'audience', 'august', 'authority', 'available',
    'avenue', 'average', 'aviation', 'awareness', 'balance', 'balloon', 'bandwidth', 'banking',
    'basketball', 'battery', 'battlefield', 'beautiful', 'because', 'become', 'bedroom', 'behavior',
    'believe', 'benefit', 'beside', 'between', 'beyond', 'bicycle', 'billion', 'biology',
    'birthday', 'biscuit', 'bitter', 'bizarre', 'blanket', 'blocking', 'bluetooth', 'boarding'
]

HARD_WORDS = [
    'abdicate', 'abhor', 'abscond', 'absolve', 'abstain', 'abstruse', 'accidental', 'accommodate',
    'accomplice', 'acculturate', 'acetaminophen', 'acknowledge', 'acquiesce', 'acquiescence', 'acrophobia', 'acropolis',
    'actualize', 'acuity', 'adage', 'adamant', 'addendum', 'adequate', 'adhere', 'adherent',
    'adjacent', 'adjudicate', 'adjunct', 'adjuration', 'adjutant', 'administer', 'admissible', 'admissive',
    'adolescence', 'adolescent', 'admonish', 'admonition', 'adobe', 'adolescent', 'adoption', 'adorable',
    'adoration', 'adoring', 'adorn', 'adornment', 'adrenaline', 'adrift', 'adsorb', 'adsorption',
    'adulation', 'adulatory', 'adulterate', 'adulteration', 'adultery', 'advancement', 'advantage', 'advent',
    'adventure', 'adventurer', 'adventurous', 'adverb', 'adversary', 'adverse', 'adversity', 'advertise',
    'advertisement', 'advertising', 'advice', 'advisability', 'advisable', 'advise', 'adviser', 'advisor',
    'advisory', 'advocacy', 'advocate', 'aesthete', 'aesthetic', 'aesthetics', 'affability', 'affable',
    'affair', 'affectation', 'affected', 'affectedly', 'affecting', 'affection', 'affectionate', 'affectioned',
    'affidavit', 'affiliate', 'affiliation', 'affinity', 'affirm', 'affirmation', 'affirmative', 'affix',
    'afflatus', 'afflict', 'affliction', 'affluence', 'affluent', 'affront', 'afghani', 'afield',
    'afire', 'aflame', 'afloat', 'afoot', 'aforementioned', 'aforesaid', 'aforethought', 'afraid',
    'afresh', 'african', 'afrikaans', 'aft', 'after', 'aftermath', 'aftermost', 'afternoon'
]

def get_words_by_difficulty(difficulty, num_words=50):
    """Get word list based on difficulty level"""
    if difficulty == 'easy':
        word_list = EASY_WORDS
    elif difficulty == 'hard':
        word_list = HARD_WORDS
    else:  # medium
        word_list = MEDIUM_WORDS
    
    return ' '.join(random.choices(word_list, k=num_words))

def index(request):
    """Home page with typing test"""
    difficulty = request.GET.get('difficulty', 'medium')
    test_words = get_words_by_difficulty(difficulty, 50)
    recent_tests = []
    
    if request.user.is_authenticated:
        recent_tests = TypingTest.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'test_words': test_words,
        'difficulty': difficulty,
        'recent_tests': recent_tests
    }
    return render(request, 'typingtest/index.html', context)

@require_http_methods(["POST"])
@csrf_protect
def calculate_score(request):
    """Calculate WPM, accuracy, and store results"""
    try:
        data = json.loads(request.body)
        original_text = data.get('original_text', '').strip()
        typed_text = data.get('typed_text', '').strip()
        time_taken = int(data.get('time_taken', 0))
        difficulty = data.get('difficulty', 'medium')
        
        if time_taken == 0:
            return JsonResponse({'error': 'Invalid time'}, status=400)
        
        # Calculate errors
        errors = 0
        for i in range(max(len(typed_text), len(original_text))):
            if i >= len(original_text) or i >= len(typed_text):
                errors += 1
            elif typed_text[i] != original_text[i]:
                errors += 1
        
        # Calculate WPM (words per minute)
        words_typed = len(typed_text.split())
        wpm = (words_typed / time_taken) * 60 if time_taken > 0 else 0
        
        # Calculate accuracy
        total_chars = len(original_text)
        accuracy = ((total_chars - errors) / total_chars * 100) if total_chars > 0 else 0
        accuracy = max(0, min(100, accuracy))
        
        # Store result if user is logged in
        if request.user.is_authenticated:
            TypingTest.objects.create(
                user=request.user,
                difficulty=difficulty,
                words=original_text,
                wpm=round(wpm, 2),
                accuracy=round(accuracy, 2),
                errors=errors,
                time_taken=time_taken
            )
        
        return JsonResponse({
            'wpm': round(wpm, 2),
            'accuracy': round(accuracy, 2),
            'errors': errors,
            'time_taken': time_taken
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required(login_url='login')
def results(request):
    """Display user's typing test results"""
    difficulty_filter = request.GET.get('difficulty', 'all')
    
    if difficulty_filter == 'all':
        tests = TypingTest.objects.filter(user=request.user).order_by('-created_at')
    else:
        tests = TypingTest.objects.filter(user=request.user, difficulty=difficulty_filter).order_by('-created_at')
    
    # Calculate stats
    if tests:
        avg_wpm = sum([test.wpm for test in tests]) / len(tests)
        avg_accuracy = sum([test.accuracy for test in tests]) / len(tests)
        best_wpm = max([test.wpm for test in tests])
    else:
        avg_wpm = 0
        avg_accuracy = 0
        best_wpm = 0
    
    # Get stats by difficulty
    all_tests = TypingTest.objects.filter(user=request.user)
    easy_tests = all_tests.filter(difficulty='easy')
    medium_tests = all_tests.filter(difficulty='medium')
    hard_tests = all_tests.filter(difficulty='hard')
    
    easy_avg_wpm = sum([t.wpm for t in easy_tests]) / len(easy_tests) if easy_tests else 0
    medium_avg_wpm = sum([t.wpm for t in medium_tests]) / len(medium_tests) if medium_tests else 0
    hard_avg_wpm = sum([t.wpm for t in hard_tests]) / len(hard_tests) if hard_tests else 0
    
    context = {
        'tests': tests,
        'avg_wpm': round(avg_wpm, 2),
        'avg_accuracy': round(avg_accuracy, 2),
        'best_wpm': round(best_wpm, 2),
        'total_tests': len(all_tests),
        'difficulty_filter': difficulty_filter,
        'easy_tests_count': len(easy_tests),
        'medium_tests_count': len(medium_tests),
        'hard_tests_count': len(hard_tests),
        'easy_avg_wpm': round(easy_avg_wpm, 2),
        'medium_avg_wpm': round(medium_avg_wpm, 2),
        'hard_avg_wpm': round(hard_avg_wpm, 2),
    }
    return render(request, 'typingtest/results.html', context)

def new_test(request):
    """Generate a new typing test"""
    difficulty = request.GET.get('difficulty', 'medium')
    test_words = get_words_by_difficulty(difficulty, 50)
    return JsonResponse({'words': test_words, 'difficulty': difficulty})

@csrf_protect
def register(request):
    """User registration with validation"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        errors = []
        
        if not username:
            errors.append('Username is required.')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        elif len(username) > 150:
            errors.append('Username must be less than 150 characters.')
        elif not username.isalnum() and '_' not in username and '-' not in username:
            errors.append('Username can only contain letters, numbers, underscores, and hyphens.')
        elif User.objects.filter(username=username).exists():
            errors.append('This username is already taken.')
        
        if email and User.objects.filter(email=email).exists():
            errors.append('This email is already registered.')
        
        if not password:
            errors.append('Password is required.')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        elif not any(char.isupper() for char in password):
            errors.append('Password must contain at least one uppercase letter.')
        elif not any(char.isdigit() for char in password):
            errors.append('Password must contain at least one number.')
        
        if password != password_confirm:
            errors.append('Passwords do not match.')
        
        if errors:
            context = {
                'errors': errors,
                'username': username,
                'email': email
            }
            return render(request, 'typingtest/register.html', context)
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            messages.success(request, f'Welcome {username}! Your account has been created successfully.')
            return redirect('index')
        
        except Exception as e:
            errors.append(f'An error occurred: {str(e)}')
            context = {
                'errors': errors,
                'username': username,
                'email': email
            }
            return render(request, 'typingtest/register.html', context)
    
    return render(request, 'typingtest/register.html')

@csrf_protect
def login_view(request):
    """User login with validation"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        errors = []
        
        if not username:
            errors.append('Username is required.')
        if not password:
            errors.append('Password is required.')
        
        if errors:
            context = {'errors': errors, 'username': username}
            return render(request, 'typingtest/login.html', context)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            next_page = request.GET.get('next', 'index')
            return redirect(next_page)
        else:
            errors.append('Invalid username or password.')
            context = {'errors': errors, 'username': username}
            return render(request, 'typingtest/login.html', context)
    
    return render(request, 'typingtest/login.html')

def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

@login_required(login_url='login')
def leaderboard(request):
    """Display global leaderboard"""
    difficulty = request.GET.get('difficulty', 'all')
    
    if difficulty == 'all':
        tests = TypingTest.objects.values('user__username').annotate(
            avg_wpm=models.Avg('wpm'),
            avg_accuracy=models.Avg('accuracy'),
            test_count=models.Count('id')
        ).filter(test_count__gte=1).order_by('-avg_wpm')[:20]
    else:
        tests = TypingTest.objects.filter(difficulty=difficulty).values('user__username').annotate(
            avg_wpm=models.Avg('wpm'),
            avg_accuracy=models.Avg('accuracy'),
            test_count=models.Count('id')
        ).filter(test_count__gte=1).order_by('-avg_wpm')[:20]
    
    context = {
        'tests': tests,
        'difficulty': difficulty
    }
    return render(request, 'typingtest/leaderboard.html', context)