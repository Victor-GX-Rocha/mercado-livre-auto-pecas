'''
""" Logger for devs. """

import logging

dev = logging.getLogger("dev")
dev.setLevel(logging.INFO)
dev.propagate = False

dev_handler = logging.FileHandler("dev.log", encoding="utf-8")
dev_formatter = logging.Formatter("%(asctime)s -> %(levelname)s | %(message)s")
dev_handler.setFormatter(dev_formatter)
dev.addHandler(dev_handler)
'''