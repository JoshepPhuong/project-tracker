import pathlib
import re

from django.conf import settings

import mistune

from config.settings.common.paths import BASE_DIR

H_LEVEL = 2
VERSION_FORMAT = r"\d{1,2}\.\d{1,2}\.\d{1,3}$"


class ChangelogRenderer(mistune.HTMLRenderer):
    """Renderer for changelog page.

    It expects style like `## X.Y.Z` for versions in changelog.

    """

    def heading(self, text: str, level: int, **attrs) -> str:
        """Override to add anchors for changelog versions headers."""
        if re.fullmatch(VERSION_FORMAT, text) and level == H_LEVEL:
            tag = f"h{level}"
            anchor = f"{text.replace('.', '').lower()}"
            return f"<{tag} id={anchor}><a href=#{anchor}>{text}</a></{tag}>"

        return super().heading(text, level, **attrs)


def get_changelog_html(changelog_name: str) -> str:
    """Convert changelog text to html."""
    changelog_path = pathlib.Path(f"{settings.BASE_DIR}/docs/{changelog_name}")
    if not changelog_path.exists():
        return ""  # pragma: no cover

    with pathlib.Path(changelog_path, encoding="UTF-8").open() as file:
        changelog = file.read()

    markdown = mistune.create_markdown(renderer=ChangelogRenderer())
    return markdown(changelog)


def get_latest_version(changelog_filepath: str) -> str:
    """Get latest version from changelog file.

    Args:
        changelog_filepath (str):Path to changelog file

    Raises:
        ValueError: if we couldn't find any versions in changelog file

    Notes:
        - We use absolute path to avoid issues with path
        (For example in PyCharm)
        - We don't use `from django.conf import settings` because this function
        is used in settings to setup version for sentry and open-api

    """
    atx = "#" * H_LEVEL
    version_regex = rf"(?<=^{atx} ){VERSION_FORMAT}$"
    re_rule = re.compile(version_regex)

    with pathlib.Path(f"{BASE_DIR}/docs/{changelog_filepath}").open() as file:
        for line in file:
            search = re_rule.search(line)
            if search:
                return search.group()

    raise ValueError(  # pragma: no cover
        "Incorrect changelog file, couldn't find version number for "
        f"{changelog_filepath}",
    )


def get_choice_by_label(choices, label: str):
    """Return the choice member using its label."""
    for choice in choices:
        if choice.label == label:
            return choice
    raise ValueError(f"{label} is not a valid choice")
