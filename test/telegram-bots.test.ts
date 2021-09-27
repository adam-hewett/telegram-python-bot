import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as Only1Token from '../bots/o1t-bot/o1t-bot-stack';

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const o1tStack = new Only1Token.Only1TokenBotStack(app, 'O1TTestStack');
    // THEN
    expectCDK(o1tStack).to(
        matchTemplate(
            {
                Resources: {},
            },
            MatchStyle.EXACT
        )
    );
});
