#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""
    Auteur: Daerlnaxe aka Alexandre CODOUL

    Date de création: 08/08/2017
    Dernière modif: 08/08/2017

    Version: Alpha 1.1

    commentaire: Pour les débutants, l'ayant été moi même il y a peu en Python et surtout en XML,
    beaucoup de lecture pour aboutir à lire des exemples très basiques et pas très clairs, jusqu'au moment ou je me suis décidé à lire
    tout le code d'etree pour mieux comprendre. Tout est liste, il faut donc comprendre qu'a chaque noeud on imbrique une liste, pas de dictionnaire
    pour permettre sans doute une construction aisée de cette arborescence quand les noeuds portent le même nom (dico = clé unique donc erreur si les clés sont similaires).
    De ce fait né en fait l'obligation pour parcourir de créer une fonction qui s'auto appelle tant qu'il y a quelque chose à parcourir. Et pour reproduire les effets
    de balise, à chaque lancement de cette fonction - a part pour les feuilles/fruits - on encadre de balises d'ouverture et fermeture.
    ElementTree ne liste apparement pas les commentaires, via XML.
    J'ai mis pas mal de commentaires pour permettre une bonne compréhension

"""

import sys
import xml.etree.ElementTree as etree


#======================= Fonction hors classe de xlml.etree  =============================

"""
    conversion via xml.etree
    d'une chaine xml en arbre puis l'affiche à l'écran et/ou renvoie une chaine formatée pour plus de lisibilité
    Note: Fonctionne avec un Element et non un ElementTree
    Note: N'oubliez pas de passer les switchs affich et formr selon ce que vous voulez faire sans quoi il ne se passera rien
"""
def conv_aff_xml( chaine_xml, affich=False, formr=False ):
    arbre = etree.XML(chaine_xml)   # === Construction d'un arbre via une chaine, c'est une fonction or classe de xml.etree
    if affich: affiche_xml( arbre )    # Forçage de l'affichage
    if formr:
        return form_xml( arbre )        # Formate une chaine


#======================= Fonction en rapport avec xml.etree.ElementTree =============================
"""
    Récupère la racine d'un ElementTree qui est un Element (comme un autre).
    De mémoire quand on parse un fichier xml il sort un ElementTree, et les deux classes n'ont pas souvent(jamais)
    de compatibilité sur leurs fonctions. l'ElementTree est un assemblage d'Element pour faire simple avec des fonctions intégrées.
    GetRoot ramène la racine de l'ElementTree mais ne signifie rien pour Element, la racine étant un Element comme un autre, et étant juste
    au début de la liste contenant toute l'arborescence.
    Note: N'oubliez pas de passer les switchs affich et formr selon ce que vous voulez faire sans quoi il ne se passera rien
"""
def aff_letree( elementTree, affich=False, formr=False ):
    elemracine = elementTree.getroot()
    if affich: affiche_xml( elemracine )
    if formr:
        return form_xml( elemracine )


"""
"""
def aff_element( element, affich=False, formr=False ):
    if affich: form_el( element, '' )
    #if formr: return form_xml( element)
# ==== fonctions communes

"""
    mise en forme des attributs
"""
def mf_attrs( attrs ):
    chaineattr=''
    for key, value in attrs():
        chaineattr += f" {key}='{value}'"

    return chaineattr

#======================= Fonctions en rapport avec xml.etree.Element =============================

"""
    renvoi de chaine formatée
"""
def form_xml( arbre ):
    chaiF = ''
    racine = arbre.tag

    chaiF += f'<{racine}>\n'
    chaiF += form_el(arbre, "")
    chaiF += f'</{racine}>\n'
    return chaiF

def form_el( node, marge):
    chaiF = ''

    for element in node:
    # === permet de savoir aussi si c'est une feuille ou une branche
        texte = getattr(element, 'text', None)

    # === Formatage des attributs
        attrs = getattr(element, 'items', None)
        chaineattr = mf_attrs( attrs )

    # === Mise en forme selon le cas
        marge += "\t"
    # --- Annulation des tabs et retours, générés par un précédent formatage sinon engendre des soucis
        if texte:
            texte = texte.replace('\t', '')
            texte = texte.replace('\n', '')

        if texte=='': texte = None

        # --- Cas d'une feuille
        if texte :
            chaiF += f'{marge}<{element.tag}{chaineattr}>{texte}</{element.tag}>\n'
        # --- Cas d'une branche
        else:
            chaiF += f'{marge}<{element.tag}{chaineattr}>\n'
            chaiF += form_el(element, marge)
            chaiF += f'{marge}</{element.tag}>\n'

        marge = marge.replace('\t', '', 1)

    return chaiF

# --- Affichage


"""
    affiche à l'écran en temps réel
"""
def affiche_xml( arbre ):
    racine = arbre.tag
    # --- On encadre de la racine avant de lancer tout le processus de parcours
    print(f'<{racine}>')
    affiche_el(arbre, "")
    print(f'</{racine}>')

"""
    Fonction qui s'auto appelle tant qu'il reste quelque chose à parcourir
"""
def affiche_el( node, marge ):
    print('node:', node.tag)
    for element in node:

    # === permet de savoir aussi si c'est une feuille ou une branche
        texte = getattr(element, 'text', None)

    # === Formatage des attributs
        attrs = getattr(element, 'items', None)
        chaineattr = mf_attrs( attrs )

    # === Mise en forme selon le cas
        marge += "\t"
    # --- Annulation des tabs et retours sinon engendre des soucis
        if texte:
            texte = texte.replace('\t', '')
            texte = texte.replace('\n', '')

        if texte=='': texte = None

        # --- Cas d'une feuille
        if texte :
            print( f'{marge}<{element.tag}{chaineattr}>{texte}</{element.tag}>' )
        # --- Cas d'une branche
        else:
            print('enfants')
            print(f'{marge}<{element.tag}{chaineattr}>')
            affiche_el(element, marge)
            print(f'{marge}</{element.tag}>')

        marge = marge.replace('\t', '', 1)
