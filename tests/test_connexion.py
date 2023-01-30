from flask import request, url_for
from server import loadClubs, loadCompetitions


def test_loadClubs():
    """Test de la fonction loadClubs()"""
    resultat = [{"name": "Simply Lift",
                 "email": "john@simplylift.co",
                 "points": "13"},
                {"name": "Iron Temple",
                 "email": "admin@irontemple.com",
                 "points": "4"},
                {"name": "She Lifts",
                 "email": "kate@shelifts.co.uk",
                 "points": "12"}
                ]
    assert loadClubs() == resultat


def test_loadCompetitions():
    """Test de la fonction loadCompetitions()"""
    resultat = [{"name": "Spring Festival",
                 "date": "2020-03-27 10:00:00",
                 "numberOfPlaces": "25"},
                {"name": "Fall Classic",
                 "date": "2020-10-22 13:30:00",
                 "numberOfPlaces": "13"}
                ]
    assert loadCompetitions() == resultat


def test_vue_index(client, templates_utilises):
    """L'URL / est accessible : status_code + template + context"""
    reponse = client.get("/")
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "index.html"


def test_vue_index_inaccessible(client):
    """Méthode POST non autorisée sur l'URL /"""
    reponse = client.post("/")
    assert reponse.status_code == 405


def test_login_adresse_valide(client, templates_utilises, club, competitions):
    """Le club se connecte avec son adresse mail + redirection vers l'URL /showSummary : status_code + template + context"""
    reponse = client.post("/showSummary", data={"email": "mail@test.com"}, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "welcome.html"
    assert context["club"] == club[0]
    assert context["competitions"] == competitions


def test_login_adresse_invalide(client, templates_utilises, club):
    """Le club essaie de se connecter avec une adresse mail invalide"""
    reponse = client.post("/showSummary", data={"email": "mail@test.fr"}, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "index.html"


def test_vue_showSummary_inaccessible(client):
    """Méthode GET non autorisée sur l'URL /showSummary"""
    reponse = client.get("/showSummary")
    assert reponse.status_code == 405


def test_deconnexion(client, templates_utilises):
    """Le club se déconnecte + redirection vers l'URL / : status_code + template + context"""
    reponse = client.get("/logout", follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "index.html"
