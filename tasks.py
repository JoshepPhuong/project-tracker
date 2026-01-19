import invoke

import invocations

ns = invoke.Collection(
    invocations.ci,
    invocations.db,
    invocations.django,
    invocations.docker,
    invocations.github_actions,
    invocations.pre_commit,
    invocations.project,
    invocations.python,
    invocations.pytest,
    invocations.system,
)


# Configurations for run command
ns.configure(
    {
        "run": {
            "pty": True,
            "echo": True,
        },
        "project_config": invocations._config.Config(
            project_name="project-tracker",
        ),
    },
)
