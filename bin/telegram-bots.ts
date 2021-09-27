#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
const app = new cdk.App();

import { Only1TokenBotStack } from '../bots/o1t-bot/o1t-bot-stack';
new Only1TokenBotStack(app, 'Only1TokenBotStack', {});

import { FatcakeBotStack } from '../bots/fatcake-bot/fatcake-bot-stack';
new FatcakeBotStack(app, 'FatcakeBotStack', {});
