import hashlib
import logging
import json

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from django.conf import settings


logger = logging.getLogger(__name__)

class Mailchimp:
    def __init__(self):
        self.client = MailchimpMarketing.Client()
        self.client.set_config({
            "api_key": settings.MAILCHIMP_API_KEY,
            "server": settings.MAILCHIMP_SERVER_PREFIX
        })
        self.client.ping.get()

    def add_member(self, email, list_id, propagate_exception=False):
        email = email.strip().lower()
        try:
            response = self.client.lists.add_list_member(list_id, body={
                "email_address": email,
                "status": "subscribed"
            })
        except ApiClientError as e:
            error = json.loads(e.text)
            logger.error("%s (%s)",error["title"], error["detail"])
            if propagate_exception:
                raise e
        else:
            return response

    def get_member(self, email, list_id, propagate_exception=False):
        email = email.strip().lower()
        email_hash = hashlib.md5(email.encode("utf-8")).hexdigest()
        try:
            response = self.client.lists.get_list_member(list_id, email_hash)
        except ApiClientError as e:
            error = json.loads(e.text)
            logger.error("%s (%s)",error["title"], error["detail"])
            if propagate_exception:
                raise e
        else:
            return response

    def delete_member(self, email, list_id, propagate_exception=False):
        email = email.strip().lower()
        email_hash = hashlib.md5(email.encode("utf-8")).hexdigest()
        try:
            response = self.client.lists.delete_list_member(list_id, email_hash)
        except ApiClientError as e:
            error = json.loads(e.text)
            logger.error("%s (%s)",error["title"], error["detail"])
            if propagate_exception:
                raise e
        else:
            return response