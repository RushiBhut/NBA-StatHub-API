from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class GameModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    name_1 = db.Column(db.String, nullable=False)
    field_goal_percentage_1 = db.Column(db.Float, nullable=False)
    three_point_percentage_1 = db.Column(db.Float, nullable=False)
    free_throw_percentage_1 = db.Column(db.Float, nullable=False)
    name_2 = db.Column(db.String, nullable=False)
    field_goal_percentage_2 = db.Column(db.Float, nullable=False)
    three_point_percentage_2 = db.Column(db.Float, nullable=False)
    free_throw_percentage_2 = db.Column(db.Float, nullable=False)

game_post_args = reqparse.RequestParser()
game_post_args.add_argument("date", type=str, help="The date of the game is required.", required=True)
game_post_args.add_argument("name_1", type=str, help="The name of team 1 is required.", required=True)
game_post_args.add_argument("field_goal_percentage_1", type=float, help="The field goal percentage for team 1 is required.", required=True)
game_post_args.add_argument("three_point_percentage_1", type=float, help="The three point percentage for team 1 is required.", required=True)
game_post_args.add_argument("free_throw_percentage_1", type=float, help="The free throw percentage for team 1 is required.", required=True)
game_post_args.add_argument("name_2", type=str, help="The name of team 2 is required.", required=True)
game_post_args.add_argument("field_goal_percentage_2", type=float, help="The field goal percentage for team 2 is required.", required=True)
game_post_args.add_argument("three_point_percentage_2", type=float, help="The three point percentage for team 2 is required.", required=True)
game_post_args.add_argument("free_throw_percentage_2", type=float, help="The free throw percentage for team 2 is required.", required=True)

game_put_args = reqparse.RequestParser()
game_put_args.add_argument("date", type=str)
game_put_args.add_argument("name_1", type=str)
game_put_args.add_argument("field_goal_percentage_1", type=float)
game_put_args.add_argument("three_point_percentage_1", type=float)
game_put_args.add_argument("free_throw_percentage_1", type=float)
game_put_args.add_argument("name_2", type=str)
game_put_args.add_argument("field_goal_percentage_2", type=float)
game_put_args.add_argument("three_point_percentage_2", type=float)
game_put_args.add_argument("free_throw_percentage_2", type=float)

resource_fields = {
    "id": fields.Integer,
    "date": fields.String,
    "name_1": fields.String,
    "field_goal_percentage_1": fields.Float,
    "three_point_percentage_1": fields.Float,
    "free_throw_percentage_1": fields.Float,
    "name_2": fields.String,
    "field_goal_percentage_2": fields.Float,
    "three_point_percentage_2": fields.Float,
    "free_throw_percentage_2": fields.Float
}

team_names = ["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls", "Cleveland Cavaliers",
            "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
            "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", "Milwaukee Bucks",
            "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder", "Orlando Magic",
            "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs",
            "Toronto Raptors", "Utah Jazz", "Washington Wizards"]

def game_found(game_id):
    game = GameModel.query.filter_by(id=game_id).first()

    if game:
        abort(409, message="Game with this ID already exists.")

def game_not_found(game_id):
    game = GameModel.query.filter_by(id=game_id).first()

    if not game:
        abort(404, message="Game with this ID not found.")

class Game(Resource):
    @marshal_with(resource_fields)
    def get(self, game_id):
        game_not_found(game_id)

        return GameModel.query.filter_by(id=game_id).first()

    @marshal_with(resource_fields)
    def post(self, game_id):
        game_found(game_id)

        args = game_post_args.parse_args()

        if args['name_1'] not in team_names or args['name_2'] not in team_names :
            abort(403, message="Invalid name for either team 1 or team 2.")

        game = GameModel(
            id = game_id,
            date = args['date'],
            name_1 = args['name_1'],
            field_goal_percentage_1 = args['field_goal_percentage_1'],
            three_point_percentage_1 = args['three_point_percentage_1'],
            free_throw_percentage_1 = args['free_throw_percentage_1'],
            name_2 = args['name_2'],
            field_goal_percentage_2 = args['field_goal_percentage_2'],
            three_point_percentage_2 = args['three_point_percentage_2'],
            free_throw_percentage_2 = args['free_throw_percentage_2']
        )

        db.session.add(game)
        db.session.commit()

        return game, 201
    
    @marshal_with(resource_fields)
    def put(self, game_id):
        game_not_found(game_id)

        args = game_put_args.parse_args()

        if args['name_1'] and args['name_1'] not in team_names or args['name_2'] and args['name_2'] not in team_names:
            abort(403, message="Invalid name for either team 1 or team 2.")

        game = GameModel.query.filter_by(id=game_id).first()

        for arg in args:
            if args[str(arg)]:
                setattr(game, str(arg), args[str(arg)])

        db.session.commit()

        return game, 204

    def delete(self, game_id):
        game_not_found(game_id)

        db.session.delete(GameModel.query.filter_by(id=game_id).first())
        db.session.commit()

        return '', 204

api.add_resource(Game, "/game/<int:game_id>")

if __name__ == "__main__":
    app.run(debug=True)
