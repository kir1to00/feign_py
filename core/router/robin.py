from core.router.base import Router
from model.center_schema import BaseServiceInfo


class RobinRouter(Router):
    counter = 0

    def select(self, si: BaseServiceInfo):
        count = len(si.hosts)
        RobinRouter.counter += 1
        if RobinRouter.counter > 100000:
            RobinRouter.counter = 0
        return si.hosts[RobinRouter.counter % count] if count > 0 else None
