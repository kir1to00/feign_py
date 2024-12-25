from enums.base import BaseEnum


class NacosUrlEnum(BaseEnum):
    # 注册 注销 更新 查询实例相关
    INSTANCES = "/nacos/v2/ns/instance"
    # 查询指定命名空间下的配置列表
    HISTORY_CONFIG = "/nacos/v2/cs/history/configs"
    # 查询指定服务的实例列表
    INSTANCE_LIST = "/nacos/v2/ns/instance/list"
