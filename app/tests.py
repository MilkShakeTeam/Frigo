# coding=utf-8
import datetime
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase
from app.models import Product, Fridge, ProductFridge


class ProductMethodTests(TestCase):

    def test_need_to_eat_with_long_date(self):
        """
        need_to_eat() doit retourner False pour les produits dont la date est > à aujourd'hui + 3 jours
        """
        long_date_product = Product(exp_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(long_date_product.need_to_eat(), False)

    def test_need_to_eat_with_short_date(self):
        """
        need_to_eat() doit retourner True pour les produits dont la date est < à aujourd'hui + 3 jours
        """
        short_date_product = Product(exp_date=timezone.now() + datetime.timedelta(days=2))
        self.assertEqual(short_date_product.need_to_eat(), True)

    def test_need_to_eat_with_expired_date(self):
        """
        need_to_eat() doit retourner True pour les produits dont la date_exp est < maintenant
        """
        exp_date_product = Product(exp_date=timezone.now() - datetime.timedelta(days=5))
        self.assertEqual(exp_date_product.need_to_eat(), True)


# tests sur l'ajout de frigo
def create_fridge(owner, capacity):
    """
    Créer un frigo avec le nom du propriétaire et une capacité
    :param owner:       le nom du propriétaire
    :param capacity:    la capacité du frigo
    :rtype : Fridge
    """
    return Fridge.objects.create(owner=owner, capacity=capacity)


def create_product(name, exp_date):
    """
    Créer un produit avec un nom et une date de péremption
    :param name:      le nom du produit
    :param exp_date:  la date de péremption du produit
    :rtype : Product
    """
    return Product.objects.create(name=name, exp_date=exp_date)


def create_product_fridge(fridge, product, quantity, unit):
    """
    Créer un ProductFridge avec un frigo, un produit, une quantité et une unité
    :param fridge:  le frigo concerné
    :param product: le produit concerné
    :param quantity:la quantité du prduit
    :param unit:    l'unité de la quantité
    :rtype : ProductFridge
    """
    return ProductFridge.objects.create(product=product, fridge=fridge,
                                        quantity=quantity, unit=unit)


class FridgeViewTests(TestCase):
    def test_index_view_with_no_fridge(self):
        """
        Si aucun frigo n'existe, un message doit être affiché
        """
        response = self.client.get(reverse('app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aucun frigo")
        self.assertQuerysetEqual(response.context['fridges'], [])

    def test_index_view_with_an_empty_fridge(self):
        """
        Les frigos sans produits doivent quand même être affiché sur la page d'accueil
        """
        fridge = create_fridge(owner="empty", capacity=-100)
        response = self.client.get(reverse('app:index'))
        self.assertContains(response, "Frigo vide")
        self.assertQuerysetEqual(response.context['fridges'][fridge.id]['products'], [])

    def test_index_view_with_products_in_fridge(self):
        """
        Les frigos contenant des produits doivent être affichés
        """
        fridge = create_fridge(owner="withProduct", capacity=100)
        product = create_product(name="product", exp_date=timezone.now())
        create_product_fridge(fridge=fridge, product=product, quantity=2, unit='g')
        response = self.client.get(reverse('app:index'))
        self.assertNotContains(response, "Frigo vide", status_code=200)
        self.assertTrue(fridge.id in response.context['fridges'])
