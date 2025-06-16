""" Log for users. """

import logging

log = logging.getLogger("log")
log.setLevel(logging.INFO)
log.propagate = False

dev_handler = logging.FileHandler("log.log", encoding="utf-8")
dev_formatter = logging.Formatter("%(asctime)s -> %(levelname)s | %(message)s")
dev_handler.setFormatter(dev_formatter)
log.addHandler(dev_handler)
