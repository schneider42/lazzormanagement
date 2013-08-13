#!/usr/bin/env python
import lazzormanagement
import ConfigParser
import logging
import sys

logging.basicConfig(level=logging.INFO)

manager = lazzormanagement.LazzorManager(sys.argv[1])
manager.run()



