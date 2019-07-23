from flask import render_template, flash, redirect, url_for, request, jsonify, abort, Markup
from app import app
from app import create
from app.forms import LoginForm, ExperienceForm
from app import models
from app import db
from math import *
import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scs
from sqlalchemy import func, text, update
import datetime







@app.route('/')
@app.route('/index')
def index():   
    return " A/B Testing "

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = ExperienceForm()
    if form.validate_on_submit():
        t = models.Testeur(nombre_classe=form.nombre_classe.data, nombre_utilisateur=form.nombre_utilisateur.data, nombre_jour=form.duree_test.data, parametre_teste=form.parametre_teste.data)
        db.session.add(t)
        db.session.commit()        
        return redirect(url_for('recap', id=t.id)) 

        
    return render_template('create.html',  title='Experience', form=form)



@app.route('/recap/<id>')
def recap(id):
    t = models.Testeur.query.get(id)
  
    
    
   
    #incoherence dans les chiffres, total individu et total_succes_etc




    return render_template('recap.html',  class_number=t.nombre_classe, user_number=t.nombre_utilisateur, day_number=t.nombre_jour, tested_param=t.parametre_teste )


@app.route('/graph/<id>')
def graph(id):
    t=models.Testeur.query.get(id)
    total_individu= db.session.query(models.Observation).filter(text("testeur_id=:value")).params(value=id).count()
    print(f"total_individu : {total_individu}")
    #total_individu_challenger=db.session.query(models.Observation).filter(text("testeur_id=:value and classe_renvoyee=:valeur1")).params(value=id, valeur1=2).count()
    #print(f"total_individu_challenger : {total_individu_challenger}")
    #total_individu_controller=db.session.query(models.Observation).filter(text("testeur_id=:value and classe_renvoyee=:valeur2")).params(value=id,valeur2=1).count()
    #print(f"total_individu_controller : {total_individu_controller}")
    total_succes_controller=db.session.query(models.Observation).filter(text("testeur_id=:testeur_id and classe_renvoyee=:classe_renvoyee and feedback=:feedback")).params(testeur_id=id, classe_renvoyee=1, feedback=1).count()
    total_succes_challenger=db.session.query(models.Observation).filter(text("testeur_id=:testeur_id and classe_renvoyee=:classe_renvoyee and feedback=:feedback")).params(testeur_id=id, classe_renvoyee=2, feedback=1).count()
    print(f"total_succes_controller : {total_succes_controller}")
    print(f"total_succes_challenger :  {total_succes_challenger}")
    
    
    total_succes_challenger_tmps=db.session.query(models.Observation.date_creation, func.count()).filter(text("testeur_id=:value and classe_renvoyee=:valeur1 and feedback=1")).params(value=id, valeur1=2).group_by(
         func.extract('second', models.Observation.date_creation)).all()
    
    print(f"total_succes_challenger_tmps : {total_succes_challenger_tmps}")
    print("\n\n")
    print("\n\n")

    total_succes_controller_tmps=db.session.query(models.Observation.date_creation, func.count()).filter(text("testeur_id=:value and classe_renvoyee=:valeur1 and feedback=1")).params(value=id, valeur1=1).group_by(
         func.extract('second', models.Observation.date_creation)).all()

    print(f"total_succes_controller_tmps: {total_succes_controller_tmps}")
    print("\n\n")
    print("\n\n")

    tableau_des_temps1, tableau_succes_challenger = zip(*total_succes_challenger_tmps[1:])
    tableau_des_temps2, tableau_succes_controller = zip(*total_succes_controller_tmps[1:]) 
    #Permet de recuperer dans chacun des tableaux le temps et le nombre de succes     
 
    tableau_temps_challenger = [t.strftime("%-S") for t in tableau_des_temps1] #recupère le temps pour le challenger
    tableau_temps_controller = [t.strftime("%-S") for t in tableau_des_temps2] #recupère le temps pour le controller

    all_temps = sorted(list(set(tableau_des_temps1 + tableau_des_temps2)))#creation d'une liste triée ayant les temps de chacun des groupes
    map_challenger = dict(total_succes_challenger_tmps[1:])
    map_controller = dict(total_succes_controller_tmps[1:])
   

    data_controller = []
    data_challenger = []
    for temps in all_temps:
        data_challenger.append(map_challenger.get(temps, 0)) #si la seconde cherchée est présénte dans le tableau alors on stocke la valeur sinon on  stocke 0
        data_controller.append(map_controller.get(temps, 0)) #idem

    all_temps = [elt.strftime("%-S") for elt in all_temps]

    #print(f"IsSame ==> {tableau_succes_challenger == tableau_succes_controller}")

    print(f"data_challenger :  {data_challenger}")
    print("\n\n")
    print(f"data_contoller : {data_controller}")
    print("\n\n")
    print(f"all_temps : {all_temps}")

    return render_template('graph.html', 
    labels=all_temps,
     data1=list(data_controller),
     data2=list(data_challenger))


