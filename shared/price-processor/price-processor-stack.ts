import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as s3 from '@aws-cdk/aws-s3';
import * as logs from '@aws-cdk/aws-logs';
import * as events from '@aws-cdk/aws-events';
import * as targets from '@aws-cdk/aws-events-targets';

export class PriceProcessorStack extends cdk.Stack {
    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);
        const path = `shared/price-processor/lambdas`;
        const layerPath = 'shared/lambda-layers';

        const solutionName = 'price-processor';
        // const baseCoinGeckoApiUrl = 'https://api.coingecko.com/api/v3/coins/';

        const s3Bucket = new s3.Bucket(this, 'price-bucket', {
            autoDeleteObjects: true,
            blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
            bucketName: `price-processor-${cdk.Stack.of(this).region}`,
            encryption: s3.BucketEncryption.S3_MANAGED,
            removalPolicy: cdk.RemovalPolicy.DESTROY,
        });

        const priceProcessorLibsLayer = new lambda.LayerVersion(this, 'price-processor-libs', {
            code: lambda.Code.fromAsset(`${layerPath}/price-processor-libs`),
            layerVersionName: 'price-processor-libs-layer',
            compatibleRuntimes: [lambda.Runtime.NODEJS_14_X, lambda.Runtime.PYTHON_3_8],
        });

        const lbd = new lambda.Function(this, `${solutionName}-lambda`, {
            runtime: lambda.Runtime.PYTHON_3_8,
            handler: `${solutionName}.lambda_handler`,
            code: lambda.Code.fromAsset(`${path}/${solutionName}`),
            environment: {
                MPLCONFIGDIR: '/tmp',
                BUCKET_NAME: s3Bucket.bucketName,
            },
            layers: [priceProcessorLibsLayer],
            logRetention: logs.RetentionDays.ONE_WEEK,
            timeout: cdk.Duration.seconds(60),
            memorySize: 2048,
        });

        s3Bucket.grantReadWrite(lbd);

        const crowPriceLbd = new lambda.Function(this, `${solutionName}-crow-price-lambda`, {
            runtime: lambda.Runtime.PYTHON_3_8,
            handler: `crow-${solutionName}.lambda_handler`,
            code: lambda.Code.fromAsset(`${path}/crow-price-processor`),
            environment: {
                MPLCONFIGDIR: '/tmp',
                BUCKET_NAME: s3Bucket.bucketName,
            },
            layers: [priceProcessorLibsLayer],
            logRetention: logs.RetentionDays.ONE_WEEK,
            timeout: cdk.Duration.seconds(60),
            memorySize: 2048,
        });

        s3Bucket.grantReadWrite(crowPriceLbd);

        const rule = new events.Rule(this, 'schedule-rule', {
            schedule: events.Schedule.rate(cdk.Duration.minutes(1)),
        });
        rule.addTarget(new targets.LambdaFunction(lbd));
        rule.addTarget(new targets.LambdaFunction(crowPriceLbd));
    }
}
