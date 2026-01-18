import invoke

from . import django, docker, pre_commit, printing, python, system


@invoke.task
def build(
    context: invoke.Context,
) -> None:
    """Build python environ."""
    if python.get_python_env() == python.PythonEnv.LOCAL:
        context.run("uv sync --all-groups")
    else:
        docker.buildpack(context)


@invoke.task
def init(
    context: invoke.Context,
    clean: bool = False,
) -> None:
    """Prepare env for working with project."""
    printing.print_success("Setting up project")
    git_setup(context)
    printing.print_success("Initial assembly of all dependencies")
    if clean:
        docker.clear(context)
    system.copy_local_settings(context)
    system.copy_vscode_settings(context)
    build(context)
    django.migrate(context)
    django.set_default_site(context)
    django.createsuperuser(context)
    printing.print_success("Project setup is completed")


@invoke.task
def git_setup(context: invoke.Context) -> None:
    """Set up git for working."""
    printing.print_success("Setting up git and pre-commit")
    pre_commit.install(context)

    _set_git_setting(
        context,
        setting="merge.ff",
        value="false",
    )
    _set_git_setting(
        context,
        setting="pull.ff",
        value="only",
    )


def _set_git_setting(
    context: invoke.Context,
    setting: str,
    value: str,
) -> None:
    """Set git setting in config."""
    context.run(f"git config --local --add {setting} {value}")


@invoke.task
def update(
    context: invoke.Context,
) -> None:
    """Update project dependencies."""
    context.run("uv lock --upgrade")
    pre_commit.update(context)
