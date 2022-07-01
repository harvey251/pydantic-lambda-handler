import nox


@nox.session(python=["3.9", "3.10"])
def run_tests(session: nox.Session) -> None:
    session.install("pytest")
    session.run("pytest")
