import os


class NoEnvironmentVar(Exception):
    def __init__(self, variable: str):
        super().__init__(f'Environment variable {variable} does not exist')


def get_env_variable(variable: str) -> str:
    """Retrieve the value of the specified environment variable.

    Args:
        variable (str): The name of the environment variable.

    Returns:
        str: The value of the environment variable.

    Raises:
        NoEnvironmentVar: If the specified environment variable does not exist.

    """
    # Check if the 'variable' environment variable exists
    if variable not in os.environ:
        raise NoEnvironmentVar(variable)

    return os.environ.get(variable)
