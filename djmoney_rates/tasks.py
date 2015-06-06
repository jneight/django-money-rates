# coding=utf-8

from __future__ import absolute_import

from django.core.management import call_command

from celery import shared_task
from celery.utils.log import get_task_logger


logger_celery = get_task_logger(__name__)


@shared_task
def update_money_rates():
    logger_celery.info('[TASK] [SCHED] going to update money rates')
    return call_command('update_rates')
