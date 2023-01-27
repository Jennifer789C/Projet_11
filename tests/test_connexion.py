from server import loadClubs, loadCompetitions


def test_vue_index(client, templates_utilises):
    reponse = client.get("/")
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "index.html"


def test_loadClubs():
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
    resultat = [{"name": "Spring Festival",
                 "date": "2020-03-27 10:00:00",
                 "numberOfPlaces": "25"},
                {"name": "Fall Classic",
                 "date": "2020-10-22 13:30:00",
                 "numberOfPlaces": "13"}
                ]
    assert loadCompetitions() == resultat


def test_login_adresse_valide(client, templates_utilises, club, competitions):
    reponse = client.post("/showSummary", data={"email": "mail@test.com"}, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "welcome.html"
    assert context["club"] == club[0]
    assert context["competitions"] == competitions


def test_login_adresse_invalide(client, templates_utilises, club):
    reponse = client.post("/showSummary", data={"email": "mail@test.fr"}, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "index.html"


def test_vue_showSummary_inaccessible(client):
    reponse = client.get("/showSummary")
    assert reponse.status_code == 405
