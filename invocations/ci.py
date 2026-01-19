import invoke

from . import project, printing, docker, system, github_actions


@invoke.task
def prepare(context: invoke.Context) -> None:
    """Prepare ci environment for check."""
    printing.print_success("Preparing CI")
    docker.up(context)
    github_actions.set_up_hosts(context)
    system.copy_local_settings(context)
    project.build(context)
    # Needed to resolve minio urls
    context.run("sudo apt-get install -y libnss-myhostname")
