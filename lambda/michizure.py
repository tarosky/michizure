import boto3

ec2 = boto3.client('ec2')


def lambda_handler(ev, ctx):
  print(ev)
  image_id = ev['detail']['requestParameters']['imageId']

  snapshots = ec2.describe_snapshots(
      Filters=[
          {
              'Name': 'description',
              'Values': [
                  'Created by CreateImage(*) for {}'.format(image_id),
                  'Created by CreateImage(*) for {} from *'.format(image_id),
                  (
                      'Copied for DestinationAmi {} from SourceAmi * for '
                      'SourceSnapshot *. Task created on *.').format(image_id),
              ],
          },
      ])

  for snap in snapshots['Snapshots']:
    ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])
    print('Deleted:')
    print(snap)
