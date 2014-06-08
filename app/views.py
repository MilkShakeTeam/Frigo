# coding=utf-8
import datetime
from django.http import HttpResponseRedirect
from app.forms import AddProductForm, AddFridgeForm
from app.models import Fridge, Product, ProductFridge
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse


def index(request):
    """
    Affiche l'ensemble des frigos avec leurs produits
    :param request:
    :return: index.html
    """
    fridges = Fridge.objects.with_products()
    context = {
        'fridges': fridges,
        'form': AddFridgeForm,
    }
    return render(request, 'app/index.html', context)


def detail(request, fridge_id):
    """
    Récupère les produits d'un frigo en particulier et affiche un formulaire d'ajout
    :param request:
    :param fridge_id: l'identifiant du frigo désiré
    :return: detail.html
    :raise Http404: si le frigo n'a pas été trouvé
    """
    try:
        # Récupération du frigo et de ces produits
        fridge_id = int(fridge_id)
        fridge = Fridge.objects.with_products(fridge_id)
    except Fridge.DoesNotExist:
        raise Http404
    # Récupération du formulaire
    form = AddProductForm()
    return render(request, 'app/detail.html', {
        'fridge': fridge,
        'form': form,
    })


def add_product(request, fridge_id):
    """
    Ajoute un produit à un frigo
    :param request:
    :param fridge_id: l'identifiant du frigo voulu
    :return: detail.html
    :raise Http404: si le frigo n'a été trouvé
    """
    # Vérification de l'existence du frigo
    fridge = get_object_or_404(Fridge, pk=fridge_id)

    if request.method == 'POST':
        # Récupération des informations du formulaire
        form = AddProductForm(request.POST)
        if form.is_valid():
            try:
                # Récupération des données envoyées en POST
                product_name = request.POST['name']
                product_exp_date = request.POST['expdate']
                product_quantity = request.POST['quantity']
                product_unit = request.POST['unit']
            except KeyError:
                # Si un index n'a pas été trouvé : renvoi l'utilisateur vers detail.html
                return render(request, 'app/detail.html', {
                    'fridge': Fridge.objects.with_products(fridge_id),
                    'form': form
                })

            else:
                # Création du nouveau produit avec les informations reçues
                new_product = Product(name=product_name,
                                      exp_date=datetime.datetime.strptime(product_exp_date, "%d/%m/%Y"))
                new_product.save()
                # Création de la ligne de liaison avec le produit, le frigo et les informaitons reçues
                new_productfridge = ProductFridge(fridge=fridge, product=new_product,
                                                  quantity=product_quantity, unit=product_unit)
                new_productfridge.save()
                # Redirect vers la même page : detail.html
                return HttpResponseRedirect(reverse('app:detail', args=(fridge_id,)))
        else:
            # En cas de non validation du formulaire : renvoi vers detail.html
            return render(request, 'app/detail.html', {
                'fridge': Fridge.objects.with_products(fridge_id),
                'form': form
            })


def delete_product(request, fridge_id, product_id):
    """
    Supprime un produit d'un frigo
    :param request:
    :param fridge_id: l'identifiant du frigo concernée
    :param product_id: l'identifiant du produit concerné
    :return: detail.html
    :raise Http404: si le frigo, le produit ou la ligne de liaison n'a pas été trouvé
    """
    # Récupération des trois objets
    fridge = get_object_or_404(Fridge, pk=fridge_id)
    product = get_object_or_404(Product, pk=product_id)
    fridge_product = get_object_or_404(ProductFridge, product=product, fridge=fridge)
    # Suppression de la ligne de liaison
    fridge_product.delete()

    return render(request, 'app/detail.html', {
        'fridge': Fridge.objects.with_products(fridge_id),
        'form': AddProductForm(),
    })


def add_fridge(request):
    """
    Ajoute un frigo
    """
    if request.method == 'POST':
        # Récupération des informations du formulaire
        form = AddFridgeForm(request.POST)
        if form.is_valid():
            try:
                # Récupération des données envoyées en POST
                fridge_owner = request.POST['owner']
                fridge_capacity = request.POST['capacity']
            except KeyError:
                # Si un index n'a pas été trouvé : renvoi l'utilisateur vers detail.html
                return render(request, 'app/index.html', {
                    'fridges': Fridge.objects.with_products(),
                    'form': AddFridgeForm,
                    'error_message': 'Probleme lors du traitement du formulaire !',
                })
            else:
                # Création du nouveau frigo avec les informations reçues
                new_fridge = Fridge(owner=fridge_owner, capacity=fridge_capacity)
                new_fridge.save()

                # Redirect vers la même page : index.html
                return HttpResponseRedirect(reverse('app:index'))
        else:
            # En cas de non validation du formulaire : renvoi vers index.html
            return render(request, 'app/index.html', {
                'fridges': Fridge.objects.with_products(),
                'form': form,
                'error_message': 'Formulaire incomplet !'
            })

