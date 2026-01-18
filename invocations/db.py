import os

import invoke
from . import _config, django, printing


@invoke.task
def load_db_dump(
    context: invoke.Context,
    dbname: str | None = None,
    host: str | None = None,
    port: str | None = None,
    username: str | None = None,
    password: str | None = None,
    file: str = "",
    additional_params: str = "",
) -> None:
    """Load db dump to local db."""
    os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.local"
    from django.conf import settings

    db_settings = settings.DATABASES["default"]
    dbname = dbname or db_settings["NAME"]
    host = host or db_settings["HOST"]
    port = port or db_settings["PORT"]
    username = username or db_settings["USER"]
    password = password or db_settings["PASSWORD"]
    config = _config.Config.from_context(context)
    django.resetdb(context, apply_migrations=False)
    context.run(
        config.db.load_dump_command.format(
            dbname=dbname,
            host=host,
            port=port,
            username=username,
            file=file or config.db.dump_filename,
            additional_params=additional_params
            or config.db.load_additional_params,
        ),
        watchers=(
            invoke.Responder(
                pattern=config.db.password_pattern,
                response=f"{password}\n",
            ),
        ),
    )
    printing.print_success("DB is ready for use")


@invoke.task
def backup_local_db(
    context: invoke.Context,
    dbname: str,
    host: str,
    port: str,
    username: str,
    password: str,
    file: str = "",
    additional_params: str = "",
) -> None:
    """Back up local db."""
    config = _config.Config.from_context(context)
    printing.print_success("Creating backup of local db.")
    context.run(
        config.db.dump_command.format(
            dbname=dbname,
            host=host,
            port=port,
            username=username,
            file=file or config.db.dump_filename,
            additional_params=additional_params
            or config.db.dump_additional_params,
        ),
        watchers=(
            invoke.Responder(
                pattern=config.db.password_pattern,
                response=f"{password}\n",
            ),
        ),
    )
