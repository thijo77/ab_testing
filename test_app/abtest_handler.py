import requests
import os

#HOST = "http://192.168.191.131:5000"
HOST = "http://localhost:5000"
class AbTestHandler:
	def __init__(self):
		self.last_id = None

	def fetch_class(self, test_id):
		response = requests.get(f"{HOST}/attribution_classe/{test_id}")
		data = response.json()
		print(data)
		self.last_id = data.get("observation_id")
		classe = data.get("classe_attribuee")
		test_id_ = data.get("utilisateur")
		return  classe, self.last_id, test_id_

	def send_feedback(self, feedback):
		return requests.post(f"{HOST}/observation/{self.last_id}", json={
			"feedback":feedback
		})
