import json
import random
import os
from urllib import parse

from locust import HttpLocust, TaskSet, task, between


# Load json file
def random_line():
    file_name = random.choice(os.listdir("./searches"))
    lines = open(file_name).read().splitlines()
    return random.choice(lines)


class UserTasks(TaskSet):
    def __init__(self, parent):
        super(UserTasks, self).__init__(parent)

    @task
    def get_random_payload(self):
        req = random_line().split('||')
        if len(req) == 2:
            self.client.get('http://search5:9200'+req[0], data=req[1].replace('@@@@', '\n'))


class WebsiteUser(HttpLocust):
    """
    Locust user class that does requests to the locust web server running on localhost
    """
    wait_time = between(2, 5)
    task_set = UserTasks
