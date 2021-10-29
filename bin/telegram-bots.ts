#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
const app = new cdk.App();

import { PriceProcessorStack } from '../shared/price-processor/price-processor-stack';
new PriceProcessorStack(app, 'PriceProcessorStack', {});

import { TestBotStack } from '../bots/test-bot/test-bot-stack';
new TestBotStack(app, 'TestBotStack', {});

import { Only1TokenBotStack } from '../bots/o1t-bot/o1t-bot-stack';
new Only1TokenBotStack(app, 'Only1TokenBotStack', {});

import { FatcakeBotStack } from '../bots/fatcake-bot/fatcake-bot-stack';
new FatcakeBotStack(app, 'FatcakeBotStack', {});

import { FateTokenBotStack } from '../bots/fatetoken-bot/fatetoken-bot-stack';
new FateTokenBotStack(app, 'FateTokenBotStack', {});

import { InfiniteOneBotStack } from '../bots/infiniteone-bot/infiniteone-bot-stack';
new InfiniteOneBotStack(app, 'InfiniteOneBotStack', {});

import { SeaChainTokenBotStack } from '../bots/seachaintoken-bot/seachaintoken-bot-stack';
new SeaChainTokenBotStack(app, 'SeaChainTokenBotStack', {});

import { ProjectQuantumBotStack } from '../bots/projectquantum-bot/projectquantum-bot-stack';
new ProjectQuantumBotStack(app, 'ProjectQuantumBotStack', {});
