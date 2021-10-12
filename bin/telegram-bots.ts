#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
const app = new cdk.App();

import { TestBotStack } from '../bots/test-bot/test-bot-stack';
new TestBotStack(app, 'TestBotStack', {});

import { Only1TokenBotStack } from '../bots/o1t-bot/o1t-bot-stack';
new Only1TokenBotStack(app, 'Only1TokenBotStack', {});

import { FatcakeBotStack } from '../bots/fatcake-bot/fatcake-bot-stack';
new FatcakeBotStack(app, 'FatcakeBotStack', {});

import { FateTokenBotStack } from '../bots/fatetoken-bot/fatetoken-bot-stack';
new FateTokenBotStack(app, 'FateTokenBotStack', {});
