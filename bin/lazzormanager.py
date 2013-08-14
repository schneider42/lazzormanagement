#!/usr/bin/env python
import lazzormanagement
import ConfigParser
import logging
import sys
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level = logging.INFO, format = FORMAT)

manager = lazzormanagement.LazzorManager(sys.argv[1])
manager.run()



