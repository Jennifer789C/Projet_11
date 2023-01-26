from server import loadClubs, loadCompetitions


def test_vue_index(client, templates_utilises):
    response = client.get('/')
    assert response.status_code == 200
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


def test_login_adresse_valide():
    pass


def test_login_adresse_invalide():
    pass
