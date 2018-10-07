import logging
from pprint import PrettyPrinter

from troposphere import GetAtt, Ref, awslambda

from infra import util

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)

util.patch_events()


def get_code():
  with open('lambda/michizure.py', 'r') as f:
    return f.read()


def michizure_function(lambda_michizure_role):
  return awslambda.Function(
      'MichizureFunction',
      Code=awslambda.Code(ZipFile=get_code()),
      Handler='index.lambda_handler',
      Role=GetAtt(lambda_michizure_role, 'Arn'),
      Runtime='python3.6',
      Timeout=20)


def michizure_invocation_permission(michizure_function, michizure_event_rule):
  return awslambda.Permission(
      'MichizureInvocationPermission',
      Action='lambda:InvokeFunction',
      FunctionName=Ref(michizure_function),
      Principal='events.amazonaws.com',
      SourceArn=GetAtt(michizure_event_rule, 'Arn'))
