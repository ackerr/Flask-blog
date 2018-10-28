# 暂时放着错误页面，重构后移位置
from flask import render_template

from src import app


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server(error):
    return render_template('errors/500.html'), 500
