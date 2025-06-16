""" Logger for devs. """

import logging

dev_log = logging.getLogger("dev_log")
dev_log.setLevel(logging.INFO)
dev_log.propagate = False

dev_handler = logging.FileHandler("dev.log", encoding="utf-8")
dev_formatter = logging.Formatter("%(asctime)s -> %(levelname)s | %(message)s")
dev_handler.setFormatter(dev_formatter)
dev_log.addHandler(dev_handler)
