def test_actualisation_points(client, templates_utilises, club, competitions, reservations):
    reponse = client.get("/")
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "index.html"
    assert b"<td>Club test</td>\n                <td>13</td>" in reponse.data

    club = club[0]
    competition = competitions[0]
    places = 7
    data = {"club": club["name"], "competition": competition["name"], "places": places}
    reponse = client.post("/purchasePlaces", data=data, follow_redirects=True)
    assert reponse.status_code == 200
    assert len(templates_utilises) == 2
    template, context = templates_utilises[1]
    assert template.name == "welcome.html"

    reponse = client.get("/")
    assert reponse.status_code == 200
    assert len(templates_utilises) == 3
    template, context = templates_utilises[2]
    assert template.name == "index.html"
    assert b"<td>Club test</td>\n                <td>6</td>" in reponse.data
