import server


def test_vue_book(client, templates_utilises, club, competitions):
    """Test de la vue si club et compétition ok : status_code + template + context"""
    club = club[0]
    competition = competitions[0]
    uri = "/book/" + competition["name"] + "/" + club["name"]
    reponse = client.get(uri, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "booking.html"
    assert context["club"] == club
    assert context["competition"] == competition


def test_vue_book_club_errone(client, templates_utilises, competitions):
    """Test de la vue si le club est erroné : status_code + template + context"""
    competition = competitions[0]
    uri = "/book/" + competition["name"] + "/Club erreur"
    reponse = client.get(uri, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "welcome.html"
    assert context["club"] == "Club erreur"
    assert context["competitions"] == competitions


def test_vue_book_competition_erronnee(client, templates_utilises, club, competitions):
    """Test de la vue si la compétition est erronée : status_code + template + context"""
    club = club[0]["name"]
    uri = "/book/Competition erreur/" + club
    reponse = client.get(uri, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "welcome.html"
    assert context["club"] == club
    assert context["competitions"] == competitions


def test_vue_book_inaccessible(client):
    """Méthode POST non autorisée sur l'URL /book/<competition>/<club>"""
    reponse = client.post("book/<competition>/<club>")
    assert reponse.status_code == 405


def test_reservation(client, templates_utilises, club, competitions):
    """Saisie d'une valeur pour réserver"""
    club = club[0]
    competition = competitions[0]["name"]
    places = 7
    data = {"club": club["name"], "competition": competition, "places": places}
    reponse = client.post("/purchasePlaces", data=data, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "welcome.html"
    assert context["club"] == club
    assert context["competitions"] == competitions


def test_reservation_limite_points(client, templates_utilises, club, competitions):
    """Le club ne peut pas réserver plus de places qu'il n'a de points"""
    club = club[0]
    club["points"] = 10
    competition = competitions[0]
    places = 11
    data = {"club": club["name"], "competition": competition["name"], "places": places}
    reponse = client.post("/purchasePlaces", data=data, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "booking.html"
    assert context["club"] == club
    assert context["competition"] == competition


def test_reservation_limite_places(client, templates_utilises, club, competitions):
    """Le club ne peut pas réserver plus de places que la compétition en a de disponible"""
    club = club[0]
    competition = competitions[0]
    competition["numberOfPlaces"] = 5
    places = 11
    data = {"club": club["name"], "competition": competition["name"], "places": places}
    reponse = client.post("/purchasePlaces", data=data, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "booking.html"
    assert context["club"] == club
    assert context["competition"] == competition


def test_reservation_12_max_premier_acces(client, templates_utilises, club, competitions):
    """Le club ne peut pas réserver plus de 12 places par compétition"""
    club = club[0]
    competition = competitions[0]
    places = 13
    data = {"club": club["name"], "competition": competition["name"], "places": places}
    reponse = client.post("/purchasePlaces", data=data, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "booking.html"
    assert context["club"] == club
    assert context["competition"] == competition


def test_reservation_12_max_acces_supplementaire_invalide(client, templates_utilises, club, competitions, mocker):
    """Le club ne peut pas réserver plus de 12 places par compétition"""
    club = club[0]
    competition = competitions[0]
    mocker.patch.object(server, "places_reservees", {competition["name"]: 3})
    places = 10
    data = {"club": club["name"], "competition": competition["name"], "places": places}
    reponse = client.post("/purchasePlaces", data=data, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "booking.html"
    assert context["club"] == club
    assert context["competition"] == competition


def test_reservation_12_max_acces_supplementaire_valide(client, templates_utilises, club, competitions, mocker):
    """Le club ne peut pas réserver plus de 12 places par compétition"""
    club = club[0]
    competition = competitions[0]
    mocker.patch.object(server, "places_reservees", {competition["name"]: 1})
    places = 10
    data = {"club": club["name"], "competition": competition["name"], "places": places}
    reponse = client.post("/purchasePlaces", data=data, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "welcome.html"
    assert context["club"] == club
    assert context["competitions"] == competitions


def test_vue_puchasePlaces_inaccessible(client):
    """Méthode GET non autorisée sur l'URL /purchasePlaces"""
    reponse = client.get("/purchasePlaces")
    assert reponse.status_code == 405


def test_bouton_reservation_inaccessible(client, templates_utilises, club, competitions):
    """Le bouton de réservation ne doit pas s'afficher si :
    - il n'y a plus de place disponible dans la compétition
    - le club n'a plus de point disponible
    - le club a déjà dépensé 12 points dans cette compétition
    - la date de la compétition est antérieure à la date du jour
    """
    club = club[0]
    competition = competitions[0]
    competition["numberOfPlaces"] = 0
    reponse = client.post("/showSummary", data={"email": club["email"]}, follow_redirects=True)
    template, context = templates_utilises[0]
    assert template.name == "welcome.html"
    assert b"Book Places" not in reponse.data


def test_points_disponible():
    """Le nombre de points du club doit être à jour"""
    pass


def test_places_disponible():
    """Le nombre de places disponibles de la compétition doit être à jour"""
    pass
