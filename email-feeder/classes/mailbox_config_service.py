import dataclasses
import typing
import logger_service


class MailboxConfigMailConnectorConfig(typing.TypedDict):
    host: str
    port: int
    login: str
    password: str
    enable: bool
    certfile: str
    keyfile: str
    mailbox_to_monitor: str


@dataclasses.dataclass(eq=False, repr=False)
class MailboxConfigMailConnector:
    instance_name: str
    instance_config: MailboxConfigMailConnectorConfig


@dataclasses.dataclass(eq=False, repr=False)
class MailboxConfig:
    working_path: str
    mail_connectors: dict[str, MailboxConfigMailConnector]

    @staticmethod
    def form_dict(source: dict[str, typing.Any]) -> "MailboxConfig":
        if "mail-connectors" not in source:
            raise Exception("Configuration missing 'mail-connectors' section.")

        logger = logger_service.get_logger()
        mail_connectors: dict[str, MailboxConfigMailConnector]
        for connector_type, instances in source["mail-connectors"].items():
            if not isinstance(instances, dict):
                logger.warning(
                    f"Expected a dictionary of instances for connector '{connector_type}', got {type(instances)}. It will be discarded."
                )

                continue

            for instance_name, instance_config in instances.items():
                if not isinstance(instance_name, str):
                    logger.error(
                        f"Invalid type for '{connector_type}' instance's name. Expected 'str', got {type(typing.cast(object, instance_name))}. It will be discarded."
                    )
                    continue

                connector = MailboxConfigMailConnector(
                    instance_name=typing.cast(instance_name),
                    instance_config=typing.cast(
                        MailboxConfigMailConnectorConfig, instance_config
                    ),
                )

        if "working-path" not in source:
            raise Exception("Configuration missing 'working-path' section.")

        return MailboxConfig(
            mail_connectors=mail_connectors,
            working_path=source["working-path"],
        )


class MailboxConfigService:
    def __init__(self) -> None:
        pass
