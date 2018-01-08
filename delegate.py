#! /usr/bin/env python3
# coding=utf-8
import time
import configargparse
import os
import json
import logging
import statistics
import sys

from redeemer import Delegator, Stats

parser = configargparse.ArgumentParser('redeemer', formatter_class=configargparse.ArgumentDefaultsRawHelpFormatter)
parser.add_argument('--account', type=str, help='Account to perform delegations for')
parser.add_argument('--wif', type=configargparse.FileType('r'), help='An active WIF for account. The flag expects a path to a file. The environment variable REDEEMER_WIF will be checked for a literal WIF also.')
parser.add_argument('--log_level', type=str, default='INFO')
parser.add_argument('--dry_run', type=bool, default=True, help='Set this to false to actually broadcast transactions')
parser.add_argument('--interval', type=int, default=60, help='Time in seconds to wait between polling for new delegations')

args = parser.parse_args()

logger = logging.getLogger("redeemer")
logging.basicConfig(level=logging.getLevelName(args.log_level))

wifs = []
if args.wif:
    logger.info('Using wif from file %s' % args.wif)
    wifs = args.wif.read().strip().split(':')
elif os.environ.get('REDEEMER_WIF') is not None:
    logger.info('Using wif from environment variable REDEEMER_WIF')
    wifs = os.environ.get('REDEEMER_WIF').strip().split(':')
else:
    logger.warn('You have not specified a wif; signing transactions is not possible!')

if args.dry_run:
  logger.warn("dry run mode; no transactions will be broadcast")

delegator = Delegator(logger=logger)

while True:
  last_idx = ""
  while True:
    try:
      logger.info("at index %s", last_idx)
      results, last_idx = delegator.delegate(args.account, last_idx=last_idx, dry_run=args.dry_run, wifs=wifs)
      gather_stats(results)
      if len(results) == 0:
        break
    except Exception as e:
      logger.exception("failed to delegate")
      break
  logger.info("Waiting %d seconds until the next run", args.interval)
  time.sleep(args.interval)

