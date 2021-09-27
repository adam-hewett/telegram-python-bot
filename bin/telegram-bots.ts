#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';

import { Only1TokenBotStack } from '../bots/o1t-bot/o1t-bot-stack';
const o1tApp = new cdk.App();
new Only1TokenBotStack(o1tApp, 'Only1TokenBotStack', {});

import { FatcakeBotStack } from '../bots/fatcake-bot/fatcake-bot-stack';
const fatcakeApp = new cdk.App();
new FatcakeBotStack(fatcakeApp, 'FatcakeBotStack', {});
