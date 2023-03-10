import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
MAX_PLACES = 12
reservations = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if not club:
        flash("L'adresse mail saisie est inconnue")
        return redirect(url_for('index'))
    else:
        club = club[0]
    return render_template('welcome.html', club=club, competitions=competitions, datetime=datetime)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub[0], competition=foundCompetition[0])
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for('index'))


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    places_reservees = [c for c in reservations if c["club"] == club["name"] and c["competition"] == competition["name"]]

    if datetime.now() > datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S"):
        flash(f"Cette compétition est terminée, vous ne pouvez plus réserver de places.")
        return render_template('welcome.html', club=club, competitions=competitions, datetime=datetime)

    elif placesRequired < 0:
        flash(f"Vous avez saisi une valeur négative, veuillez réessayer.")
        return redirect(url_for('book', competition=competition["name"], club=club["name"]))

    elif placesRequired > int(club["points"]):
        flash(f"Vous n'avez pas assez de points, votre solde est de {club['points']}.")
        return redirect(url_for('book', competition=competition["name"], club=club["name"]))

    elif placesRequired > int(competition["numberOfPlaces"]):
        flash(f"Il ne reste que {competition['numberOfPlaces']} places disponibles, vous ne pouvez pas en réserver plus.")
        return redirect(url_for('book', competition=competition["name"], club=club["name"]))

    elif not places_reservees:
        if placesRequired > MAX_PLACES:
            flash(f"Afin de garantir l'équité entre clubs, vous ne pouvez pas réserver plus de {MAX_PLACES} places par compétition.")
            return redirect(url_for('book', competition=competition["name"], club=club["name"]))

        else:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club["points"] = int(club["points"]) - placesRequired
            reservations.append({"club": club["name"], "competition": competition["name"], "places": placesRequired})
            flash(f"Félicitations! Vous avez correctement réservé {placesRequired} places pour la compétition {competition['name']}.")
            competition.update({club["name"]: placesRequired})
            return render_template('welcome.html', club=club, competitions=competitions, datetime=datetime)

    elif placesRequired + int(places_reservees[0]["places"]) > MAX_PLACES:
        flash(f"Vous avez déjà réservé {places_reservees[0]['places']} places pour cette compétition. Vous ne pouvez en réserver que "
              f"{MAX_PLACES} au total.")
        return redirect(url_for('book', competition=competition["name"], club=club["name"]))

    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club["points"] = int(club["points"]) - placesRequired
        places_reservees[0]["places"] = placesRequired + int(places_reservees[0]["places"])
        flash(f"Félicitations! Vous avez correctement réservé {places_reservees[0]['places']} places pour la compétition "
              f"{competition['name']}.")
        competition.update({club["name"]: places_reservees[0]["places"]})
        return render_template('welcome.html', club=club, competitions=competitions, datetime=datetime)


@app.route('/tableau')
def tableau():
    return render_template('tableau.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
