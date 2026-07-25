import logging

import structlog

logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)

logger = structlog.get_logger()
