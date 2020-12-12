import utils

def a(input):
    direction = utils.Coord2D(-1,0)
    point = utils.Coord2D(0,0)

    for instruction, value in input:
        if instruction == 'N':
            point.y += value
        elif instruction == 'S':
            point.y -= value
        elif instruction == 'E':
            point.x -= value
        elif instruction == 'W':
            point.x += value
        elif instruction == 'L':
            for i in range(value//90):
                direction.rotate90R()
        elif instruction == 'R':
            for i in range(value//90):
                direction.rotate90L()
        elif instruction == 'F':
            point.x += direction.x*value
            point.y += direction.y*value

    print(abs(point.x+point.y))

def rotate90L(ship, waypoint):
    dx, dy = waypoint.x-ship.x, waypoint.y-ship.y
    sdx = dy
    waypoint.x = ship.x - sdx
    waypoint.y = ship.y + dx

def rotate90R(ship, waypoint):
    dx = ship.x + waypoint.y - ship.y
    waypoint.y = ship.y - (waypoint.x-ship.x)
    waypoint.x = dx

def b(input):
    waypoint = utils.Coord2D(10,1)
    ship = utils.Coord2D(0,0)

    for instruction, value in input:
        if instruction == 'N':
            waypoint.y += value
        elif instruction == 'S':
            waypoint.y -= value
        elif instruction == 'E':
            waypoint.x += value
        elif instruction == 'W':
            waypoint.x -= value
        elif instruction == 'L':
            for i in range(value//90):
                rotate90L(ship, waypoint)
        elif instruction == 'R':
            for i in range(value//90):
                rotate90R(ship, waypoint)
        elif instruction == 'F':
            dx, dy = waypoint.x-ship.x, waypoint.y-ship.y
            ship.x += dx*value
            ship.y += dy*value
            waypoint.x += dx*value
            waypoint.y += dy*value

    print(abs(ship.x)+abs(ship.y))

input = utils.input_lines(generator=lambda x: (x[0],int(x[1:])), test=False)
a(input)
b(input)
