import pathlib
from appdirs import user_config_dir

config = pathlib.Path(user_config_dir('FTPd'), "settings.py")
if config.exists():
    exec(config.open().read())
else:
    raise RuntimeError("Missing %s file." % config)
