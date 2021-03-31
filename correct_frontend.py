from app import app
import configparser
import os

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
path_config = os.path.join(dir_path, ".config")
config.read(path_config)
port = int(config['STARTVALUE']['port'])


if __name__ == '__main__':
    if port == 0:
        app.run()
    else:
        print("port = " + str(port))
        app.run(port=port)
