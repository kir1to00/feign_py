import threading
from contextlib import asynccontextmanager
import requests
import uvicorn
from fastapi import FastAPI
from starlette.responses import Response


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)
nacos_service_url = 'http://127.0.0.1:8848'
# 服务的组名
GROUP_NAME = "asia-rag"
# 服务的名称
SERVICE_NAME = "test-api"
# 服务的IP地址
IP = "127.0.0.1"
# 服务的端口
PORT = 9855


class NacosService:

    def __init__(self, nacos_addr, service_name, group_name, ip, port, beat_interval=5):
        self.nacos_addr = nacos_addr
        self.service_name = service_name
        self.group_name = group_name
        self.ip = ip
        self.port = port
        self.beat_interval = beat_interval

        # 注册服务实例
        self.service_register()

        # 启动心跳定时器
        self.start_heartbeat_timer()

    def service_register(self):
        url = f"{self.nacos_addr}/nacos/v2/ns/instance"
        params = {
            "serviceName": self.service_name,
            "groupName": self.group_name,
            "ip": self.ip,
            "port": self.port,
            "ephemeral": True
        }
        res = requests.post(url, data=params)
        print(res)
        print("完成注册")

    def service_beat(self):
        url = f"{self.nacos_addr}/nacos/v1/ns/instance/beat"
        params = {
            "serviceName": self.service_name,
            "groupName": self.group_name,
            "ip": self.ip,
            "port": self.port,
        }
        res = requests.put(url, data=params)
        print(f"心跳检测中... 响应状态码： {res.status_code}")

    def start_heartbeat_timer(self):
        """启动心跳定时器"""
        self.beat_timer = threading.Timer(self.beat_interval, self.heartbeat_loop)
        self.beat_timer.daemon = True  # 设置为守护线程，以便程序结束时自动终止
        self.beat_timer.start()

    def heartbeat_loop(self):
        """心跳循环函数"""
        self.service_beat()
        self.start_heartbeat_timer()  # 递归地重新启动定时器


def health(message) -> Response:
    print(message)
    return Response(status_code=200, content=f"对端反馈{message}")


#
# # 心跳检测
# def service_beat():
#     while True:
#         url = f"{nacos_service_url}/nacos/v1/ns/instance/beat?serviceName=" + SERVICE_NAME + "&ip=" + IP + "&port=" + str(
#             PORT)
#         params = {
#             "serviceName": SERVICE_NAME,
#             "groupName": GROUP_NAME,
#             "ip": IP,
#             "port": PORT
#         }
#         res = requests.put(url,data=params)
#         print(f"心跳检测中... 响应状态码： {res.status_code}")
#         time.sleep(5)
app.get("/hello", description="存活检测")(health)

if __name__ == "__main__":
    NacosService(nacos_addr=nacos_service_url, group_name=GROUP_NAME, service_name=SERVICE_NAME, ip=IP, port=PORT)
    uvicorn.run("api:app", host="0.0.0.0", port=9855, workers=1)
