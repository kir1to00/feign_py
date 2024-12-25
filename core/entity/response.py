# feign远程调用响应体
class FeignRemoteResponse:
    def __init__(self, data=None, message="success", code=0):
        self.data = data
        self.code = code
        self.message = message

    def __str__(self):
        return f"HTTP {self.code}\nBody:\n{self.data}"

    def get_body(self):
        return self.data