@app.route('/attribution_classe/<id>')
def attribution_classe(id):
    t=models.Testeur.query.get(id)
    
    classe_int = random.randint(1,t.nombre_classe)
    date=datetime.datetime.now()
    #date_str=str(date)
    
    observation1=models.Observation(classe_renvoyee=classe_int, testeur_id=t.id, date_creation=date)
    db.session.add(observation1)
    db.session.commit()  

    return jsonify(
                    observation_id = observation1.id,
                    utilisateur = t.id, 
                    nombre_de_classe = t.nombre_classe, 
                    duree = t.nombre_jour,
                    classe_attribuee = classe_int,
                    nombre_utilisatur = t.nombre_utilisateur,
                    date_creation = date)
                    

@app.route('/observation/<id>', methods=["POST"])
def observation(id):    
    data = request.get_json()
    observation=models.Observation.query.get(id)
    if observation is None:
        abort(404)

    updated = models.Observation.query.filter_by(id=id).update({"feedback":data.get("feedback"), "date_feedback":datetime.datetime.now()})
    db.session.commit() 
    print(observation) 
    return jsonify(id_observation=observation.id,classe_renvoyee=observation.classe_renvoyee, feedback=observation.feedback, date_creation=observation.date_creation)
    

    
        
@app.route('/graphe2/<id>')
def graphe2(id):
    t=models.Testeur.query.get(id)
    total_individu= db.session.query(models.Observation).filter(text("testeur_id=:value")).params(value=id).count()
    #print(f"total_individu : {total_individu}")
    total_succes_controller=db.session.query(models.Observation).filter(text("testeur_id=:testeur_id and classe_renvoyee=:classe_renvoyee and feedback=:feedback")).params(testeur_id=id, classe_renvoyee=1, feedback=1).count()
    total_succes_challenger=db.session.query(models.Observation).filter(text("testeur_id=:testeur_id and classe_renvoyee=:classe_renvoyee and feedback=:feedback")).params(testeur_id=id, classe_renvoyee=2, feedback=1).count()
    #print(f"total_succes_controller : {total_succes_controller}")
    #print(f"total_succes_challenger :  {total_succes_challenger}")
    total_succes_controller_diff=db.session.query(models.Observation.date_creation, func.count()).filter(text("testeur_id=:value and classe_renvoyee=:valeur1 and feedback=1")).params(value=id, valeur1=1).group_by(
         func.extract('second', models.Observation.date_creation)-func.extract('second',models.Observation.date_feedback)).all()
    #print(f"total_succes_controller_diff : {total_succes_controller_diff}")
    total_succes_challenger_diff=db.session.query(models.Observation.date_creation, func.count()).filter(text("testeur_id=:value and classe_renvoyee=:valeur1 and feedback=1")).params(value=id, valeur1=2).group_by(
         func.extract('second', models.Observation.date_creation-func.extract('second', models.Observation.date_feedback))).all()
    #print(f"total_succes_challenger_diff : {total_succes_challenger_diff }")

    tableau_des_tempsChallenger, tableau_succes_challenger = zip(*total_succes_challenger_diff[1:])
    tableau_des_tempsController, tableau_succes_controller = zip(*total_succes_controller_diff[1:]) 
    #print(f"tableau_des_tempsChallenger : {tableau_des_tempsChallenger}")
    #print(f"tableau_succes_challenger : {tableau_succes_challenger}")
    tableau_temps_challenger_diff = [t.strftime("%-S") for t in tableau_des_tempsChallenger] #recupère le temps pour le challenger
    tableau_temps_controller_diff = [t.strftime("%-S") for t in tableau_des_tempsController] #recupère le temps pour le controller
    all_temps_diff = sorted(list(set(tableau_des_tempsChallenger + tableau_des_tempsController)))#creation d'une liste triée ayant les temps de chacun des groupes
    map_challenger_diff = dict(total_succes_challenger_diff[1:])
    map_controller_diff= dict(total_succes_controller_diff[1:])

    data_controller_diff=[]
    data_challenger_diff=[]
    for temps in all_temps_diff:
        data_challenger_diff.append(map_challenger_diff.get(temps,0))
        data_controller_diff.append(map_controller_diff.get(temps,0))
    all_temps_diff = [elt.strftime("%-S") for elt in all_temps_diff]

    print(f"data_challenger :  {data_challenger_diff}")
    print("\n\n")
    print(f"data_controller : {data_controller_diff}")
    print("\n\n")
    print(f"all_temps : {all_temps_diff}")

   



    return render_template('test.html',labels=all_temps_diff,data1=list(data_controller_diff), data2=list(data_challenger_diff))



