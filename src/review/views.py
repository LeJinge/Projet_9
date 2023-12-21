import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from src.review.forms import TicketForm


# Create your views here.
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