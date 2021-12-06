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

app = Flask(__name__)
api = Api(app)

api.add_resource(Player, '/player') 

if __name__ == '__main__':
  app.run(host='0.0.0.0')

#Se crea la clase Match
class Match(Resource):
  #Se crea el metodo GET
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('matchId', required=True)
    args = parser.parse_args()

    match_id = args['matchId']
    try:
      match = self.get_match(match_id)
      return match, 200
    except Exception as ex:
      return {'error': str(ex), 'match_id': match_id}

  #Se crea el metodo Post
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('team1', required=True)
    parser.add_argument('team2', required=True)
    parser.add_argument('matchScore', required=True)

    args = parser.parse_args()

    team_1 = args['team1']
    team_2 = args['team2']
    match_score = args['score']

    try:
      match_id = self.create_match(team_1, team_2, match_score)

      match = dict();
      match['match_id'] = match_id
      match['team_1'] = team_1
      match['team_2'] = team_2
      match['match_score'] = match_score

      return match, 200
    except Exception as ex:
      return {'error': str(ex)}, 400
    pass

  def get_match(self, match_id):
    try:
      cursor = conn_mysql.cursor()
      cursor.execute("SELECT * FROM match WHERE match_id = (%s)", (match_id))
      row = cursor.fetchone()
      if row == None:
        raise ValueError('Match does not exists')
      else:
        match_id = row[1]
        team_1 = row[2]
        team_2 = row[3]
        match_score = row[4]

      match = dict();
      match['match_id'] = match_id
      match['team_1'] = team_1
      match['team_2'] = team_2
      match['match_score'] = match_score
    except Exception as ex:
      raise ex
    return (match)

  def create_match(self, team_1, team_2, match_score):
    try:
      cursor = conn_mysql.cursor()
      cursor.execute("INSERT INTO match (team_1, team_2, match_score) VALUES (%s, %s)", (team_1, team_2, match_score))
      conn_mysql.commit()
      match_id = cursor.lastrowid
      return (match_id)
    except Exception as ex:
      raise ex
      



