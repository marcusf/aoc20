import utils

p1, p2 = [tuple([int(b) for b in a[1:]]) for a in \
    utils.read_input_multi(delim_1='\n\n',delim_2='\n', test=False)]

def one_pass(p1,p2):
    c1, c2 = p1[0], p2[0]
    if c1 > c2:
        p1, p2 = p1[1:]+(c1,c2), p2[1:]
    else:
        p2, p1 = p2[1:]+(c2,c1), p1[1:]
    return p1, p2

def a(p1, p2):
    while p1 and p2:
        p1, p2 = one_pass(p1, p2)
    winner = p1 if p1 else p2
    print(sum([a*b for a,b in zip(winner, range(len(winner),0,-1))]))

def b(p1, p2):
    winner, score, _ = game(p1,p2)
    print(winner, score)
    print(sum([a*b for a,b in zip(score, range(len(score),0,-1))]))

def game(p1, p2,gamen=1):
    print('=== Game {} ==='.format(gamen))
    nextgame = gamen
    round=0
    previous = set()

    while p1 and p2:
        round += 1
        print('')
        print('-- Round {} (Game {}) --'.format(round, gamen))

       
        if (p1,p2) in previous:
            print("*** Round already played in game, 1 wins.")
            return 1, p1, nextgame
        previous.add((p1,p2))

        print('Player 1\'s deck: {}'.format(', '.join([str(p) for p in p1])))
        print('Player 2\'s deck: {}'.format(', '.join([str(p) for p in p2])))

        c1, c2 = p1[0], p2[0]
        winner = 0

        print('Player 1 plays: {}'.format(c1))
        print('Player 2 plays: {}'.format(c2))

        if len(p1)-1 >= c1 and len(p2)-1 >= c2:
            print('Playing a sub-game to determine the winner...\n')
            nextgame+=1
            winner, _, nextgame = game(p1[1:c1+1], p2[1:c2+1], nextgame)
            print('\n...anyway, back to game {}.'.format(nextgame))
        else:
            winner = 1 if c1 > c2 else 2

        if winner == 1:
            p1, p2 = p1[1:]+(c1,c2), p2[1:]
        else:
            p2, p1 = p2[1:]+(c2,c1), p1[1:]

        print('Player {} wins round {} of game {}!'.format(winner, round, gamen))

    print('The winner of game {} is player {}!'.format(gamen, 1 if p1 else 2))
    return 1 if p1 else 2, p1 if p1 else p2, nextgame

a(p1,p2)
b(p1,p2)