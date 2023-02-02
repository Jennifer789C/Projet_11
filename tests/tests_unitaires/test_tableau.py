def test_vue_tableau(client, templates_utilises, club):
    """L'URL /tableau est accessible : status_code + template + context"""
    reponse = client.get("/tableau")
    assert reponse.status_code == 200
    assert len(templates_utilises) == 1
    template, context = templates_utilises[0]
    assert template.name == "tableau.html"
    assert context["clubs"] == club
    assert b"<td>Club test</td>\n                <td>13</td>" in reponse.data


def test_vue_tableau_inaccessible(client):
    """Méthode POST non autorisée sur l'URL /tableau"""
    reponse = client.post("/tableau")
    assert reponse.status_code == 405
