from flask import Flask, make_response, jsonify
from flask_restful import Api

from data import db_session, news_resources

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api = Api(app, catch_all_404s=True)


def main():
    db_session.global_init("db/blogs.db")
    # для списка объектов
    api.add_resource(news_resources.NewsListResource, '/api/v2/news') # ALL

    # для одного объекта
    api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>') # ONE

    app.run()


if __name__ == '__main__':
    main()
