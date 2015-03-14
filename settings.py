from appdirs import user_config_dir

config = os.path.join(user_config_dir('FTPd'), "settings.py")
if os.path.exists(config):
    execfile(config)
else:
    raise RuntimeError("Missing %s file." % config)
