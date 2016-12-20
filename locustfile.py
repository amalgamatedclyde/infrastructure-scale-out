__author__ = 'clyde'
from locust import HttpLocust, TaskSet, task
import base64
import os
from random import choice


images = os.listdir('/home/clyde/markable/imgs')
print images
class UserBehavior(TaskSet):
    # @task(2)
    # def index(self):
    #     self.client.get("/")

    @task(1)
    def post(self):
        with open('/home/clyde/markable/imgs/' + choice(images), 'rb') as fh:
            encoded_data = base64.b64encode(fh.read())
        post_dict = {'data': {"image_file": encoded_data}}
        self.client.post("/classes", json=post_dict)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 250
    max_wait = 1000