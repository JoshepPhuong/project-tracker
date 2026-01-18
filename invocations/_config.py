# Default and additional config for project invocations

import collections.abc
import contextlib
import dataclasses
import typing

import invoke


@contextlib.contextmanager
def context_override(
    context: invoke.Context,
    **config,
) -> collections.abc.Generator[invoke.Context, typing.Any, None]:
    """Temporary override context settings."""
    old_context_config = {key: context.config.get(key) for key in config}
    context.config.update(**config)
    try:
        yield context
    finally:
        context.config.update(**old_context_config)


@dataclasses.dataclass
class SystemSettings:
    """Settings for system module."""

    settings_template: str = "config/settings/.env.local"
    save_settings_from_template_to: str = "config/settings/.env"
    vs_code_settings_template: str = ".vscode/recommended_settings.json"


@dataclasses.dataclass
class GitSettings:
    """Settings for git module."""

    merge_ff: str = "false"
    pull_ff: str = "only"
    copy_commit_template: str = (
        "[automated-commit]: {action}\n\n"
        "copy: {original_path}\n"
        "to:\n* {destination_paths}\n\n"
        "{project_task}"
    )
    copy_init_message_template: str = (
        "Copy {original_path} to:\n"
        "* {destination_paths}\n\n"
        "Count of created commits: {commits_count}"
    )


@dataclasses.dataclass
class PreCommitSettings:
    """Settings for pre-commit module."""

    hooks: collections.abc.Sequence[str] = (
        "pre-commit",
        "pre-push",
        "commit-msg",
    )


@dataclasses.dataclass
class PythonSettings:
    """Settings for python module."""

    entry: str = "python"
    docker_service: str = "app"
    docker_service_params: str = "--rm"
    mypy_entry: str = "-m mypy"
    pytest_entry: str = "-m pytest"


@dataclasses.dataclass
class DockerSettings:
    """Settings for docker module."""

    compose_cmd = "docker compose"
    main_containers: collections.abc.Sequence[str] = (
        "postgres",
        "redis",
        "mailpit",
        "minio",
        "minio-create-bucket",
    )
    build_image_tag: str = ""
    buildpack_builder: str = "paketobuildpacks/builder:base"
    buildpack_runner: str = "paketobuildpacks/run:base"
    buildpack_requirements_path: str = "requirements"


@dataclasses.dataclass
class GitHubActionsSettings:
    """Settings for github actions module."""

    hosts: collections.abc.Sequence[str] = ()


@dataclasses.dataclass
class DjangoSettings:
    """Settings for django module."""

    runserver_command: str = "runserver_plus"
    runserver_host: str = "0.0.0.0"  # noqa: S104
    runserver_port: str = "8000"
    runserver_params: str = ""
    runserver_docker_params: str = "--rm --service-ports"
    migrate_command: str = "migrate"
    makemessages_params: str = "--all --ignore venv"
    compilemessages_params: str = ""
    verbose_email_name: str = "Email address"
    default_superuser_email: str = "root@localhost"
    verbose_username_name: str = "Username"
    default_superuser_username: str = "root"
    verbose_password_name: str = "Password"
    default_superuser_password: str = "root"
    shell_command: str = "shell_plus --ipython"
    path_to_remote_config_file: str = "/workspace/app/config/settings/.env"
    manage_file_path: str = "./manage.py"
    settings_path: str = "config.settings.local"
    app_boilerplate_link: str | None = None
    app_template_directory: str = "."
    apps_path: str = "apps"
    remote_db_config_mapping: dict[str, str] = dataclasses.field(
        default_factory=lambda: {
            "dbname": "RDS_DB_NAME",
            "host": "RDS_DB_HOST",
            "port": "RDS_DB_PORT",
            "username": "RDS_DB_USER",
            "password": "RDS_DB_PASSWORD",
        },
    )


@dataclasses.dataclass
class CelerySettings:
    """Settings for celery module."""

    app: str = "config.celery.app"
    scheduler: str = "django"
    service_name: str = "celery"
    loglevel: str = "info"
    extra_params: tuple[str] = ("--beat",)
    local_cmd: str = (
        "celery --app {app} "
        "worker --scheduler={scheduler} --loglevel={loglevel} {extra_params}"
    )


@dataclasses.dataclass
class DBSettings:
    """Settings for db module."""

    password_pattern: str = "Password.*"
    load_dump_command: str = (
        "psql "
        "{additional_params} "
        "--dbname={dbname} "
        "--host={host} "
        "--port={port} "
        "--username={username} "
        "--file={file}"
    )
    dump_filename: str = "local_db_dump.sql"
    load_additional_params: str = "--quiet"
    dump_command: str = (
        "pg_dump "
        "{additional_params} "
        "--dbname={dbname} "
        "--host={host} "
        "--port={port} "
        "--username={username} "
        "--file={file}"
    )
    dump_additional_params: str = "--no-owner"


@dataclasses.dataclass(frozen=True)
class Config:
    """Settings for project invocations."""

    project_name: str = ""

    system: SystemSettings = dataclasses.field(
        default_factory=SystemSettings,
    )
    git: GitSettings = dataclasses.field(
        default_factory=GitSettings,
    )
    pre_commit: PreCommitSettings = dataclasses.field(
        default_factory=PreCommitSettings,
    )
    docker: DockerSettings = dataclasses.field(
        default_factory=DockerSettings,
    )
    python: PythonSettings = dataclasses.field(
        default_factory=PythonSettings,
    )
    github_actions: GitHubActionsSettings = dataclasses.field(
        default_factory=GitHubActionsSettings,
    )
    django: DjangoSettings = dataclasses.field(
        default_factory=DjangoSettings,
    )
    celery: CelerySettings = dataclasses.field(
        default_factory=CelerySettings,
    )
    db: DBSettings = dataclasses.field(
        default_factory=DBSettings,
    )

    def __post_init__(self) -> None:
        """Set default values for settings that are dependant on others."""
        if not self.docker.build_image_tag:
            self.docker.build_image_tag = self.project_name

        if not self.github_actions.hosts:
            self.github_actions.hosts = self.docker.main_containers

    @classmethod
    def from_context(cls, context: invoke.Context) -> "Config":
        """Get config from invoke context."""
        return context.config.get(
            "project_config",
            cls(),
        )
