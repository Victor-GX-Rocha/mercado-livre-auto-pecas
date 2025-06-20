""" Log objects. """

import logging

# Log for users.

user = logging.getLogger("user")
user.setLevel(logging.INFO)
user.propagate = False

user_handler = logging.FileHandler("log.log", encoding="utf-8")
user_formatter = logging.Formatter("%(asctime)s -> %(levelname)s | %(message)s")
user_handler.setFormatter(user_formatter)
user.addHandler(user_handler)

# Log for devs.

dev = logging.getLogger("dev")
dev.setLevel(logging.INFO)
dev.propagate = False

dev_handler = logging.FileHandler("dev.log", encoding="utf-8")
dev_formatter = logging.Formatter("%(asctime)s -> %(levelname)s | %(message)s")
dev_handler.setFormatter(dev_formatter)
dev.addHandler(dev_handler)