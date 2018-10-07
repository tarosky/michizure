import logging
from pprint import PrettyPrinter

from troposphere.events import Rule, Target

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def patch_events():
  # Patch for https://github.com/cloudtools/troposphere/issues/775
  if 'RoleArn' in Target.props:
    del Target.props['RoleArn']
  if 'RoleArn' not in Rule.props:
    Rule.props['RoleArn'] = (str, False)
