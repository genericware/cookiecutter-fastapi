# Standard Library ---------------------------------------------------------------------
import logging
import sys

# Third-Party --------------------------------------------------------------------------
import rapidjson as json
import structlog
from structlog.types import EventDict, Processor

# Project ------------------------------------------------------------------------------
from app.core.config import settings


def rename_event_key(_, __, event_dict: EventDict) -> EventDict:
    """
    Rename the `event` field to `message`.

    :param _:
    :param __:
    :param event_dict:
    :return:
    """
    event_dict["message"] = event_dict.pop("event")
    return event_dict


def drop_color_message_key(_, __, event_dict: EventDict) -> EventDict:
    """
    Remove the second message that uvicorn logs named `color_message`.

    :param _:
    :param __:
    :param event_dict:
    :return:
    """
    event_dict.pop("color_message", None)
    return event_dict


def tracer_injection(_, __, event_dict: EventDict) -> EventDict:
    """
    Injects trace and span IDs into log messages.

    :param _:
    :param __:
    :param event_dict:
    :return:
    """
    # todo: use opentelemetry
    # retrieve correlation ids from current tracer context
    # span = _cur_span_ctx_var.get()
    # trace_id, span_id = (
    #     (span.context.trace_id, span.context.span_id) if span else (None, None)
    # )
    trace_id, span_id = None, None

    # add ids to structlog event dictionary
    event_dict["trace_id"] = str(trace_id or 0)
    event_dict["span_id"] = str(span_id or 0)

    return event_dict


def setup_logging(json_logs: bool = False, log_level: str = "INFO") -> None:
    """
    Initialize application logging using structlog.

    :param json_logs:
    :param log_level:
    :return:
    """
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ExtraAdder(),
        drop_color_message_key,
        tracer_injection,
        timestamper,
        structlog.processors.StackInfoRenderer(),
    ]

    if json_logs:
        shared_processors.append(rename_event_key)
        shared_processors.append(structlog.processors.format_exc_info)

    structlog.configure(
        processors=shared_processors
        + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    log_renderer: structlog.types.Processor
    if json_logs:
        log_renderer = structlog.processors.JSONRenderer(serializer=json.dumps)
    else:
        log_renderer = structlog.dev.ConsoleRenderer()

    formatter = structlog.stdlib.ProcessorFormatter(
        # these only run on `logging` entries external to structlog.
        foreign_pre_chain=shared_processors,
        # these run on all entries after the pre_chain completes
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            log_renderer,
        ],
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level.upper())

    for _log in ["uvicorn", "uvicorn.error"]:
        # clears the log handlers for uvicorn loggers
        # enables propagation so messages are caught by the root logger
        logging.getLogger(_log).handlers.clear()
        logging.getLogger(_log).propagate = True

    # re-creates the access logs to add all information in the structured log.
    # prevents logs from propagating to a higher logger, rendering them silent.
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.access").propagate = False

    def handle_exception(exc_type, exc_value, exc_traceback):
        """
        Log all uncaught exceptions except for KeyboardInterrupt.

        :param exc_type:
        :param exc_value:
        :param exc_traceback:
        :return:
        """
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        root_logger.error(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = handle_exception


# config
setup_logging(json_logs=settings.log_json_format)
access_log: structlog.stdlib.BoundLogger = structlog.stdlib.get_logger("api.access")
