import boto3
import sys
import os
import csv
import json
from dotenv import load_dotenv


load_dotenv()
region_list = json.loads(os.getenv('region_name'))
f = open('result.csv', 'w')
writer = csv.writer(f)

session = boto3.Session(
    aws_access_key_id=os.getenv('aws_access_key_id'),
    aws_secret_access_key=os.getenv('aws_secret_access_key')
)

for region in region_list:

    ecs = session.client('ecs', region_name=region)

    try:
        paginator = ecs.get_paginator('list_clusters')
        response = paginator.paginate().build_full_result()
        clusters = response['clusterArns']
    except Exception as e:
        print(f'Error in fetching clusters \n {e}')
        sys.exit(0)

    print(f"found {len(clusters)} clusters in region {region}")
    for cluster in clusters:
        cluster_name = cluster.split('/')[1]
        print(f"fetching services in cluster : {cluster_name}")
        try:
            paginator = ecs.get_paginator('list_services')
            response = paginator.paginate(cluster=cluster).build_full_result()
            services = response['serviceArns']
        except Exception as e:
            print(f'Error in fetching services from cluster : {cluster_name} \n{e}')
            continue
        
        for service in services:
            temp = service.split('/')
            service_name = ""
            if len(temp) == 3:
                service_name = temp[2]
            elif len(temp) == 2:
                service_name = temp[1]

            try:
                response = ecs.describe_services(
                    cluster=cluster_name,
                    services=[service_name]
                )
                task_defintion_name = response['services'][0]['taskDefinition'].split('/')[1]
                writer.writerow([region, cluster_name, service_name, task_defintion_name])
            except Exception as e:
                print(f'Error in describing service : {service_name} from cluster : {cluster_name} \n{e}')

f.close()
print("COMPLETE!!")