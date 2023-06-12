import os.path
import random
import urllib.parse

from locust import HttpUser, task

inputs_file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "inputs.txt"
)

with open(inputs_file_path, "r", encoding="utf-8") as inputs_file:
    inputs = [line.strip() for line in inputs_file]


def random_inference_url() -> str:
    query = urllib.parse.quote(random.choice(inputs))
    return f"/predict/{query}"


class QuickstartUser(HttpUser):
    @task
    def predict(self):
        with self.client.get(random_inference_url()) as response:
            if response.status_code != 200:
                response.failure("Could not return response")
