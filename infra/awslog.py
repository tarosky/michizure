import logging
from pprint import PrettyPrinter

from troposphere import Join, Ref, logs

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def lambda_log_name(function):
  return Join('', [
      '/aws/lambda/',
      Ref(function),
  ])


def michizure_log(michizure_function):
  return logs.LogGroup(
      'MichizureLog',
      LogGroupName=lambda_log_name(michizure_function),
      RetentionInDays=180)
