from typing import List

from core.router.base import Router
from model.center_schema import BaseServiceInfo, NacosHostsInfo
from util.ip_utils import ip_to_long, get_local_ip
import logging

logger = logging.getLogger(__name__)

try:
    CURRENT_IP_LONG = ip_to_long(get_local_ip())
except Exception as e:
    CURRENT_IP_LONG = 0  # 设置一个默认值以防止程序崩溃


class HashRouter(Router):
    def select(self, si: BaseServiceInfo):
        if not si or not si.hosts:
            logger.warning("No service info or hosts available.")
            return None

        hosts: List[NacosHostsInfo] = si.hosts
        count = len(hosts)
        if count == 0:
            logger.warning("Host list is empty.")
            return None

        try:
            index = CURRENT_IP_LONG % count
            selected_host = hosts[index]
            logger.info(f"Selected host {selected_host} for service {si}.")
            return selected_host
        except IndexError as e:
            logger.error("Index out of range error while selecting host: %s", e)
            return None
        except Exception as e:
            logger.error("Unexpected error while selecting host: %s", e)
            return None
