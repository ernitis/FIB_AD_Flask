from app import create_app
import sys
import globals

ip = globals.setIp(sys.argv[1])

flask_app = create_app()

if __name__ == "__main__":
    flask_app.run(host=ip, port=8000, debug=True)
