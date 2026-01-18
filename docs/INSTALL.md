# PhuongPV

- Project URL: <https://phuongpv.com>
- API Docs: <https://dev.phuongpv.com/api/v1/open-api/redoc/>
- Swagger UI: <https://dev.phuongpv.com/api/v1/open-api/ui/>

## Installing project for developing on local PC

You have to have the following tools installed prior initializing the project:

- [docker](https://docs.docker.com/engine/installation/)
- [docker-compose](https://docs.docker.com/compose/install/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Task runner

For easier running of everyday tasks, like:

- run dev server
- run all tests
- run linters
- run celery workers
- ...

We use [invoke](https://pypi.org/project/invoke/).

It provides shortcuts for most of the tasks, so it's like collection of bash scrips
or makefile or `npm scripts`.

To enable autocompletion of invoke commands add this line to your `~/.zshrc`

```bash
source <(inv --print-completion-script zsh)
```

### Python interpreter

Also `invoke` abstract "python interpreter", so you can use both `virtual env`
and `dockerized` python interpreter for working with project
(see `tasks.py` file).

- `virtualenv` is the default approach that requires python interpreter,
virtualenv, etc.
- `dockerized` is simpler for quick starting project and for experienced
developers

Suggested approach is using `virtualenv`

### Services

- Project may use external services like Database (postgres), message broker,
cache (redis). For easier set up they are defined in `compose.yml` file,
and they are automatically prepared / started when using `invoke`.

### Prepare python env

Create separate python virtual environment if you are going to run it in
local:

```bash
uv venv --python 3.13 --prompt project-tracker --seed
source .venv/bin/activate && uv sync --all-groups
```

Set up aliases for docker hosts in `/etc/hosts`:

```text
127.0.0.1 postgres
127.0.0.1 redis
127.0.0.1 mailpit
127.0.0.1 s3.minio.localhost
```

Start project initialization that will set up docker containers,
python/system env:

```bash
inv project.init
```

Run the project and go to `localhost:8000` page in browser to check whether
it was started:

```bash
inv django.run
```

That's it. After these steps, the project will be successfully set up.

Once you run `project.init` initially you can start web server with
`inv django.run` command without executing `project.init` call.
