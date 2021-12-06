# Player APP

This is an app to create and get players, developed in Python and supported in Docker.

## Installation

Install docker-compose to execute all the necessary containers. 
Install curl to make HTTP requests

## Usage
### Start
```bash
docker-compose up --build [-d] 
```
- -d option is to run containers in deattached mode
#
### Create Players
```bash
curl -XPOST localhost:8083/player -d '{"playerName": "johndoe", "gold":"1000"}' -H "Content-Type: application/json"
```
Expected Response:
```bash
{"player_id": "1", "player_name": "johndoe", "gold": "1000"}
```

#
### Get Player Data
```bash
curl -XGET localhost:8083/player -d '{"playerId":3}' -H "Content-Type: application/json"  
```
Expected Response:
```bash
{"player_id": "1", "player_name": "johndoe", "gold": "1000"}
```
#
### Create Match
```bash
curl -XPOST localhost:8083/match -d '{"team_1": "1", "team_2":"2", "match_score": "25-20"}' -H "Content-Type: application/json"
```
Expected Response:
```bash
{"match_id": "1", team_1": "3", "team_2": "5", "match_score": "25-20"}
```

#
### Get Match
```bash
curl -XGET localhost:8083/match -d '{"match_id":1}' -H "Content-Type: application/json"  
```
Expected Response:
```bash
{"match_id": "1", team_1": "3", "team_2": "5", "match_score": "25-20"}
```

#
### Create Categories
```bash
curl -XPOST localhost:8083/player -d '{"categoryName": "bronze", "categoryDescription":"Lowest Category Type"}' -H "Content-Type: application/json"
```
Expected Response:
```bash
{"category_id": "1", "category_name": "bronze", "category_description": "Lowest Category Type"}
```

#
### Get Category
```bash
curl -XGET localhost:8083/player -d '{"categoryId":1}' -H "Content-Type: application/json"  
```
Expected Response:
```bash
{"player_id": "1", "category_name": "bronze", "category_description": "Lowest Category Type"}
```
#
### Stop
If you started the containers with -d option
```bash
docker-compose stop
```
