#Valmiiseen pohjaan kommentoidut funktiot toteuttanut:
#Ilari Miettunen


from dotenv import dotenv_values
import requests
import webbrowser
import websocket
import json
from lib.math import normalize_heading
import time
import math

FRONTEND_BASE = "noflight.monad.fi"
BACKEND_BASE = "noflight.monad.fi/backend"

game_id = None


def on_message(ws: websocket.WebSocketApp, message):
    [action, payload] = json.loads(message)

    if action != "game-instance":
        print([action, payload])
        return

    # New game tick arrived!
    game_state = json.loads(payload["gameState"])
    commands = generate_commands(game_state)

    time.sleep(0.1)
    ws.send(json.dumps(["run-command", {"gameId": game_id, "payload": commands}]))


def on_error(ws: websocket.WebSocketApp, error):
    print(error)


def on_open(ws: websocket.WebSocketApp):
    print("OPENED")
    ws.send(json.dumps(["sub-game", {"id": game_id}]))


def on_close(ws, close_status_code, close_msg):
    print("CLOSED")


#Counts the angle difference between two direcitons
def angleDiff(ac_dir, goal_dir):
    """Calculates absolute value of angle difference between two directions

    Args:
        ac_dir (integer): Direction aircraft is currently heading
        goal_dir (integer): Wanted direction

    Returns:
        integer: absolute value of angle difference
    """
    if abs(ac_dir - goal_dir) > 180:
        return 360 - abs(ac_dir - goal_dir)
    else:
        return abs(ac_dir - goal_dir)

def approachPoint(ac_dir, ap_dir, ap_x, ap_y, ext = False):
    """Calculates coordinates for point in approach line with default distance of 10 from airport or with extended approach line.
     Approach point is calculated so that it gives aircraft enough distance to turn to airport's approach direction

    Args:
        ac_dir (int): aircraft's current heading
        ap_dir (int): airport's approach direction
        ap_x (int): airport's x-coordinate
        ap_y (int): airport's y-coordinate
        ext (bool): True if extended radius, false if calulated with radius of 10

    Returns:
        float, float : approach point's coordinates
    """
    #Difference between aircraft and airport directions
    ang_diff = angleDiff(ac_dir, ap_dir)

    #Minimum radius that is enough to make the turn to airport rounded up to five because ticksAhead is 5 per tick
    #Default is 10
    if ext:
        radius = math.ceil(((5*ang_diff)/20)/5)*5
    else:
        radius = 10

    #Direction from where airport needs to be approached
    from_dir = normalize_heading(ap_dir-180)

    #Coordinates for approach point
    if from_dir == 180 or from_dir == 0:
        app_x = ap_x + radius*math.cos(math.radians(from_dir))
        app_y = ap_y
    elif from_dir == 90 or from_dir == 270:
        app_x = ap_x
        app_y = ap_y + radius*math.sin(math.radians(from_dir))
    else:
        app_x = ap_x + radius*math.cos(math.radians(from_dir))
        app_y = ap_y + radius*math.sin(math.radians(from_dir))

    return app_x, app_y

def distanceBetween(ac_x, ac_y, x2, y2):
    """Calculates distance between two points

    Args:
        ac_x (float): aircraft's current x-coordinate
        ac_y (float): aircraft's current y-coordinate
        x2 (float): x-coordinate of other point
        y2 (float): y-coordinate of other point

    Returns:
        float: distance between two coordinates
    """
    delta_y = ac_y-y2
    delta_x = ac_x-x2

    return math.sqrt(math.pow(delta_y,2) + math.pow(delta_x,2))

def directionTo(ac_x, ac_y, goal_x, goal_y):
    """Calculates direction from aircraft's coordinates to other coordinates

    Args:
        ac_x (float): aircraft's current x-coordinate
        ac_y (float): aircraft's current y-coordinate
        goal_x (float): x-coordinate of other point
        goal_y (float): y-coordinate of other point

    Returns:
        int: direction from aircraft to other point
    """
    if ac_x == goal_x:
        if ac_y < goal_y:
            return 90
        else:
            return 270
    if ac_y == goal_y:
        if ac_x < goal_x:
            return 0
        else:
            return 180
    return normalize_heading(math.degrees(math.atan2(goal_y-ac_y, goal_x-ac_x)))

