from locust import HttpLocust, TaskSet, task

start_global_num = 1


class ScriptTasks(TaskSet):
    def on_start(self):
        global start_global_num
        print(self.locust.name + "--执行on_start,start_num:" + str(start_global_num))
        self.locust.start_num = start_global_num
        start_global_num = start_global_num + 1

    @task()
    def index(self):
        num = self.locust.index_num
        print(str(self.locust.start_num) + "--执行index,index_num:" + str(num))
        self.client.get("/txqp/test")
        self.locust.index_num = num + 1


class websiteUser(HttpLocust):
    name = "test"
    start_num = 1
    index_num = 1
    task_set = ScriptTasks
    host = "http://192.168.2.62:8864"
    min_wait = 0
    max_wait = 0
