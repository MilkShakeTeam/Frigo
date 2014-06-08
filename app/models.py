# coding=utf-8
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime
import locale
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8.')


class FridgeManager(models.Manager):
    """
    Permet de créer des requêtes personnalisées en rapport avec le modèle Fridge
    """

    def with_products(self, fridge_id=0):
        """
        Permet de récupérer l'ensemble des produits de frigos
        :rtype array:                           tableau structuré
        :param fridge_id:                       {optionnel} identifiant du frigo si un seul frigo n'est voulu
        :return: :raise Fridge.DoesNotExist:    si le frigo demandé n'existe pas
        """
        fridge_id = int(fridge_id)

        # Requête de récupération de tous les produits de tous les frigos avec les informations de la table de liaison
        fridges = Fridge.objects.all().values('productfridge__quantity',
                                          'productfridge__unit',
                                          'productfridge__product__name',
                                          'productfridge__product__id',
                                          'productfridge__product__exp_date',
                                          'owner', 'id').order_by('productfridge__product__exp_date')

        # Si fridge_id est passé, réstriction de la requête à ce frigo
        if fridge_id:
            fridges = fridges.filter(id=fridge_id)

        # Création des datas à renvoyer sous la forme d'un tableau de frigo contenant un tableau de produit
        datas = {}
        for fridge in fridges:
            # Si le frigo n'a pas encore été traité : création de l'entrée dans le tableau
            if not fridge['id'] in datas:
                datas[fridge['id']] = {
                    'id': fridge['id'],
                    'owner': str(fridge['owner']),
                    'products': []
                }

            # Si le frigo contient des produits; ajout d'une entrée dans le tableau de produit avec les informaitions
            if fridge['productfridge__product__id']:
                product = Product.objects.get(pk=fridge['productfridge__product__id'])
                datas[fridge['id']]['products'].append({
                    'id': fridge['productfridge__product__id'],
                    'name': fridge['productfridge__product__name'],
                    'exp_date': fridge['productfridge__product__exp_date'].strftime("%A %d %B %Y"),
                    'quantity': fridge['productfridge__quantity'],
                    'unit': fridge['productfridge__unit'],
                    'need_to_eat': product.need_to_eat(),
                })

        # Si l'on demande un frigo en particulier et que celui-ci n'est pas renseigné dans les datas : exception
        if not fridge_id in datas and fridge_id > 0:
            raise Fridge.DoesNotExist

        # Si l'on demande un frigo en particulier : retourne le tableau de l'index du frigo
        if fridge_id:
            return datas[fridge_id]
        else:
            return datas


class Product(models.Model):
    """
    Représente un produit, avec un nom et une date de peremption
    """
    name = models.CharField(max_length=200)
    exp_date = models.DateTimeField('expiration date')

    def __unicode__(self):
        """
        Retourne le produit sous forme de chaine de caractères
        :return: String de la forme nom - date de pérémption jour xx mois année
        """
        return self.name + ' - ' + self.exp_date.strftime("%A %d %B %Y")

    def need_to_eat(self):
        """
        Permet de savoir si un produit doit être mangé de façon urgente ou non, soit
        si sa date de peremption est passée ou dans les trois jours qui arrivent
        :return: bool   True si le produit doit être consommé
        """
        return self.exp_date <= timezone.now() + datetime.timedelta(days=3)
    need_to_eat.boolean = True
    need_to_eat.short_description = 'Need to eat it ?'


class Fridge(models.Model):
    """
    Représente un frigo avec un propriétaire, une capacité et une liste de produit
    """
    owner = models.CharField(max_length=200)
    capacity = models.IntegerField(default=0)
    products = models.ManyToManyField(Product, through='ProductFridge')
    #Surcharge de objects avec le manager
    objects = FridgeManager()

    def __unicode__(self):
        """
        Retourne le frigo sous forme de chaine de caractères
        :return: String de la forme propriétaire capacité
        """
        return str(self.owner) + ' ' + str(self.capacity)


class ProductFridge(models.Model):
    """
    Représente la table de liaison entre le frigo et le produit
    Contient les informations sur la quantité et l'unité du produit
    """
    product = models.ForeignKey(Product)
    fridge = models.ForeignKey(Fridge)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=10, default='g')

