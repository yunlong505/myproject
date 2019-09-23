from gevent._semaphore import Semaphore
from locust import HttpLocust, TaskSet, task, events

all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()
start_global_num = 1


def on_hatch_complete(**kwargs):
    # 创建钩子方法
    all_locusts_spawned.release()


# 挂载到locust钩子函数（所有的Locust实例产生完成时触发）
events.hatch_complete += on_hatch_complete


class ScriptTasks(TaskSet):
    def on_start(self):
        global start_global_num
        print(self.locust.name + "--执行on_start,start_num:" + str(start_global_num))
        self.locust.start_num = start_global_num
        start_global_num = start_global_num + 1
        # 限制在所有用户准备完成前处于等待状态
        all_locusts_spawned.wait()

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
    min_wait = 1000
    max_wait = 1000
