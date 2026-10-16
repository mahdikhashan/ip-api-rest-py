"""Load test for the IP API.

Run (web UI at http://localhost:8089):
    uv run locust -f loadtest/locustfile.py --host http://<vm-address>

Headless example (100 users, +10/s, 2 minutes, HTML report):
    uv run locust -f loadtest/locustfile.py --host http://<vm-address> \
        --headless -u 100 -r 10 -t 2m --html loadtest/report.html
"""
from locust import HttpUser, between, task


class IPApiUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task(3)
    def plain_text(self):
        with self.client.get("/", name="GET / (text)", catch_response=True) as r:
            if r.status_code != 200 or not r.text:
                r.failure(f"unexpected response: {r.status_code} {r.text!r}")

    # ignore test on the json qurry path
    # @task(1)
    # def json(self):
    #     with self.client.get(
    #         "/?format=json", name="GET /?format=json", catch_response=True
    #     ) as r:
    #         if r.status_code != 200 or "ip" not in r.json():
    #             r.failure(f"unexpected response: {r.status_code} {r.text!r}")
