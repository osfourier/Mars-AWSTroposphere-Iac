"""

Generating CloudFormation Template With Troposphere

"""

from troposphere import (
    Base64,
    ec2,
    GetAtt,
    Join,
    Output,
    Parameter,
    Ref,
    Template,
)

# Updating the Template {NOTE: the following are installed to be used:
#  > pip install ipify $ > pip install ipaddress. Line 21 and 22 needs a Linux_platform to work locally.}

# from ipaddress import ip_network
# from ipify import get_ip

t = Template ()
# t.add_description("Effective DevOps in AWS")

ApplicationPort = "443"

# PublicCidrIp = str(ip_network(get_ip()))

# Set Key-Pair parameter to use for the EC2 instance 
t.add_parameter(Parameter(
    "KeyPair",
    Description = "key-for-demoEC2",
    Type = "AWS::EC2::KeyPair::KeyName",
    ConstraintDescription = "key-for-demoEC2",
    Default = "key-for-demoEC2"
))

# Create Security Group for the EC2 to allow SSH and TCP traffic
t.add_resource (ec2.SecurityGroup (
    "SecurityGroup",
    GroupDescription = "Allow SSH and TCP/{} access".format("ApplicationPort"),
    SecurityGroupIngress = [
        ec2.SecurityGroupRule (
            IpProtocol = "tcp",
            FromPort = "22",
            ToPort = "22",
            CidrIp = "0.0.0.0/0",
        ),
        ec2.SecurityGroupRule (
            IpProtocol = "tcp",
            FromPort = "443",
            ToPort = "443",
            CidrIp = "0.0.0.0/0",
        ),
    ]
))

# Let's make use of the UserData of EC2 to setup our HelloWorld Application
ud = Base64 (Join ('\n', [
    "#!/bin/bash",
    "sudo apt install --enablerepo=epel -y nodejs",
    "wget http://bit.ly/2vEsNuc -O /home/ubuntu/helloworld.js",
    "wget http://bit.ly/2vVvT18 -O /etc/init/helloworld.conf",
    "start helloworld"
]))


# Let's create the EC2
fourierCF_EC2 = ec2.Instance (
    "fourierInstance",
    ImageId = "ami-00399ec92321828f5",
    InstanceType = "t2.micro",
    SecurityGroupIds = [Ref("SecurityGroup")],
    KeyName = Ref ("KeyPair"),
    UserData = ud
)
t.add_resource (fourierCF_EC2)

output_publicIp = Output (
    "EC2PublicIp",
    Description = "PublicIp of the Instance",
    Value = GetAtt (fourierCF_EC2, "PublicIp"),
)
t.add_output (output_publicIp)

# Another way of generating the output
t.add_output ( Output(
    "WebUrl",
    Description = "Application Endpoint",
    Value = Join ("", [
        "http://", GetAtt (fourierCF_EC2, "PublicDnsName"), 
        ":", ApplicationPort
    ])
))

print (t.to_json())

with open('helloEC2.yaml', 'w') as f:
    f.write(t.to_yaml())