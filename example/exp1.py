from decorator.feign_api import FeignApi
from enums.http_method import HttpMethod


class Test:
    @staticmethod
    @FeignApi(method=HttpMethod.GET,
              service_type='nacos',
              service_name="test-api",
              group_name="asia-rag",
              url="hello",
              name="测试接口",
              service_center_url="http://localhost:8848")
    def hello(message="feign测试"):
        ...


test = Test().hello()
print(test.data)
