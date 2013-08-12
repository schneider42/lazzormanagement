#!/usr/bin/env python
import lazzormanagement
import ConfigParser
import logging
import sys

logging.basicConfig(level=logging.INFO)
config = ConfigParser.RawConfigParser()
config.read(sys.argv[1])


manager = lazzormanagement.LazzorManager(config)
manager.run()



