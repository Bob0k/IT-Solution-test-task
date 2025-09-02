import random

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import QuoteItem
from .forms import QuoteForm, SourceForm

def landing(request):
    return redirect('index')

def get_random_quote():
    total_weight = QuoteItem.objects.aggregate(sum=Sum('weight'))['sum']
    random_val = random.uniform(0, total_weight)
    cumulative = 0
    for quote in QuoteItem.objects.all():
        cumulative += quote.weight
        
        if random_val <= cumulative:
            return quote

@require_POST
@csrf_exempt
def like_quote(request):
    quote_id = int(request.body)
    changed_opinion = False
    if quote_id < 0:
        quote_id *= -1
        changed_opinion = True

    quote = get_object_or_404(QuoteItem, id=quote_id)

    quote.likes += 1
    quote.dislikes -= 1 if changed_opinion else 0
    quote.save()
    
    print("liked ", quote, request.body)
    return JsonResponse({
        'success': True
    })

@require_POST
@csrf_exempt
def dislike_quote(request):
    quote_id = int(request.body)
    changed_opinion = False
    if quote_id < 0:
        quote_id *= -1
        changed_opinion = True

    quote = get_object_or_404(QuoteItem, id=quote_id)

    quote.dislikes += 1
    quote.likes -= 1 if changed_opinion else 0
    quote.save()
    
    print("disliked ", quote, request.body)
    return JsonResponse({
        'success': True
    })

def add_quote(request):
    log = 'false'
    message = ''
    if request.method == 'POST':
        log = 'true'
        
        if 'name' in request.POST:
            form = SourceForm(request.POST)

        else:
            form = QuoteForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                message = 'Добавлено'

            except Exception as e:
                form.add_error(None, str(e))
    
    form = QuoteForm()
    
    return render(request, 'add.html', {'sourceform': SourceForm(),
                                        'quoteform': QuoteForm(),
                                        'log': log,
                                        'message': message})

# Create your views here.
def index(request):
    if request.method == 'POST':
        print("Hello")
        return
    
    item = get_random_quote()
    item.view_count += 1
    item.save()

    return render(request, "index.html", {"quote": item})

def board(request):
    items = QuoteItem.objects.all().order_by('-likes')[:10]

    return render(request, "board.html", {"quotes": items})
