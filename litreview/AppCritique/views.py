
from django.core.paginator import Paginator
from itertools import chain
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import CharField, Value
from django.shortcuts import render, redirect

from .forms import SignupForm
from .models import Ticket, Review, UserFollows, CustomUser
from django.shortcuts import get_object_or_404
from .forms import TicketForm, ReviewForm
import logging
logger = logging.getLogger(__name__)


# ======================================================
# PAGE D'ACCUEIL
# ======================================================

def home(request):
    return render(
        request,
        'AppCritique/home.html'
    )

# ======================================================
# INSCRIPTION
# ======================================================


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
        else:
            logger.debug(form.errors)  
    else:
        form = SignupForm()
    return render(
        request,
        'AppCritique/signup.html',
        {'form': form}
    )
# ======================================================
# CONNEXION
# ======================================================

class CustomLoginView(LoginView):
    template_name = 'AppCritique/login.html'

# ======================================================
# DECONNEXION
# ======================================================

def logout_view(request):
    logout(request)
    return redirect('login')

# ======================================================
# FEED
# ======================================================

@login_required
def feed(request):

    followed_users = UserFollows.objects.filter(
        user=request.user
    ).values_list(
        'followed_user',
        flat=True
    )
    tickets = Ticket.objects.filter(
        user__in=followed_users
    )
    reviews = Review.objects.filter(
        user__in=followed_users
    )
    # Tickets des abonnements + les miens
    tickets = (
     Ticket.objects.filter(
        user__in=followed_users
     ).annotate(content_type=Value('TICKET', output_field=CharField())) |
     Ticket.objects.filter(
        user=request.user
     ).annotate(content_type=Value('TICKET', output_field=CharField()))
    )

    # Reviews des abonnements
    # + mes reviews
    # + reviews faites sur mes tickets
    reviews = Review.objects.filter(
        user__in=followed_users
    ).annotate(content_type=Value('REVIEW', output_field=CharField())) | Review.objects.filter(
        user=request.user
    ).annotate(content_type=Value('REVIEW', output_field=CharField())) | Review.objects.filter(
        ticket__user=request.user
    ).annotate(content_type=Value('REVIEW', output_field=CharField()))
    posts = sorted(
    chain(tickets, reviews),
    key=lambda post: post.time_created,
    reverse=True
)
    
    # PAGINATION
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'AppCritique/feed.html',
        {
            'posts': page_obj,
            'page_obj': page_obj
        }
    )

# ======================================================
# CREER TICKET
# ======================================================

@login_required
def create_ticket(request):

    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(
            request.POST,
            request.FILES
        )
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Ticket créé avec succès !')
            return redirect('feed')
    return render(
        request,
        'AppCritique/create_ticket.html',
        {'form': form}
    )

# ======================================================
# CREER REVIEW
# ======================================================

@login_required
def create_review(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )

    # Empêche plusieurs critiques
    existing_review = Review.objects.filter(
        ticket=ticket,
        user=request.user
    ).exists()

    if existing_review:
        return redirect('feed')
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, 'Critique créée avec succès !')
            return redirect('feed')
    return render(
        request,
        'AppCritique/create_review.html',
        {
            'form': form,
            'ticket': ticket
        }
    )


# ======================================================
# CREER TICKET + REVIEW
# ======================================================

@login_required
def create_ticket_review(request):

    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == 'POST':
        ticket_form = TicketForm(
            request.POST,
            request.FILES
        )
        review_form = ReviewForm(
            request.POST
        )

        if (
            ticket_form.is_valid()
            and review_form.is_valid()
        ):
            ticket = ticket_form.save(
                commit=False
            )
            ticket.user = request.user
            ticket.save()
            review = review_form.save(
                commit=False
            )

            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, 'Ticket et critique créés avec succès !')
            return redirect('feed')

    return render(
        request,
        'AppCritique/create_ticket_review.html',
        {
            'ticket_form': ticket_form,
            'review_form': review_form
        }
    )


# ======================================================
# POSTS UTILISATEUR
# ======================================================

@login_required
def posts(request):
    tickets = Ticket.objects.filter(
        user=request.user
    )
    reviews = Review.objects.filter(
        user=request.user
    )
    tickets = tickets.annotate(
        content_type=Value(
            'TICKET',
            CharField()
        )
    )
    reviews = reviews.annotate(
        content_type=Value(
            'REVIEW',
            CharField()
        )
    )
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(
        request,
        'AppCritique/posts.html',
        {'posts': posts}
    )

# ======================================================
# MODIFIER TICKET
# ======================================================

@login_required
def update_ticket(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )
    if ticket.user != request.user:

        return redirect('feed')
    form = TicketForm(
        instance=ticket
    )
    if request.method == 'POST':
        form = TicketForm(
            request.POST,
            request.FILES,
            instance=ticket
        )
        if form.is_valid():
            messages.success(request, 'Ticket modifié avec succès !')
            form.save()
            return redirect('posts')
    return render(
        request,
        'AppCritique/update_ticket.html',
        {
            'form': form
        }
    )

# ======================================================
# MODIFIER REVIEW
# ======================================================

@login_required
def update_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id
    )
    if review.user != request.user:

        return redirect('feed')
    form = ReviewForm(
        instance=review
    )
    if request.method == 'POST':

        form = ReviewForm(
            request.POST,
            instance=review
        )
        if form.is_valid():
            messages.success(request, 'Critique modifiée avec succès !')
            form.save()
            return redirect('posts')
    return render(
        request,
        'AppCritique/update_review.html',
        {
            'form': form,
            'ticket': review.ticket
        }
    )

# ======================================================
# SUPPRIMER TICKET
# ======================================================

@login_required
def delete_ticket(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )
    if ticket.user == request.user:
        ticket.delete()
        messages.success(request, 'Ticket supprimé avec succès !')
    return redirect('posts')

# ======================================================
# SUPPRIMER REVIEW
# ======================================================

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id
    )
    if review.user == request.user:
        review.delete()
        messages.success(request, 'Critique supprimée avec succès !')
    return redirect('posts')

# ======================================================
# ABONNEMENTS
# ======================================================

@login_required
def subscriptions(request):
    if request.method == 'POST':
        username = request.POST.get(
            'followed_user'
        )
        # Vérifie que le champ n'est pas vide
        if username:
            username = username.strip()
            try:
                followed_user = CustomUser.objects.get(
                    username=username
                )
                # Empêche de se suivre soi-même
                if followed_user != request.user:

                    UserFollows.objects.get_or_create(
                        user=request.user,
                        followed_user=followed_user
                    )
                    messages.success(
                        request,
                        f'Vous suivez maintenant {username}'
                    )
                else:
                    messages.error(
                        request,
                        "Vous ne pouvez pas vous suivre vous-même."
                    )
            except CustomUser.DoesNotExist:
                messages.error(
                    request,
                    "Utilisateur introuvable."
                )
        return redirect('subscriptions')

    # Recharge après ajout
    follows = UserFollows.objects.filter(
        user=request.user
    )
    followers = UserFollows.objects.filter(
        followed_user=request.user
    )
    return render(
        request,
        'AppCritique/subscriptions.html',
        {
            'follows': follows,
            'followers': followers
        }
    )

# ======================================================
# DESABONNER
# ======================================================

@login_required
def unfollow_user(request, follow_id):
    follow = get_object_or_404(
        UserFollows,
        id=follow_id
    )
    if follow.user == request.user:
        follow.delete()
    return redirect('subscriptions')