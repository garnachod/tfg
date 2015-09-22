import os
import sys
lib_path = os.path.abspath('./sources')
sys.path.append(lib_path)
from sources import app

if __name__ == '__main__':
	app.secret_key = os.urandom(24)
	app.run(host='0.0.0.0', debug=False)

