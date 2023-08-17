from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)
    header={}

    def on_start(self):
        response = self.client.post("/login", data={"username":"ankur1@gmail.com", "password":"test123"})
        self.header["Authorization"] = "Bearer "+response.json()["access_token"]


    @task
    def get_posts(self):
        self.client.get("/posts",headers=self.header)
