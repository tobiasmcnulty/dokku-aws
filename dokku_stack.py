import troposphere.ec2 as ec2
from troposphere import (
    Base64,
    FindInMap,
    Join,
    Output,
    Parameter,
    Ref,
    Tags,
    Template
)

template = Template()

instance_type = template.add_parameter(Parameter(
    "InstanceType",
    Description="The instance type",
    Type="String",
    Default="t2.micro",
    AllowedValues=[
        't2.nano',
        't2.micro',
        't2.small',
        't2.medium',
        't2.large',
        't2.xlarge',
        't2.2xlarge',
        'm4.large',
        'm4.xlarge',
        'm4.2xlarge',
        'm4.4xlarge',
        'm4.10xlarge',
        'm4.16xlarge',
        'm3.medium',
        'm3.large',
        'm3.xlarge',
        'm3.2xlarge',
        'c4.large',
        'c4.xlarge',
        'c4.2xlarge',
        'c4.4xlarge',
        'c4.8xlarge',
        'c3.large',
        'c3.xlarge',
        'c3.2xlarge',
        'c3.4xlarge',
        'c3.8xlarge',
        'p2.xlarge',
        'p2.8xlarge',
        'p2.16xlarge',
        'g2.2xlarge',
        'g2.8xlarge',
        'x1.16large',
        'x1.32xlarge',
        'r4.large',
        'r4.xlarge',
        'r4.2xlarge',
        'r4.4xlarge',
        'r4.8xlarge',
        'r4.16xlarge',
        'r3.large',
        'r3.xlarge',
        'r3.2xlarge',
        'r3.4xlarge',
        'r3.8xlarge',
        'i3.large',
        'i3.xlarge',
        'i3.2xlarge',
        'i3.4xlarge',
        'i3.8xlarge',
        'i3.16large',
        'd2.xlarge',
        'd2.2xlarge',
        'd2.4xlarge',
        'd2.8xlarge',
        'f1.2xlarge',
        'f1.16xlarge',
    ]
))

key_name = template.add_parameter(Parameter(
    "KeyName",
    Description="Name of an existing EC2 KeyPair to enable SSH access to "
                "the AWS EC2 instances",
    Type="AWS::EC2::KeyPair::KeyName",
    ConstraintDescription="must be the name of an existing EC2 KeyPair."
))

dokku_version = template.add_parameter(Parameter(
    "DokkuVersion",
    Description="Dokku version to install, e.g., \"v0.10.4\" (see https://github.com/dokku/dokku/releases).",
    Type="String",
    Default="v0.10.4",
))

dokku_web_config = template.add_parameter(Parameter(
    "DokkuWebConfig",
    Description="Whether or not to enable the Dokku web config (defaults to false for security reasons).",
    Type="String",
    AllowedValues=["true", "false"],
    Default="false",
))

dokku_vhost_enable = template.add_parameter(Parameter(
    "DokkuVhostEnable",
    Description="Whether or not to use vhost-based deployments (e.g., foo.domain.name).",
    Type="String",
    AllowedValues=["true", "false"],
    Default="true",
))

dokku_hostname = template.add_parameter(Parameter(
    "DokkuHostname",
    Description="Hostname for Dokku installation (e.g., \"dokku.me\").",
    Type="String",
    Default="",
))

root_size = template.add_parameter(Parameter(
    "RootVolumeSize",
    Description="The size of the root volumne (in GB).",
    Type="Number",
    Default="30",
))

ssh_cidr = template.add_parameter(Parameter(
    "SshCidr",
    Description="CIDR block from which to allow SSH access. Restrict this to your IP, if possible.",
    Type="String",
    Default="0.0.0.0/0",
))

# "16.04 hvm ssd" AMIs from https://cloud-images.ubuntu.com/locator/ec2/
template.add_mapping('RegionMap', {
    "ap-northeast-1": {"AMI": "ami-0417e362"},
    "ap-northeast-2": {"AMI": "ami-536ab33d"},
    "ap-south-1": {"AMI": "ami-df413bb0"},
    "ap-southeast-1": {"AMI": "ami-9f28b3fc"},
    "ap-southeast-2": {"AMI": "ami-bb1901d8"},
    "ca-central-1": {"AMI": "ami-a9c27ccd"},
    "eu-central-1": {"AMI": "ami-958128fa"},
    "eu-west-1": {"AMI": "ami-674cbc1e"},
    "eu-west-2": {"AMI": "ami-03998867"},
    "sa-east-1": {"AMI": "ami-a41869c8"},
    "us-east-1": {"AMI": "ami-1d4e7a66"},
    "us-east-2": {"AMI": "ami-dbbd9dbe"},
    "us-west-1": {"AMI": "ami-969ab1f6"},
    "us-west-2": {"AMI": "ami-8803e0f0"},
})

security_group = template.add_resource(ec2.SecurityGroup(
    'SecurityGroup',
    GroupDescription='Allows SSH access from SshCidr and HTTP/HTTPS access from anywhere.',
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(
            IpProtocol='tcp',
            FromPort=22,
            ToPort=22,
            CidrIp=Ref(ssh_cidr),
        ),
        ec2.SecurityGroupRule(
            IpProtocol='tcp',
            FromPort=80,
            ToPort=80,
            CidrIp='0.0.0.0/0',
        ),
        ec2.SecurityGroupRule(
            IpProtocol='tcp',
            FromPort=443,
            ToPort=443,
            CidrIp='0.0.0.0/0',
        ),
    ]
))

eip = template.add_resource(ec2.EIP("Eip"))

ec2_instance = template.add_resource(ec2.Instance(
    'Ec2Instance',
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    InstanceType=Ref(instance_type),
    KeyName=Ref(key_name),
    SecurityGroups=[Ref(security_group)],
    BlockDeviceMappings=[
        ec2.BlockDeviceMapping(
            DeviceName="/dev/sda1",
            Ebs=ec2.EBSBlockDevice(
                VolumeSize=Ref(root_size),
            )
        ),
    ],
    UserData=Base64(Join('', [
        '#!/bin/bash\n',
        'sudo apt-get update\n',
        'wget https://raw.githubusercontent.com/dokku/dokku/', Ref(dokku_version), '/bootstrap.sh\n',
        'sudo',
        ' DOKKU_TAG=', Ref(dokku_version),
        ' DOKKU_VHOST_ENABLE=', Ref(dokku_vhost_enable),
        ' DOKKU_WEB_CONFIG=', Ref(dokku_web_config),
        ' DOKKU_HOSTNAME=', Ref(dokku_hostname),
        ' DOKKU_KEY_FILE=/home/ubuntu/.ssh/authorized_keys',  # use the key configured by key_name
        ' bash bootstrap.sh\n',
    ])),
    Tags=Tags(
        Name=Ref("AWS::StackName"),
    ),
))

eip_assoc = template.add_resource(ec2.EIPAssociation(
    "EipAssociation",
    InstanceId=Ref(ec2_instance),
    EIP=Ref(eip),
))

template.add_output([
    Output(
        "PublicIP",
        Description="Public IP address of Elastic IP associated with the Dokku instance",
        Value=Ref(eip),
    ),
])

print(template.to_json())
