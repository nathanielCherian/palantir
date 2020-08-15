# ![](docs/media/logo.svg)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status](https://travis-ci.com/nathanielCherian/palantir.svg?branch=master)](https://travis-ci.com/nathanielCherian/palantir)
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)


The Palantir Project is an attempt to aggregate and take advantage of the patterns of tradable assets. As if now Palantir has been optimized soley for bitcoin (for its high volatility) but will soon expand into all aspects of trade. 

## Background

At it's core palantir combines techinal indicators from different time periods and settings to form predictions about markets in the near-future. Then the optimal decisions are made to maximize profit. 


![](docs/media/classifier-sim-train.png)

The preceding chart shows a simulation of a model trained on data from 2020-06-01 to 2020-06-20 and actively playing on unseen data from 2020-06-21 to 2020-06-30 with 1 bitcoin and 200USD. Based on it's predictions palantir shorts or holds to maintain constant profit-growth.


## Installation

```pip install palantir-fc```

or for the latest dev version...

```pip install git+git:https://github.com/nathanielCherian/palantir.git```


## Usage

Palantir's CLI interface can be activated from terminal with

```$ palantir```

palantir also comes with two additional packages releasing you from the grasp of dependencies these include a data-scraper and a simulator.


## Problems

Palantir is still a WORK IN PROGRESS and will need more work before it has become a useful tool

* Bitcoin trading fees: After applying the maximum fee (.30% per transaction) to trades the basic machine suffers greatly. To counteract this we have to find the equilibrium between minimizing trades and maximizing profits. Note: This will not be a problem in the palantir-stocks

* Need to work on the CLI 

## Contributing

All contributions are very welcome.