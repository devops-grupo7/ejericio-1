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
### Stop
If you started the containers with -d option
```bash
docker-compose stop
```
