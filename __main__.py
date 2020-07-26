import pulumi
import pulumi_aws as aws

vpc = aws.ec2.Vpc("x-vpc", 
    cidr_block = "10.0.0.0/16",
    enable_dns_hostnames = True,
    tags = {"Name": "x-vpc"}
)

internet_gateway = aws.ec2.InternetGateway("x-internetgateway",
    vpc_id = vpc.id,
    tags = {"Name": "x-internetgateway"}
)

subnet = aws.ec2.Subnet("x-subnet",
    vpc_id = vpc.id,
    cidr_block = "10.0.1.0/24",
    map_public_ip_on_launch = True,
    #availability_zone = "us-east-1a",
    tags = {"Name": "x-subnet"}
)

route_table = aws.ec2.RouteTable("x-routetable",
    vpc_id = vpc.id,
    routes = [
        {
            "cidr_block": "0.0.0.0/0",
            "gateway_id": internet_gateway.id,
        },
    ],
    tags = {"Name": "x-routetable"}
)

# https://github.com/pulumi/pulumi-aws/issues/436
route_table_association = aws.ec2.RouteTableAssociation("x-routetableassociation",
    route_table_id = route_table.id,
    subnet_id = subnet.id,
)

size = 't2.micro'
ami = aws.get_ami(most_recent="true",
                  owners=["137112412989"],
                  filters=[{"name":"name","values":["amzn-ami-hvm-*"]}])

security_group = aws.ec2.SecurityGroup("x-securitygroup",
    description = 'enable: ssh, http',
    vpc_id = vpc.id,
    ingress = [
        { 'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': ['0.0.0.0/0'] },
        { 'protocol': 'tcp', 'from_port': 80, 'to_port': 80, 'cidr_blocks': ['0.0.0.0/0'] }
    ],
    tags = {"Name": "x-securitygroup"}
)

# ssh-keygen -q -t rsa -f test -m PEM -N "" <<< y
with open('test.pub', 'r') as key_file:
    public_key_string = key_file.read()

key_pair = aws.ec2.KeyPair('x-keypair',
    public_key = public_key_string,
    key_name = "test",
    tags = {"Name": "x-keypair"}
)

user_data_script = """
#!/bin/bash
echo "Hello, World!!" > index.html
nohup python -m SimpleHTTPServer 80 &
"""

instance = aws.ec2.Instance('x-instance',
    instance_type = size,
    vpc_security_group_ids = [security_group.id],
    ami = ami.id,
    subnet_id = subnet.id,
    key_name = key_pair.key_name,
    user_data = user_data_script,
    tags = {"Name": "x-instance"}
)

pulumi.export('publicIp', instance.public_ip)
pulumi.export('publicHostName', instance.public_dns)
