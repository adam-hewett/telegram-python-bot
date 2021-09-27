import { expect as expectCDK, matchTemplate, MatchStyle } from "@aws-cdk/assert";
import * as cdk from "@aws-cdk/core";
import * as Only1Token from "../bots/only-1-token-stack";

test("Empty Stack", () => {
    const app = new cdk.App();
    // WHEN
    const stack = new Only1Token.Only1TokenStack(app, "MyTestStack");
    // THEN
    expectCDK(stack).to(
        matchTemplate(
            {
                Resources: {},
            },
            MatchStyle.EXACT
        )
    );
});
