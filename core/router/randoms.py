import random

from core.router.base import Router
from model.center_schema import BaseServiceInfo


class RandomsRouter(Router):
    def select(self, si: BaseServiceInfo):
        count = len(si.hosts)
        return si.hosts[random.randint(1, 100) % count] if count > 0 else None
