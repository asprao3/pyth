#!/usr/bin/python

#Lists all reserved Instances in a particular Region say ap-southeast-1
#lists Instance ID, Launch Time and Name Tags
#surya

import boto3
import datetime
list1=[]
list2=[]
client = boto3.client('ec2',region_name="ap-southeast-1")
response1 = client.describe_instances(Filters=[
        {
            'Name': 'instance-lifecycle',
            'Values': ['spot']
        }])
for r in response1['Reservations']:
  for i in r['Instances']:
   #print(i['InstanceId'])
   #exit()
   list1.append(i['InstanceId'])

response2 = client.describe_instances()
for r in response2['Reservations']:
  for i in r['Instances']:
   #print(i['InstanceId'])
   #exit()
   list2.append(i['InstanceId'])
list = list(set(list2) - set(list1))

#	print(j)
for r in response2['Reservations']:
	for i in r['Instances']:
 		for j in list:
 			if j == i['InstanceId']:
 				if ('Tags' in i.keys()):
 					for l in i['Tags']:
 						if l['Key'] == "Name":
 							print(i['InstanceId'],"  ",i['LaunchTime'],"  ",l['Value'])

#EOF