def pointAhead(ac_x, ac_y, goal_x, goal_y, ac_dir):
    """Tells if point is in +-90 degree sector in front of aircraft

    Args:
        ac_x (float): aircraft's current x-coordinate
        ac_y (float): aircraft's current y-coordinate
        goal_x (float): x-coordinate of other point
        goal_y (float): y-coordinate of other point
        ac_dir (int): aircraft's current heading

    Returns:
        bool: True if given point is in front of aircraft
    """
    dir_to = directionTo(ac_x, ac_y, goal_x, goal_y)
    return angleDiff(ac_dir, dir_to) <= 90

def turn(ac_dir,goal_dir):
    """Tells which way aircraft must turn

    Args:
        ac_dir (int): aircraft's current heading
        goal_dir (int): wanted direction in which to turn

    Returns:
        int: new direction in which aircraft will turn
    """
    #If angle difference between aircraft direction and goal direction is 20degrees or less, goal direction will 
    # be set as aircraft's new direction unless it's only 2degreers or less apart from current direction
    if angleDiff(ac_dir, goal_dir) <= 20:
        new_dir = normalize_heading(goal_dir)
        if abs(new_dir-ac_dir) <= 2:
            new_dir = ac_dir

    #If angle difference is more, we'll decide on what direction it is better to turn        
    else:
        if normalize_heading(ac_dir-goal_dir)<= 180:
            #Right turn
            new_dir = normalize_heading(ac_dir-20)
        else:
            #Left turn
            new_dir = normalize_heading(ac_dir+20)
    return new_dir

#Calculates aircrafts next coordinates on this heading
def getNextPoint(aircraft, direction):
    """Calculates the coordinates for point in which aircraft will move during next ticks 
    (ticksAhead = amount of ticks) if it would move to given direction and current speed

    Args:
        aircraft (dict): Dict containing information concerning aircraft
        direction (int): Direction in which the movement will be calculated

    Returns:
        float,float: Coordinates for aircrafts next position
    """
    ticksAhead = 5
    nextX = aircraft['position']['x'] + ticksAhead*int(aircraft['speed']) * math.cos(math.radians(direction))
    nextY = aircraft['position']['y'] + ticksAhead*int(aircraft['speed']) * math.sin(math.radians(direction))

    return nextX, nextY


def collision(aircrafts, ac1, direction):
    """Calculates if aircrafts will collide if flown in certain direction. Teturns True if aircraft's will end up 
    inside others collisionRadius +5 (+5 for time to react and turn away)

    Args:
        aircrafts (list): List of aircraft dicts
        ac1 (dict): Aircraft which possibility to collide to others is inspected
        direction (int): Direction that is inspected for intersecting traffic

    Returns:
        bool: True if situation leads to collision
    """
    for ac2 in aircrafts:
        if ac2['id'] != ac1['id']:
            ac1NextX, ac1NextY = getNextPoint(ac1, direction)
            ac2NextX, ac2NextY = getNextPoint(ac2, ac2['direction'])
            if distanceBetween(ac1NextX, ac1NextY, ac2NextX, ac2NextY) <= ac1['collisionRadius']+5:
                return True           

    return False


