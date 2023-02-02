def test_actualisation_points(client, club, competitions, reservations):
    client.get("/")
    reponse = client.get("/tableau")
    assert b"<td>Club test</td>\n                <td>13</td>" in reponse.data

    client.get("/")
    client.post("/showSummary", data={"email": "mail@test.com"}, follow_redirects=True)

    club = club[0]
    competition = competitions[0]
    uri = "/book/" + competition["name"] + "/" + club["name"]
    client.get(uri, follow_redirects=True)

    places = 7
    data = {"club": club["name"], "competition": competition["name"], "places": places}
    client.post("/purchasePlaces", data=data, follow_redirects=True)

    client.get("/logout", follow_redirects=True)

    reponse = client.get("/tableau")
    assert b"<td>Club test</td>\n                <td>6</td>" in reponse.data
