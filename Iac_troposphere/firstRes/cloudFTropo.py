from __future__ import print_function
from re import sub

# Crating aws_subnet using troposphere

from troposphere import Cidr, ec2 
from troposphere import Tags, GetAtt, Ref, Sub, Export
from troposphere import Template, Output

# Create the Object that will generate the template

t = Template()

# Define Resources that you want CloudFormation to generate
# define the first Subnet.
# NOTE:: that 'Subnet()' is in the ec2 module
net_learncf_1a = ec2.Subnet("netlearnCf1a")
net_learncf_1a.AvailabilityZone = "us-east-2a"
net_learncf_1a.CidrBlock = "10.0.1.0/24"
net_learncf_1a.VpcId = "vpc-0b5f0305b0120b17d"

# Tags can be added
net_learncf_1a.Tags = [
    {"Key": "Name", "Value": "learncf-1a"},
    {"Key": "Comment", "Value": "CloudFormation+Troposphere"}
]
t.add_resource(net_learncf_1a)

# We can achieve the same thing using the parameters to Subnet() function instead of the properties
# of the object created by Subnet()

net_learncf_1b = ec2.Subnet (
    "netlearnCf1b",
    AvailabilityZone = "us-east-2b",
    CidrBlock = "10.0.2.0/24",
    VpcId = GetAtt(net_learncf_1a, "VpcId"),
    Tags = Tags(
        Name = "learncf-1b",
        Comment = "CloudFormation+Tropospere"
    )
)
t.add_resource(net_learncf_1b)

# Output Section will exporrt the Subnet IDs to be used by other stacks
out_net_learncf_1a = Output("outNetLearnCf1a")

# Ref is another CloudFormation intrinsic function:
# If pointed to a subnet to a subnet, Ref will return the subnet ID:
out_net_learncf_1a.Value = Ref(net_learncf_1a)

out_net_learncf_1a.Export = Export(Sub(
    "${AWS::StackName}-" + net_learncf_1a.title
))

# Similar output for the second subnet

out_net_learncf_1b = Output("outNetLearnCf1b")
out_net_learncf_1b.Value = Ref(net_learncf_1b)
out_net_learncf_1b.Export = Export(Sub(
    "${AWS::StackName}-" + net_learncf_1b.title
))

# Add outputs to template
t.add_output(out_net_learncf_1a)
t.add_output(out_net_learncf_1b)

# Write the template to a file

print (t.to_json())

with open('learncf-subnet.yaml', 'w') as f:
    f.write(t.to_yaml())