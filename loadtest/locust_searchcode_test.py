from locust import HttpLocust, TaskSet, task, between
import random
from urllib import parse
from random import randint


class UserTasks(TaskSet):

    def search_api(self, query, src):
        url = '?q=' + parse.quote_plus(query)
        if src:
            url = url + '&src=' + parse.quote_plus(src)
        self.client.get(domain() + url,
                        headers=headers())

    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def search_with_src(self):
        self.search_api(query=random_terms(), src=random_src())


class WebsiteUser(HttpLocust):
    """
    Locust user class that does requests to the locust web server running on localhost
    """
    wait_time = between(4, 10)
    task_set = UserTasks


def domain():
    return '''https://searchcode.com/'''


def headers():
    return {
        'Accept': 'application/json',
        'Accept - Language': 'en - au',
        'Host': 'searchcode.com'
    }


def random_language():
    lang_code = randint(1, 118)
    return f'{lang_code}'


def random_src():
    src = randint(1, 10)
    return f'{src}'


def random_terms():
    return random.choice(['interface',
                          'golang',
                          'Factory Method',
                          'Abstract class',
                          'map&hashmap',
                          'uint',
                          'bytes&'])