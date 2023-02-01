import aws_cdk as core
import aws_cdk.assertions as assertions

from gemjudge_cdk.gemjudge_cdk_stack import GemjudgeCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in gemjudge_cdk/gemjudge_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GemjudgeCdkStack(app, "gemjudge-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
