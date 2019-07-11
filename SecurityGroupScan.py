#!/usr/bin/python


import boto3
import re
import io
import csv
#from datetime import datetime, timedelta


# encoding=utf8
ec2_fileout = "securityGroupslistProdSpecificIO.csv";
cs = open(ec2_fileout, "w");
columnTitleRow = ", SecurityGroupId, Protocol, FromPort, ToPort, Description, Tags\n";
cs.write(columnTitleRow);

def GetEc2(region):
 csv_arr = []
 #remove the comments when you are hard coding credentials, by default the code takes the default profile 
 #aws_access_key_id =
 #aws_secret_access_key =
 #ec2client = boto3.client('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=region);
 ec2client = boto3.client('ec2', region_name=region)
 resp = ec2client.describe_security_groups();
 print("Instances that have inbound open to world")
 print("in Region: " + region)
 csv_arr.append('\n Region:' + region)
 for i in resp['SecurityGroups']:
  print ""
  for j in i['IpPermissions']:
      for k in j['IpRanges']:
#        print k['CidrIp']
        if (k['CidrIp'] == '0.0.0.0/32'):
            csv_arr.append('\n')
            print i['GroupId']
            csv_arr.append(i['GroupId'])
            if j['IpProtocol'] == '-1':
                print" protocol: ALL "
                csv_arr.append(" ALL ")
            else:
                print "protocol: " + j['IpProtocol']
                csv_arr.append(j['IpProtocol'])
                print (j['FromPort'])
                print (j['ToPort'])
                csv_arr.append(j['FromPort'])
                csv_arr.append(j['ToPort'])
            flag1 = True
            print (i['Description'])
            csv_arr.append(i['Description'])
            if ('Tags' in i.keys()):
                for l in i['Tags']:
                    print ('Key: ' + l['Key'] + ' Value: ' + l['Value'])
                    csv_arr.append('Key: ' + l['Key'] + ' Value: ' + l['Value'])
  csv_arr.append('\n')

#	if(i[0]['IpPermissions'][0]['IpRanges']['CidrIp']=="0.0.0.0/0" or i[0]['IpPermissions'][0]['Ipv6Ranges']['CidrIpv6']=="::/0"):
#		print(i['GroupTd'])
#		print(i['GroupName'])

#		print("")
 return csv_arr

#region = "us-west-2"
region_list=['us-east-2','us-east-1','us-west-1','us-west-2','ap-southeast-2','ca-central-1','eu-west-1']
for l in region_list:
 cs.write(','.join(map(str, GetEc2(l))))
#cs.write(','.join(map(str, GetEc2(region))))
cs.close();
#---------------------------------------------------------------------------------------------------------
