from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse
import mysql.connector
import redis
import os

try:
  conn_mysql = mysql.connector.connect(
    host=os.environ.get('MYSQL_HOST'),
    user=os.environ.get('MYSQL_USER'),
    password=os.environ.get('MYSQL_PASSWORD'),
    port=os.environ.get('MYSQL_PORT'),
    database=os.environ.get('MYSQL_DB')
  )
  print(conn_mysql)
  print('Connected to MySQL')
except Exception as ex:
  print('Error: ', ex)
  exit('Failed to connect to MySQL, terminating.')

try:
  conn_redis = redis.Redis(
      host=os.environ.get('REDIS_HOST'),
      port=os.environ.get('REDIS_PORT'),
      password=os.environ.get('REDIS_PASSWORD'),
      charset="utf-8", 
      decode_responses=True
  )
  print(conn_redis)
  conn_redis.ping()
  print('Connected to Redis')
except Exception as ex:
  print('Error: ', ex)
  exit('Failed to connect to Redis, terminating.')

class Player(Resource):
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('playerId', required=True)
    args = parser.parse_args()

    player_id = args['playerId']
    try:
      player_stats = self.get_player(player_id)
      print(player_stats)
      return player_stats, 200
    except Exception as ex:
      print(ex)
      return {'error': str(ex), 'player_id': player_id}, 400


  def post(self):
    parser = reqparse.RequestParser()

    parser.add_argument('playerName', required=True)
    parser.add_argument('gold', required=True)

    args = parser.parse_args()

    player_name = args['playerName']
    gold = int(args['gold'])

    try:
      self.validate_player(player_name, gold)
      player_id=self.create_player(player_name, gold)

      player = dict();
      player['player_id']=player_id
      player['player_name']=player_name
      player['gold']=gold

      return player, 200

    except Exception as ex:
      print(ex)
      return {'error': str(ex)}, 400
  pass

  def validate_player(self, player_name, gold):
    if len(player_name) > 25:
      raise ValueError('PlayerName lenght exceeded')
    if gold > 1000000000:
      raise ValueError('MaxGold exceeded')

  def create_player(self, player_name, gold):
    try:
      cursor = conn_mysql.cursor()
      cursor.execute("INSERT INTO players (player_name) VALUES (%s)", (player_name,))
      conn_mysql.commit()
      print("Player created in Database with player_id:", cursor.lastrowid)
      player_id =  cursor.lastrowid
      conn_redis.set(player_id, gold)
      return(player_id)
    except mysql.connector.Error as err:
      if err.errno == 1062:
        raise ValueError("Username is already in use " + player_name)
    except Exception as ex:
      raise ex

  def get_player(self, player_id):
    try:
      cursor = conn_mysql.cursor()
      cursor.execute("SELECT player_id, player_name FROM players WHERE player_id = (%s)", (player_id,))
      print(cursor.rowcount)
      row = cursor.fetchone()
      if row == None:
        raise ValueError('User does not exists')
      else:
        player_name = row[1]

      gold = conn_redis.get(player_id)

      player = dict();
      player['player_id']=player_id
      player['player_name']=player_name
      player['gold']=gold
    except Exception as ex:
      raise ex
    return(player)

class Category(Resource):
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('categoryId', required=True)
    args = parser.parse_args()

    category_id = args['categoryId']
    try:
      category = self.get_category(category_id)
      print(category)
      return category, 200
    except Exception as ex:
      print(ex)
      return {'error': str(ex), 'category_id': category_id}, 400

  def post(self):
    parser = reqparse.RequestParser()

    parser.add_argument('categoryName', required=True)
    parser.add_argument('categoryDescription', required=True)

    args = parser.parse_args()

    name = args['categoryName']
    description = args['categoryDescription']

    try:
      category_id=self.create_category(name, description)

      category = dict();
      category['category_id']=category_id
      category['category_name']=name
      category['category_description']=description

      return category, 200

    except Exception as ex:
      print(ex)
      return {'error': str(ex)}, 400
  pass

  def get_category(self, category_id):
    try:
      cursor = conn_mysql.cursor()
      cursor.execute("SELECT category_id, name, description FROM categories WHERE category_id = (%s)", (category_id,))
      print(cursor.rowcount)
      row = cursor.fetchone()
      if row == None:
        raise ValueError('Category does not exists')
      else:
        category_name = row[1]
        category_description = row[2]


      category = dict();
      category['category_id']=category_id
      category['category_name']=category_name
      category['category_description']=category_description
    except Exception as ex:
      raise ex
    return(category)

  def create_category(self, name, description):
    try:
      cursor = conn_mysql.cursor()
      cursor.execute("INSERT INTO categories (name, description) VALUES (%s, %s)", (name, description))
      conn_mysql.commit()
      print("Category created in Database with category_id:", cursor.lastrowid)
      category_id =  cursor.lastrowid
      return(category_id)
    except mysql.connector.Error as err:
      if err.errno == 1062:
        raise ValueError("Name is already in use " + name)
    except Exception as ex:
      raise ex

app = Flask(__name__)
api = Api(app)
api.add_resource(Player, '/player') 
api.add_resource(Category, '/category') 

if __name__ == '__main__':
  app.run(host='0.0.0.0')

