from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

from models import UserFollows


def register_view(request):

    context = {
        'show_navbar': False
    }

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Vérifier si les mots de passe correspondent
        if password != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'user/register.html')

        # Vérifier si le nom d'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return render(request, 'user/register.html')

        # Si tout est bon, créez l'utilisateur
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Compte créé avec succès !")
        return redirect('login')

    return render(request, 'user/register.html', context)


def login_view(request):

    context = {
        'show_navbar': False
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Remplacer ceci par votre logique d'authentification
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Rediriger vers une page d'accueil ou de profil après une connexion réussie
            return redirect('user_feed')
        else:
            messages.error(request, "Adresse email ou mot de passe invalide.")

    return render(request, 'user/login.html', context)


@login_required
def subscription_view(request):
    utilisateur_actuel = request.user

    # Gestion des requêtes POST pour suivre ou se désabonner
    if request.method == 'POST':
        user_to_follow_id = request.POST.get('user_to_follow_id')
        user_to_unfollow_id = request.POST.get('user_to_unfollow_id')

        if user_to_follow_id:
            user_to_follow = get_object_or_404(User, pk=user_to_follow_id)
            if utilisateur_actuel != user_to_follow and not UserFollows.objects.filter(user=utilisateur_actuel, followed_user=user_to_follow).exists():
                UserFollows.objects.create(user=utilisateur_actuel, followed_user=user_to_follow)
                messages.success(request, f"Vous suivez maintenant {user_to_follow.username}.")
            else:
                messages.error(request, "Vous ne pouvez pas suivre cet utilisateur.")
        elif user_to_unfollow_id:
            user_to_unfollow = get_object_or_404(User, pk=user_to_unfollow_id)
            UserFollows.objects.filter(user=utilisateur_actuel, followed_user=user_to_unfollow).delete()
            messages.success(request, f"Vous ne suivez plus {user_to_unfollow.username}.")

        return redirect('subscription_view')  # Assurez-vous que 'subscription_view' est bien le nom défini dans urls.py pour cette vue

    # Gestion des requêtes GET pour afficher les abonnements et les abonnés
    utilisateurs_suivis = UserFollows.objects.filter(user=utilisateur_actuel).select_related('followed_user')
    abonnes = UserFollows.objects.filter(followed_user=utilisateur_actuel).select_related('user')

    # Gestion de la recherche d'utilisateurs
    query = request.GET.get('q')
    search_results = User.objects.filter(username__icontains=query).exclude(id=utilisateur_actuel.id) if query else None

    context = {
        'show_navbar': True,
        'utilisateurs_suivis': utilisateurs_suivis,  # Ceci est une liste de UserFollows objets
        'abonnes': abonnes,  # Ceci est également une liste de UserFollows objets
        'search_results': search_results  # Ceci est une liste de User objets
    }

    return render(request, 'user/subscription.html', context)



