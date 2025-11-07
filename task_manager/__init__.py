from flask import Flask

app = Flask(__name__)

from task_manager import routes
