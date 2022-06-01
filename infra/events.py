import logging
from pprint import PrettyPrinter

from troposphere import GetAtt, events

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def michizure_event_rule(events_invoke_lambda_role, michizure_function):
  return events.Rule(
      'MichizureEventRule',
      Description='Remove corresponding snapshot when a AMI is deregistered.',
      EventPattern={
          'detail-type': ['AWS API Call via CloudTrail'],
          'detail': {
              'eventSource': ['ec2.amazonaws.com'],
              'eventName': ['DeregisterImage'],
          },
      },
      RoleArn=GetAtt(events_invoke_lambda_role, 'Arn'),
      State='ENABLED',
      Targets=[
          events.Target(
              Arn=GetAtt(michizure_function, 'Arn'), Id='MichizureFunction'),
      ])
