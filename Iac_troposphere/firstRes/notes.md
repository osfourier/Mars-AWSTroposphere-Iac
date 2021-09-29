Creating stacks
    aws cloudformation create-stack --stack-name learncf-ec2 --template-body file://learncf-ec2.yaml 
    aws cloudformation create-stack --stack-name learncf-subnet --template-body file://learncf-subnet.yaml
Deleting stack
    aws cloudformation delete-stack --stack-name learncf-subnet
    aws cloudformation delete-stack --stack-name learncf-ec2 
Updating Stacks
    aws cloudformation update-stack --stack-name helloEC2 --template-body file://helloEC2.yaml

=================================================================
GENERATING SSH KEY-PAIR BYSELF
Navigate to the folder for you want to use for your keys; then run this command on your terminal;
    ssh-keygen -t rsa -b 2048
Then upload the private key{.rsa} to your aws cloud.
Create your ec2 instance using the uploaded key and enable ssh on port 22
Click connect tab on your instance page and slelect ssh-client, then copy the command and paste on your cmd-line. Edit the part with quote and remove .pem 