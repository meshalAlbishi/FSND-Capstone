import os
from datetime import datetime
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')

        return response

    # fetch all actors form the database
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def fetch_actors(jwt):
        all_actors = Actor.query.all()

        if len(all_actors) == 0:
            abort(404)

        actors = []
        for actor in all_actors:
            actors.append({
                'id': actor.id,
                'name': actor.name,
                'age': actor.age,
                'gender': actor.gender
            })

        return jsonify({
            'success': True,
            'actors': actors
        })

    # fetch all movies form the database
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def fetch_movies(jwt):
        all_movies = Movie.query.all()

        if len(all_movies) == 0:
            abort(404)

        movies = []
        for movie in all_movies:
            movies.append({
                'id': movie.id,
                'name': movie.name,
                'age': movie.age,
                'gender': movie.gender
            })

        return jsonify({
            'success': True,
            'movies': movies
        })

    # delete movie from database
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.get(movie_id)

        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'movie_id': movie_id
        })

    # delete actor from database
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(jwt, actor_id):
        actor = Actor.query.get(actor_id)

        if actor is None:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'actor_id': actor_id
        })

    # create actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor(jwt):
        data = request.get_json()

        if data.name is None or data.age is None or data.gender is None:
            abort(400)

        actor = Actor(name=data.name, age=data.age, gender=data.gender)
        actor.insert()

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    # create movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def create_movie(jwt):
        data = request.get_json()

        if data.title is None or data.release is None:
            abort(400)

        movie = Movie(title=data.title, release=data.release)
        movie.insert()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    # update movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(jwt, movie_id):
        data = request.get_json()

        if data.title is None or data.release is None:
            abort(400)

        movie = Movie.query.get(movie_id)
        movie.title = data.title
        movie.release = data.release

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    # update actor
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(jwt, actor_id):
        data = request.get_json()

        if data.name is None or data.age is None or data.gender is None:
            abort(400)

        actor = Actor.query.get(actor_id)
        actor.name = data.name
        actor.gender = data.gender

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    # error handlers
    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable request'
        }), 422)

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400)

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404)

    @app.errorhandler(401)
    def unauthorized(error):
        return (jsonify({
            'success': False,
            'error': 401,
            'message': 'unauthorized access'
        }), 401)

    @app.errorhandler(AuthError)
    def auth_error(error):
        return (jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
