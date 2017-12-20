#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Lefichier setup contient les fonctions qui vont installer votre packeges

"""
from setuptools import setup, find_packages
import centreon_bot_telegram

setup(
    # le nome de la bibliotheque tel qu'il apparaitra sur pipy
    name='centreon_bot_telegram',
    # la version du pacquet
    version=centreon_bot_telegram.__version__,
    # liste tous les pacquet a insérer des dans la diistribution
    # au lieu de la faire a la main on utilise la fonction (find_packages())
    # qui se fera recursivement dans le dossier courant
    packages=find_packages(),
    # nom de l'auteur
    author="Saint Fourier",
    # votre email sachant qu'il sera publier et public et visible pas tous le monde
    # avec les risque que ça implique
    author_email="fouriersaint@gmail.com",
    # coute description
    description="Bot telegram servant a voir les hosts et les services sur centreon",
    # long description sera affichier pour presenté la lib générale
    long_description=open('README.md').read(),
    all_reqs=open('requirements.txt').read(),
    # actoiver la prise en compte du fichier MENIFEST.in
    include_package_data=True,
    # une url qui pointe vers la page officiel de votre lib
    url="https://github.com/Fourier1/",
    download_url='https://github.com/Fourier1/CentreonTelegram.git',
    keywords='',
    # spécifier des regles pour le contenu
    classifiers=[
        "Programming Language :: Python",
        "Developpement Status :: 1 - Plannig",
        "Licence :: OSI Approved",
        "Natural Language :: Frensh",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Communication",
    ],

    # Pour creer un system de plugin
    # Pour creer une commande comme "django-admin"
    # Dans notre cas si on veu creer une commande tel que "centreon_bot_telegram-sm"
    # on a qu' a faire pointer ce nom vers la fonction proclame()
    # la syntaxe est la suivante : "nom-de-la-commande-a-creer = packeges.module.fonction"
    entry_points={
        'console_scripts': [
            'centreon_bot_telegram-sm = centreon_bot_telegram.centreon_telegram:start',
        ],
    },

    # A fournir uniquement si votre licence n'est pas listée dans "classivier"
    licence="WTFPL",

)
