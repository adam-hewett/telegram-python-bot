import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as apigateway from '@aws-cdk/aws-apigateway';
import * as logs from '@aws-cdk/aws-logs';
import * as secretsmanager from '@aws-cdk/aws-secretsmanager';

export class FatcakeBotStack extends cdk.Stack {
    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        const botName = 'fatcake-bot';
        const path = `bots/${botName}/lambda`;
        const layerPath = 'shared/lambda-layers';

        const secret = new secretsmanager.Secret(this, `${botName}-secret`);

        const botLibsLayer = new lambda.LayerVersion(this, 'bot-libs', {
            code: lambda.Code.fromAsset(`${layerPath}/bot-libs`),
            layerVersionName: 'bot-libs-layer',
            compatibleRuntimes: [lambda.Runtime.PYTHON_3_8],
        });

        const lbd = new lambda.Function(this, botName, {
            runtime: lambda.Runtime.PYTHON_3_8,
            handler: `${botName}.lambda_handler`,
            code: lambda.Code.fromAsset(`${path}/${botName}`),
            environment: {
                SECRET_ARN: secret.secretArn,
                BOT_NAME: botName,
            },
            layers: [botLibsLayer],
            logRetention: logs.RetentionDays.ONE_WEEK,
            timeout: cdk.Duration.seconds(10),
        });

        secret.grantRead(lbd);

        const restAPI = new apigateway.RestApi(this, botName, {
            restApiName: botName,
            deploy: true,
            deployOptions: {
                loggingLevel: apigateway.MethodLoggingLevel.ERROR,
            },
        });

        const apiUsagePlan = restAPI.addUsagePlan(`${botName}-usage-plan`, {
            name: `${botName}-usage-plan`,
        });

        apiUsagePlan.addApiStage({ stage: restAPI.deploymentStage });

        const botResource = restAPI.root.addResource('WpnCqakM6XBcNejEsAseDTWjhSJQgbJ2Cb6jV45ZHKCk3GRQcsnGGPdBPYM3');

        botResource.addMethod('POST', new apigateway.LambdaIntegration(lbd), {
            apiKeyRequired: false,
        });
    }
}
