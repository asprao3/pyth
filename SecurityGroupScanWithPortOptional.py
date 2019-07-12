#!/usr/bin/python
#Author: surya
import boto3
import re
import io
import csv
import sys
##################################################################################################################
#Guidelines: execute this code from command line...
#give port number if you want the code to scan rules with port number
###################################################################################################################
# encoding=utf8

def GetEc2withPort(region, portNo):
 csv_arr = []
#remove the comments when you are hard coding credentials, by default the code takes the default profile 
 #aws_access_key_id =
 #aws_secret_access_key =
 #ec2client = boto3.client('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=region);

# session = boto3.Session(profile_name='userprod')
# dev_s3_client = session.client('ec2',region_name=region)
# resp = dev_s3_client.describe_security_groups();
 ec2client = boto3.client('ec2',region_name=region);
 resp = ec2client.describe_security_groups();
 print("Instances that have Rules with port : "+ str(portNo))
 print("in Region: " + region)
 csv_arr.append('\n Region:' + region)
 for i in resp['SecurityGroups']:
  for j in i['IpPermissions']:
      for k in j['IpRanges']:
        if ('FromPort' in j.keys()):
#        print k['CidrIp']
            if (j['FromPort'] == portNo):
#           if (j['FromPort'] == int(portNo)):
                csv_arr.append('\n')
                print ""
                print i['GroupId']
                csv_arr.append(i['GroupId'])
                print "protocol: " + j['IpProtocol']
                csv_arr.append(j['IpProtocol'])
                print (j['FromPort'])
                print (j['ToPort'])
                print ((k['CidrIp']))
                csv_arr.append(j['FromPort'])
                csv_arr.append(j['ToPort'])
                csv_arr.append(k['CidrIp'])
                print (i['Description'])
                csv_arr.append(i['Description'])
                if ('Tags' in i.keys()):
                    for l in i['Tags']:
                        print ('Key: ' + l['Key'] + ' Value: ' + l['Value'])
                        csv_arr.append('Key: ' + l['Key'] + ' Value: ' + l['Value'])
#  csv_arr.append('\n')

#	if(i[0]['IpPermissions'][0]['IpRanges']['CidrIp']=="0.0.0.0/0" or i[0]['IpPermissions'][0]['Ipv6Ranges']['CidrIpv6']=="::/0"):
#		print(i['GroupTd'])
#		print(i['GroupName'])

#		print("")
 return csv_arr

def GetEc2(region):
 csv_arr = []
 #remove the comments when you are hard coding credentials, by default the code takes the default profile
 #aws_access_key_id =
 #aws_secret_access_key =
 #ec2client = boto3.client('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=region);

 # session = boto3.Session(profile_name='userprod')
 # dev_s3_client = session.client('ec2',region_name=region)
 # resp = dev_s3_client.describe_security_groups();
 ec2client = boto3.client('ec2',region_name=region);
 resp = ec2client.describe_security_groups();
 print("Instances that have inbound open to world")
 print("in Region: " + region)
 csv_arr.append('\n Region:' + region)
 for i in resp['SecurityGroups']:
  for j in i['IpPermissions']:
      for k in j['IpRanges']:
#        print k['CidrIp']
        if ('CidrIp' in k.keys()):
            if (k['CidrIp'] == '0.0.0.0/0'):
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
                    print ((k['CidrIp']))
                    csv_arr.append(j['FromPort'])
                    csv_arr.append(j['ToPort'])
                    csv_arr.append(k['CidrIp'])
                print (i['Description'])
                csv_arr.append(i['Description'])
                if ('Tags' in i.keys()):
                    for l in i['Tags']:
                        print ('Key: ' + l['Key'] + ' Value: ' + l['Value'])
                        csv_arr.append('Key: ' + l['Key'] + ' Value: ' + l['Value'])
 return csv_arr

if (len(sys.argv) > 1):
    portNo =  sys.argv[1]
    print('Port number to search is : '+ portNo)
    ec2_fileout = "securityGroupslistSpecificPort.csv";
    cs = open(ec2_fileout, "w");
    columnTitleRow = ", SecurityGroupId, Protocol, FromPort, ToPort, Cidr, Description, Tags\n";
    cs.write(columnTitleRow);

    region_list = ['us-east-2', 'us-east-1', 'us-west-1', 'us-west-2', 'ap-southeast-2', 'ca-central-1', 'eu-west-1']
    for l in region_list:
        cs.write(','.join(map(str, GetEc2withPort(l, int(portNo)))))
    cs.close()
    print ("find the list in " + ec2_fileout)
else:
    ec2_fileout1 = "securityGroupslistInboundOpenToTheWorld.csv";
    cs1 = open(ec2_fileout1, "w");
    columnTitleRow = ", SecurityGroupId, Protocol, FromPort, ToPort, Cidr, Description, Tags\n";
    cs1.write(columnTitleRow);
    region_list = ['us-east-2', 'us-east-1', 'us-west-1', 'us-west-2', 'ap-southeast-2', 'ca-central-1', 'eu-west-1']
    for l in region_list:
        cs1.write(','.join(map(str, GetEc2(l))))
    print ("find the list in "+ec2_fileout1)
    cs1.close()
#region = "us-west-2"
#cs.write(','.join(map(str, GetEc2(region))))

#---------------------------------------------------------------------------------------------------------
