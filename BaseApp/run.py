from app import create_app
import sys
import globals

if __name__ == "__main__":
    if len(sys.argv) == 2:
        globals.setIp(sys.argv[1])
        globals.setRestIp(sys.argv[1])
    elif len(sys.argv) == 3:
        globals.setIp(sys.argv[1])
        globals.setRestIp(sys.argv[2])
    else:
        globals.setIp("localhost")
        globals.setRestIp("localhost")
    flask_app = create_app()
    flask_app.run(host=globals.getIp(), port=8000, debug=True)
