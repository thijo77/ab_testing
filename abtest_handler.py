import requests
import os

HOST = "http://192.168.191.131:5000"
TEST_ID = "22"
class AbTestHandler:
	def __init__(self):
		self.last_id = None

	def fetch_class(self):
		response = requests.get(f"{HOST}/attribution_classe/{TEST_ID}")
		data = response.json()
		print(data)
		self.last_id = data.get("observation_id")
		classe = data.get("classe_attribuee")
		test_id = data.get("utilisateur")
		return  classe, self.last_id, test_id

	def send_feedback(self, feedback):
		return requests.post(f"{HOST}/observation/{self.last_id}", json={
			"feedback":feedback
		})
