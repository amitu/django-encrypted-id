def task_aliases():
    aliases = """
        tests0: tox -e py27-django15
        tests: tox
        release: python setup.py bdist_wheel sdist --formats=bztar,zip upload
        cleanup: rm -rf .tox
        readme: restview README.rst
    """
    for alias in aliases.split("\n"):
        alias = alias.strip()

        if not alias:
            continue

        name, command = alias.split(":", 1)

        yield {
            "basename": name,
            "actions": [command]
        }
