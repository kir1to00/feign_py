import os
from core.service_center.nacos.nacos_center import NacosCenter


class ServiceCenterFactory:
    @staticmethod
    def get_center(center_name='nacos'):
        if center_name == 'nacos':
            return NacosCenter()
