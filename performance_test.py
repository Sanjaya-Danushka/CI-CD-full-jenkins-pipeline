from locust import HttpUser, task, between

class PythonAppUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def test_hello(self):
        response = self.client.get("/")
        assert response.status_code == 200

    @task(3)  # This task will be executed 3 times more often than test_hello
    def test_health(self):
        response = self.client.get("/health")
        assert response.status_code == 200
