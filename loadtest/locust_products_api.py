import json
import random
import os
from urllib import parse

from locust import HttpLocust, TaskSet, task, between


# Load json file
def random_line():
    lines = open('searches_small.txt').read().splitlines()
    return random.choice(lines)


def random_post():
    lines = open('index_requests').read().splitlines()
    return random.choice(lines)

class UserTasks(TaskSet):
    def __init__(self, parent):
        super(UserTasks, self).__init__(parent)

    @task(4)
    def get_random_payload(self):
        req = random_line().split('||')
        if len(req) == 2:
            self.client.get('http://localhost:9200'+req[0], data=req[1].replace('@@@@', '\n').encode('utf8'))

    @task(1)
    def get_random_post(self):
        req = random_post().split('||')
        if len(req) == 2:
            self.client.post('http://localhost:9200'+req[0], data=req[1].replace('@@@@', '\n').encode('utf8'))


class WebsiteUser(HttpLocust):
    """
    Locust user class that does requests to the locust web server running on localhost
    """
    wait_time = between(2, 5)
    task_set = UserTasks