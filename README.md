# ab_testing
AB testing app written in Python and Flask 

## Introduction
Ce code permet de tester plusieurs versions d'une variable ou d'un contenu et de déterminer à l'aide de graphiques laquelle des versions est la meilleure.   


### Context
Aujourd'hui, de nombreuses entreprises effectuent des tests A/B afin d'améliorer le contenu de leur site web ou même de leur application. Les tests réalisés peuvent aussi bien se faire sur la couleur d'un bouton, l'emplacement d'une image ou encore la façon d'afficher les titres des publicités sur un site web. 

### Présentation
Pour pouvoir faire de l'A/B testing il faut au minimum deux versions d'une variable à comparer et des utilisateurs qui effectueront le test. Elle peut aussi bien être menée sur un site internet ou une application mobile (par exemple). Le test A/B permettra de tester une hypothèse en la comparant avec ce qui existe déja.

## Installation
- Installation de python3 https://www.python.org/downloads/
- Installation de flask ( pour plus d'informations : https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- Installation de Flask-SQLAlchemy : (venv) $ pip install flask-sqlalchemy



## Usage 

Pour la mise à jour de votre base de données à chaque fois que vous apportez une modification dans celle ci ou que l'application se développe, il est nécessaire d'installer une extention Flask. 
- Installation de Flask-Migrate :  (venv) $ pip install flask-migrate
Pour générer le script de migration, il suffit de saisir sur le terminal : 
(venv)$flask db init
(venv) $ flask db migrate -m "users table"

Pour appliquer les modifications à la base de données, il suffit d'utiliser la commande suivante : (venv) $ flask db upgrade

