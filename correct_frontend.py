from app import app
import app.config as config

if __name__ == '__main__':
    if config.START_PORT == 0:
        app.run()
    else:
        print("port = " + str(config.START_PORT))
        app.run(port=config.START_PORT)
