from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_efs as efs,
    aws_cloudformation as cfn

)
from constructs import Construct

class GemjudgeCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

       # The code that defines your stack goes here

       # example resource
        queue = sqs.Queue(
            self, "GemjudgeCdkQueue",
            visibility_timeout=Duration.seconds(300),
        )

        #Create apigatewaysqs role 
        apigatewaysqs = iam.Role(
            self, "apigatewaysqs",
            assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSQSFullAccess")]
        )
        #Giving  permission of AmazonAPIGatewayPushToCloudWatchLogs policy explicitly
        apigatewaysqs.add_to_policy(iam.PolicyStatement(
            actions=[
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:PutLogEvents",
                "logs:GetLogEvents",
                "logs:FilterLogEvents"
            ],
            resources=["*"]
        ))

        
        #Create lambda_sqs_efs_ecr_vpc role
        lambda_sqs_efs_ecr_vpc = iam.Role(
            self, "lambda_sqs_efs_ecr_vpc",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSQSFullAccess"),
                                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonElasticFileSystemFullAccess")]
        )

        #Giving  permission of AWSLambdaBasicExecutionRole and AWSLambdaVPCAccessExecutionRole policy explicitly
        lambda_sqs_efs_ecr_vpc.add_to_policy(iam.PolicyStatement(
            actions=[
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "ec2:CreateNetworkInterface",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DeleteNetworkInterface",
                "ec2:AssignPrivateIpAddresses",
                "ec2:UnassignPrivateIpAddresses"
            ],
            resources=["*"]
        ))

        questionsqs = sqs.Queue(
            self, "questionsqs",
            queue_name="questionsqs"
        )

        submitcodesqs = sqs.Queue(
            self, "submitcodesqs",
            queue_name="submitcodesqs"
        )     
        
        
        # # Create Security Group
        # security_group = ec2.SecurityGroup(
        #     self, "SecurityGroup",
        #     vpc=vpc
        # )



        # # Create EFS File System
        # file_system = efs.FileSystem(
        #     self, "EFS",
        #     vpc=vpc,
        #     security_group=security_group,
        #     performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,
        #     encrypted=False,
        # )
        
        # # Create a mount target
        # efs.CfnMountTarget(
        #     self, "MountTarget",
        #     file_system_id=file_system.file_system_id,
        #     subnet_id=vpc.private_subnets[0].subnet_id,
        #     security_groups=[security_group.security_group_id]
        # )
        
        # # Set POSIX User ID and Root Directory Permissions
        # efs.CfnFileSystem(
        #     self, "FileSystemProperties",
        #     file_system_id=file_system.file_system_id,
        #     posix_user=efs.PosixUser(
        #         uid="1000",
        #         gid="1000"
        #     ),
        #     creation_info=efs.CreationInfo(
        #         owner_uid="1000",
        #         owner_gid="1000",
        #         permissions="755"
        #     )
        # )
        
        # # Specifying Path
        # path = "/efs"


        # vpc = ec2.Vpc(
        #     self, "DefaultVpc",
        #     max_azs=2,
        #     subnet_configuration=[
        #         ec2.SubnetConfiguration(
        #             subnet_type=ec2.SubnetType.PUBLIC,
        #             name="Public",
        #             cidr_mask=24
        #         ),
        #         ec2.SubnetConfiguration(
        #             subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
        #             name="Private",
        #             cidr_mask=24
        #         )
        #     ]
        # )


        self.vpc = ec2.Vpc(
         self, "VPC", 
         cidr="10.0.0.0/16",
         max_azs=2, 
         subnet_configuration=[
             ec2.SubnetConfiguration( name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24 ),
             ec2.SubnetConfiguration( name="Private", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED, cidr_mask=24 ) ] )

        self.eip = ec2.CfnEIP(
             self, "Eip",
             domain="vpc"
        )



        
        self.nat_gateway = ec2.CfnNatGateway( self, "NatGateway",
         allocation_id=self.eip.ref,
          subnet_id=self.vpc.public_subnets[0].subnet_id
        )


        self.nat_gateway.add_depends_on(self.eip)

