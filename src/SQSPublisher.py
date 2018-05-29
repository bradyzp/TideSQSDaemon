# -*- coding: utf-8 -*-

import os
import json
import numbers
import logging
import boto3


class SQSPublisher:
    def __init__(self, queue_name, profile=None, region='us-west-2'):
        self._log = logging.getLogger(__name__)
        self._connected = False
        self._session = None
        self._resource = None
        self._queue = None
        self._name = queue_name
        self._profile = profile or 'default'
        self._region = os.getenv('AWS_REGION', None) or region

    def connect(self):
        try:
            self._session = boto3.Session(region_name=self._region, profile_name=self._profile)
            self._resource = self._session.resource('sqs')
            self._queue = self._resource.get_queue_by_name(self._name)
            self._connected = True
        except:
            self._log.exception("Exception connecting to queue.")
            raise ConnectionError("Exception connecting to SQS queue resource.")

    def send(self, body, attributes=None, group_id=None):
        if not self._connected:
            raise ConnectionError("SQS Session connection not established. Call connect() first.")
        message = self._pack_message(body, attributes, group_id)
        self._queue.send_message(message)

    def batch_send(self, *messages, attributes=None, group_id=None, batch_size=10):
        if not self._connected:
            raise ConnectionError("SQS Session connection not established. Call connect() first.")

        if batch_size > 10:
            batch_size = 10

        for i in range(len(messages) // batch_size):
            start = i * batch_size
            end = start + batch_size
            batch = [self._pack_message(body, attributes, group_id, i) for body in messages[start:end]]
            result = self._queue.send_messages(Entries=batch)
            self._log.debug(result)

    @staticmethod
    def _pack_message(body, attributes, group_id, msg_id=None):
        """
        Pack a message to AWS Spec:
        https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-message-attributes.html
        """
        message = dict(MessageBody=json.dumps(body), MessageGroupId=group_id)
        if attributes is not None and isinstance(attributes, dict):
            message['MessageAttributes'] = SQSPublisher._pack_attributes(**attributes)
        if msg_id is not None:
            message['Id'] = msg_id
        return message

    @staticmethod
    def _pack_attributes(**attrs):
        packed = dict()
        for k, v in attrs.items():
            if isinstance(v, str):
                dtype = 'String'
            elif isinstance(v, numbers.Real):
                dtype = 'Number'
            else:
                continue

            packed[k] = {
                'DataType': dtype,
                'StringValue': str(v)
            }
        return packed
