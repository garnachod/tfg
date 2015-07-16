import os
import sys
lib_path = os.path.abspath('./sources')
sys.path.append(lib_path)
from sources import app

app.secret_key = os.urandom(24)
app.run(debug=True)
