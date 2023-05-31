import random

from locust import HttpUser, task

with open("inputs.txt", "r", encoding="utf-8") as inputs_file:
    inputs = [line.strip() for line in inputs_file]


class QuickstartUser(HttpUser):
    @task
    def predict(self):
        with self.client.get(f"/predict/{random.choice(inputs)}") as response:
            if response.status_code != 200:
                response.failure("Could not return response")
