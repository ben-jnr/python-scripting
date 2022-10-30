import boto3
import csv
from dotenv import load_dotenv
import json
import os


load_dotenv()
region_list = json.loads(os.getenv('region_name'))
f = open('result.csv', 'w')
writer = csv.writer(f)

session = boto3.Session(
    aws_access_key_id=os.getenv('aws_access_key_id'),
    aws_secret_access_key=os.getenv('aws_secret_access_key')
)

for region in region_list:

    ssm = session.client('ssm', region_name=region)
    next_token = ' '

    print(f"Fetching SSM parameters in region:{region}")
    while next_token is not None:
        response = ssm.describe_parameters(NextToken=next_token)
        for parameter in response['Parameters']:
            row = [region]
            row.append(parameter['Name'])
            row.append(parameter['Type'])
            tag_response = ssm.list_tags_for_resource(
                ResourceType='Parameter',
                ResourceId=parameter['Name']
            )
            for tag in tag_response['TagList']:
                row.append(f"{tag['Key']}={tag['Value']}")
            writer.writerow(row)
        next_token = response.get('NextToken', None)
        
print('COMPLETE')
