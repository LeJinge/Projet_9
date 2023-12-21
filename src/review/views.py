import os
from itertools import chain
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Value, CharField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import TicketForm, ReviewForm
from src.review.models import Ticket, Review
from src.user.models import UserFollows


# Create your views here.
def user_feed_view(request):
    current_user = request.user
    followed_users_ids = UserFollows.objects.filter(user=current_user).values_list('followed_user', flat=True)

    tickets = Ticket.objects.filter(
        user__in=followed_users_ids
    ).prefetch_related('reviews') | Ticket.objects.filter(
        user=current_user
    ).prefetch_related('reviews')

    # Annotation pour vérifier si l'utilisateur courant a répondu
    tickets = tickets.annotate(
        user_has_responded=Exists(Review.objects.filter(ticket=OuterRef('pk'), user=current_user))
    )

    reviews = Review.objects.filter(
        user__in=followed_users_ids
    ).select_related('ticket') | Review.objects.filter(
        user=current_user
    ).select_related('ticket')

    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    combined_posts = sorted(
        chain(tickets, reviews),
        key=attrgetter('time_created'),
        reverse=True
    )

    return render(request, 'review/feed.html', {'posts': combined_posts, 'show_navbar': True})


@login_required
def create_ticket_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            # Enregistrer le ticket avec l'image originale
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # Renommer l'image si elle existe
            if 'image' in request.FILES:
                # Obtenir le chemin actuel de l'image
                current_image_path = ticket.image.path

                # Définir le nouveau nom de fichier
                new_file_name = f"{ticket.id}_{ticket.title.replace(' ', '_')}{os.path.splitext(ticket.image.name)[1]}"

                # Définir le nouveau chemin de fichier
                new_file_path = os.path.join('media/tickets', new_file_name)

                # Renommer le fichier dans le système de fichiers
                os.rename(current_image_path, new_file_path)

                # Mettre à jour le chemin de l'image dans l'objet ticket
                ticket.image = 'tickets/' + new_file_name
                ticket.save()

            return redirect('user_feed')
        else:
            print(form.errors)
    else:
        form = TicketForm()

    return render(request, 'review/create_ticket.html', {'form': form, 'show_navbar': True})


@login_required
def create_review_view(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.in_independent_review = True  # Mettre à jour l'attribut has_review
            ticket.save()
            # Renommer l'image si elle existe
            if 'image' in request.FILES:
                # Obtenir le chemin actuel de l'image
                current_image_path = ticket.image.path

                # Définir le nouveau nom de fichier
                new_file_name = f"{ticket.id}_{ticket.title.replace(' ', '_')}{os.path.splitext(ticket.image.name)[1]}"

                # Définir le nouveau chemin de fichier
                new_file_path = os.path.join('media/tickets', new_file_name)

                # Renommer le fichier dans le système de fichiers
                os.rename(current_image_path, new_file_path)

                # Mettre à jour le chemin de l'image dans l'objet ticket
                ticket.image = 'tickets/' + new_file_name
                ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.is_independent_review = True
            review.save()

            return redirect('user_feed')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
        'show_navbar': True,
    }
    return render(request, 'review/create_review.html', context)


@login_required
def create_review_response_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    # Vérifier si l'utilisateur a déjà répondu
    if ticket.has_user_response(request.user):
        messages.error(request, "Vous avez déjà répondu à ce ticket.")
        return redirect('user_feed')  # Ou une autre redirection appropriée

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('user_feed')  # Ou toute autre vue appropriée
    else:
        review_form = ReviewForm()

    return render(request, 'review/create_review_response.html', {'review_form': review_form, 'ticket': ticket})