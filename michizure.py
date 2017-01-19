import logging
from pprint import PrettyPrinter

from troposphere import Template

from infra import awslambda, awslog, events, iam

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def construct_template():
  t = Template('Michizure')

  lambda_michizure_role = t.add_resource(iam.lambda_michizure_role())
  events_invoke_lambda_role = t.add_resource(iam.events_invoke_lambda_role())

  michizure_function = t.add_resource(
      awslambda.michizure_function(lambda_michizure_role))

  t.add_resource(awslog.michizure_log(michizure_function))

  michizure_event_rule = t.add_resource(
      events.michizure_event_rule(
          events_invoke_lambda_role, michizure_function))

  t.add_resource(
      awslambda.michizure_invocation_permission(
          michizure_function, michizure_event_rule))

  return t


if __name__ == '__main__':
  print(construct_template().to_json(indent=2))
