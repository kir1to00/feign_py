import json

import httpx

from enums.nacos_url_enum import NacosUrlEnum
from model.center_schema import NacosSchema, NacosServiceInfo, BaseServiceInfo
from core.service_center.base_center import BaseCenter
import logging

from util.base_utils import json_snake_to_camel, json_camel_to_snake

logger = logging.getLogger(__name__)


class NacosCenter(BaseCenter):
    def get_service(self, service_url, service_name, group_name='DEFAULT_GROUP', **kwargs):
        schema = NacosSchema(service_name=service_name, group_name=group_name, **kwargs)
        with httpx.Client() as hpx:
            resp = hpx.get(url=service_url + NacosUrlEnum.INSTANCE_LIST.value,
                           params=json.loads(json_snake_to_camel(json.dumps(schema.model_dump(exclude_unset=True)))))
        if resp.status_code == 200:
            result = resp.json()
            if result['code'] == 0:
                return NacosServiceInfo(**json.loads(json_camel_to_snake(json.dumps(result['data']))))
            else:
                logger.error(f"GET Nacos Service Info Failed.\n{result['message']}")
                return None
