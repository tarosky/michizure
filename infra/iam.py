import logging
from pprint import PrettyPrinter

from troposphere import iam

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def michizure_role_policy():
  return {
      'Version': '2012-10-17',
      'Statement': [
          {
              'Effect': 'Allow',
              'Action': [
                  'ec2:DescribeSnapshots',
                  'ec2:DeleteSnapshot',
              ],
              'Resource': ['*'],
          },
      ],
  }


def lambda_assume_role_policy():
  return {
      'Version': '2012-10-17',
      'Statement': [
          {
              'Effect': 'Allow',
              'Principal': {
                  'Service': 'lambda.amazonaws.com'
              },
              'Action': 'sts:AssumeRole'
          }
      ]
  }


def lambda_role_policy():
  return {
      'Version': '2012-10-17',
      'Statement': [
          {
              'Action': ['logs:*'],
              'Resource': 'arn:aws:logs:*:*:*',
              'Effect': 'Allow',
          },
          {
              # This action is not needed since LogGroup resource does that.
              'Action': ['logs:CreateLogGroup'],
              'Resource': 'arn:aws:logs:*:*:*',
              'Effect': 'Deny',
          },
          {
              'Action': ['lambda:*'],
              'Resource': '*',
              'Effect': 'Allow',
          },
      ],
  }


def lambda_michizure_role():
  return iam.Role(
      'LambdaMichizureRole',
      AssumeRolePolicyDocument=lambda_assume_role_policy(),
      Policies=[
          iam.Policy(
              PolicyName='lambda', PolicyDocument=lambda_role_policy()),
          iam.Policy(
              PolicyName='michizure', PolicyDocument=michizure_role_policy()),
      ])


def events_invoke_lambda_role_policy():
  return {
      'Version': '2012-10-17',
      'Statement': [
          {
              'Effect': 'Allow',
              'Action': ['lambda:InvokeFunction'],
              'Resource': ['*']
          }
      ]
  }


def events_invoke_lambda_assume_role_policy():
  return {
      'Version': '2012-10-17',
      'Statement': [
          {
              'Sid': '',
              'Effect': 'Allow',
              'Principal': {
                  'Service': 'events.amazonaws.com'
              },
              'Action': 'sts:AssumeRole'
          }
      ]
  }


def events_invoke_lambda_role():
  return iam.Role(
      'EventsInvokeLambdaRole',
      AssumeRolePolicyDocument=events_invoke_lambda_assume_role_policy(),
      Policies=[
          iam.Policy(
              PolicyName='event',
              PolicyDocument=events_invoke_lambda_role_policy()),
      ])
