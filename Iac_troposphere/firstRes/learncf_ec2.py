# Creating EC2

from __future__ import print_function
from troposphere import Base64, Join, Ref, ec2
from troposphere import Tags, ImportValue
from troposphere import Template
from troposphere.sqs import Queue, QueuePolicy

# Create the object that will generate our template
t = Template()

ud = Base64(Join('\n', [
    "Queue = ", {"Ref" : "MyQueue"}
]))

ec2_learncf_1a = ec2.Instance("ec2LearnCf1a")
ec2_learncf_1a.ImageId = "ami-00dfe2c7ce89a450b"
ec2_learncf_1a.InstanceType = "t2.micro"
ec2_learncf_1a.SubnetId = ImportValue("learncf-subnet-netlearnCf1a")
ec2_learncf_1a.Tags = Tags (
    Name ="learncf",
    Comment = "Learning CloudFormation and Troposphere"
)
ec2_learncf_1a.UserData = ud

MyQueue = t.add_resource(Queue("MyQueue"))

t.add_resource (ec2_learncf_1a)

# Finally write the template to a file
print (t.to_json())

with open('learncf-ec2.yaml', 'w') as f:
    f.write(t.to_yaml())