@app.route('/test_khi2/<id>')
def test_khi2(id):
    t=models.Testeur.query.get(id)
    total_individu= db.session.query(models.Observation).filter(text("testeur_id=:value")).params(value=id).count()
    total_individu_challenger=db.session.query(models.Observation).filter(text("testeur_id=:value and classe_renvoyee=:valeur1")).params(value=id, valeur1=2).count()
    #print(f"total_individu_challenger : {total_individu_challenger}")
    total_individu_controller=db.session.query(models.Observation).filter(text("testeur_id=:value and classe_renvoyee=:valeur2")).params(value=id,valeur2=1).count()
    #print(f"total_individu_controller : {total_individu_controller}")
    total_succes_controller=db.session.query(models.Observation).filter(text("testeur_id=:testeur_id and classe_renvoyee=:classe_renvoyee and feedback=:feedback")).params(testeur_id=id, classe_renvoyee=1, feedback=1).count()
    total_succes_challenger=db.session.query(models.Observation).filter(text("testeur_id=:testeur_id and classe_renvoyee=:classe_renvoyee and feedback=:feedback")).params(testeur_id=id, classe_renvoyee=2, feedback=1).count()
    calcul_interm1=(total_succes_controller*total_individu)/total_individu_controller
    proba_succes_controller=float((calcul_interm1*100)/total_individu)
    print(f"proba_succes_controller {proba_succes_controller}")
    calcul_interm2=(total_succes_challenger*total_individu)/total_individu_challenger
    proba_succes_challenger=float((calcul_interm2*100)/total_individu)
    print(f"proba_succes_challenger {proba_succes_challenger}")
    difference_de_succes=abs((proba_succes_challenger)-(proba_succes_controller))
    print(f"difference_de_succes {difference_de_succes}")
    print("\n")
   

    sigma_chap = float((proba_succes_controller*total_individu_controller+proba_succes_challenger*total_individu_challenger)/total_individu)
    sigma_chap=sigma_chap/100
    print(f"sigma_chap :  {sigma_chap}")

    ecart_type=sqrt((sigma_chap*(1-sigma_chap))*(1./total_individu_controller+1./total_individu_challenger))
    print(f"ecart type {ecart_type}")
    x_ho=np.linspace(0-12*ecart_type,0+12*ecart_type,1000)
    y_ho=scs.norm(0,ecart_type).pdf(x_ho)
    y_h1=scs.norm(difference_de_succes/100,ecart_type).pdf(x_ho)
    x_h1=np.linspace(difference_de_succes/100-12*ecart_type,difference_de_succes/100+12*ecart_type,1000)
    
    #print(f"x_ho : {x_ho}")
    #print(f"y_ho: {y_ho}")
    


    return render_template('test_khi2.html',labels1=list(x_ho),labels2= list(x_h1), data1=list(y_ho), data2=list(y_h1))