# Change this to your own implementation
def generate_commands(game_state):
    """Function that generates commands to guide aircrafts to airports in right direction without colliding

    Args:
        game_state (dict): Contains all the needed information about gamestatus, airports and aircrafts

    Returns:
        list: List of commands for aircrafts
    """
 
    commands = []

    for aircraft in game_state["aircrafts"]:
        airport = {}
        #Search right destination for aircraft
        for ap in game_state["airports"]:
            if ap["name"] == aircraft["destination"]:
                airport = ap

        #Aircraft direction and coordinates
        ac_dir = aircraft["direction"]
        ac_x = round(aircraft["position"]["x"],2)
        ac_y = round(aircraft["position"]["y"],2)

        #Airport approach direction and coordinates
        ap_dir = airport["direction"]
        ap_x = airport["position"]["x"]
        ap_y = airport["position"]["y"]

        #Count APPROACH POINT on approach line with radius of 10 from airport (needs to be reached with +-40degree angle)
        approach_x, approach_y = approachPoint(ac_dir, ap_dir, ap_x, ap_y)

        #Rounded direction from aircraft's coordinates to approach point's coordinates
        #and rounded direction from aircraft's coordinates to airports point's coordinates
        dir_to_app = round(directionTo(ac_x, ac_y, approach_x, approach_y))
        dir_to_airport = round(directionTo(ac_x, ac_y, ap_x, ap_y))
  
        #If more than one aircraft in game and collision on its way, turn right 20degrees
        if len(game_state["aircrafts"]) > 1 and collision(game_state["aircrafts"], aircraft, dir_to_airport):  
            new_dir = normalize_heading(ac_dir-20)

        #Seuraavaa kahta elif lausetta yhdistämällä viimeisestä tehtävästä saa erilaisia tuloksia, koneet lentää miten sattuu mutta menee maaliin.
        #Molemmilla yhdessä saa 138pts
        #Pelkällä tällä 122pts
        #If aircraft is turnt left 10degrees and collision would happen -> turn right 10degrees
        elif collision(game_state["aircrafts"], aircraft, ac_dir+10):
            new_dir = normalize_heading(ac_dir-10)

        #Pelkällä tällä  181pts
        #If aircraft is turnt right 10degrees and collision would happen -> turn left 10degrees
        #elif collision(game_state["aircrafts"], aircraft, ac_dir-10):
            #new_dir = normalize_heading(ac_dir+10)
        
        #If no collisions in sight, aircraft tries to find it's way to airport
        #If suitable conditions(angle and distance to approach point and/or airport) to get to airport, aircraft goes to airport
        elif (angleDiff(dir_to_app, ap_dir) <= 40 or angleDiff(ac_dir,ap_dir) <= 40) and pointAhead(ac_x, ac_y, ap_x, ap_y, ac_dir):
            if ac_dir != dir_to_app and distanceBetween(ac_x, ac_y, ap_x, ap_y) > 15:
                new_dir = turn(ac_dir,dir_to_app)
            elif distanceBetween(ac_x, ac_y, ap_x, ap_y) <= 15:
                new_dir = turn(ac_dir, ap_dir)
            else:
                new_dir = ac_dir

        #If conditions doesn't allow going for landing, extended approach point will be found
        #and aircraft goes towards it
        else:
            ext_app_x, ext_app_y =  approachPoint(ac_dir, ap_dir, ap_x, ap_y, True)
            dir_to_ext_app = round(directionTo(ac_x, ac_y, ext_app_x, ext_app_y))

            new_dir = turn(ac_dir, dir_to_ext_app)

        #If calculated new direction is different from current direction, new direction will be assigned
        if new_dir != ac_dir:
            commands.append(f"HEAD {aircraft['id']} {new_dir}")
    return commands


def main():
    config = dotenv_values()
    res = requests.post(
        f"https://{BACKEND_BASE}/api/levels/{config['LEVEL_ID']}",
        headers={
            "Authorization": config["TOKEN"]
        })

    if not res.ok:
        print(f"Couldn't create game: {res.status_code} - {res.text}")
        return

    game_instance = res.json()

    global game_id
    game_id = game_instance["entityId"]

    url = f"https://{FRONTEND_BASE}/?id={game_id}"
    print(f"Game at {url}")
    webbrowser.open(url, new=2)
    time.sleep(2)

    ws = websocket.WebSocketApp(
        f"wss://{BACKEND_BASE}/{config['TOKEN']}/", on_message=on_message, on_open=on_open, on_close=on_close, on_error=on_error)
    ws.run_forever()


if __name__ == "__main__":
    main()
