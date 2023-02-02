from locust import HttpUser, task


class TestPerformance(HttpUser):
    @task
    def index(self):
        self.client.get("/")

    @task
    def showSummary(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get("/book/Fall Classic/Simply Lift")

    @task
    def purchasePlaces(self):
        self.client.post("/purchasePlaces", data={"club": "Simply Lift", "competition": "Fall Classic", "places": 3})

    @task
    def logout(self):
        self.client.get("/logout")
