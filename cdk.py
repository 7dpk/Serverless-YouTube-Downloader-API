from aws_cdk import core
from aws_cdk.aws_lambda import (
    Function,
    Code,
    Runtime,
    LayerVersion,
)
from aws_cdk.aws_dynamodb import (
    Attribute,
    AttributeType,
    Table,
)

REGION = ''
ACCOUNT_ID = ''
VERSION = ''
class MyCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda function
        function = Function(
            self,
            "MyLambdaFunction",
            runtime=Runtime.PYTHON_3_8,
            handler="lambda_handler",
            code=Code.from_asset("lambda"),
            layers=[
                LayerVersion.from_layer_version_arn(
                    self,
                    "YtDlpLayer",
                    f"arn:aws:lambda:{REGION}:{ACCOUNT_ID}:layer:yt_dlp:{VERSION}"
                ),
                LayerVersion.from_layer_version_arn(
                    self,
                    "RequestsLayer",
                    f"arn:aws:lambda:{REGION}:{ACCOUNT_ID}:layer:requests:{VERSION}"
                )
            ],
        )

        # DynamoDB table
        table = Table(
            self,
            "VideoCacheTable",
            table_name="video_cache",
            partition_key=Attribute(
                name="url",
                type=AttributeType.STRING,
            ),
            time_to_live_attribute="timestamp",
        )

        # Grant permissions to Lambda function to access DynamoDB table
        table.grant_read_write_data(function)


app = core.App()
MyCdkStack(app, "MyCdkStack")

app.synth()
