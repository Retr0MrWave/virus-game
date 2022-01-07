from aiohttp import web
import VirusGame as vg

routes = web.RouteTableDef()

gamesDict = {}

@routes.post('/create_session')
async def create_session(request):
    data = await request.post()
    # Main parameters
    for param in ('session_id', 'size', 'p1s'):
        if not param in data:
            return web.Response(status=400, reason=(param+" is required"))

    # Reserved names
    if data['session_id'] == 'create_session':
        return web.Response(status=403, reason="This is a reserved name")
    if data['session_id'] == 'join_session':
        return web.Response(status=403, reason="This is a reserved name")
    if '/' in data['session_id']:
        return web.Response(status=403, reason="This is a reserved name")
    
    # size being the right type
    try:
        size = int(data['size'])
    except ValueError:
        return web.Response(status=400, reason="size should be an integer")
    if size <= 1:
        return web.Response(status=400, reason="size should be greater, than 1")
    
    if data['session_id'] in gamesDict:
        return web.Response(status=403, reason="this session already exists")
    
    gamesDict[data['session_id']] = [vg.Game(size, size), data['p1s'], None, 1, 0].copy()
    
    return web.Response(status=200)

@routes.post('/join_session')
async def join_session(request):
    data = await request.post()
    # Main parameters
    for param in ('session_id', 'p2s'):
        if not param in data:
            return web.Response(status=400, reason=(param+" is required"))
    
    if not data['session_id'] in gamesDict:
        return web.Response(status=404, reason="this session does not exist")
    
    gamesDict[data['session_id']][2] = data['p2s']
    
    return web.Response(status=200)

@routes.post('/{session_id}/move')
async def move(request):
    data = await request.post()
    # Main parameters
    for param in ('player', 'secret', 'movex', 'movey'):
        if not param in data:
            return web.Response(status=400, reason=(param+" is required"))
    id = request.match_info['session_id']
    
    if not id in gamesDict:
        return web.Response(status=404, reason="this session does not exist")
    
    for param in ('movex', 'movey', 'player'):
        try:
            temp = int(data[param])
        except ValueError:
            return web.Response(status=400, reason=(param+" should be an integer"))
    p, x, y = map(int, (data['player'], data['movex'], data['movey']))

    if data['secret'] != gamesDict[id][p]:
        return web.Response(status=403, reason="wrong secret")

    if p != gamesDict[id][3]:
        return web.Response(status=403, reason="it is not your turn")
    
    if x < 0 or x >= gamesDict[id][0].width or y < 0 or y >= gamesDict[id][0].height:
        return web.Response(status=400, reason="You messed up the coordinates")

    res = gamesDict[id][0].makeMove(p, [x, y].copy())
    if not res:
        return web.Response(status=400, reason="Move is invalid")
    else:
        gamesDict[id][4] += 1
        if gamesDict[id][4] > 2:
            gamesDict[id][4] = 0
            if gamesDict[id][3] == 1:
                gamesDict[id][3] = 2
            else:
                gamesDict[id][3] = 1
        return web.Response(status=200)

@routes.post('/{session_id}/del')
async def del_session(request):
    data = await request.post()
    # Main parameters
    for param in ('player', 'secret'):
        if not param in data:
            return web.Response(status=400, reason=(param+" is required"))
            
    try:
        p = int(data['player'])
    except ValueError:
        return web.Response(status=400, reason=("player should be an integer"))
    
    if not request.match_info['session_id'] in gamesDict:
        return web.Response(status=404, reason="this session does not exist")
    
    if data['secret'] != gamesDict[request.match_info['session_id']][p]:
        return web.Response(status=403, reason="wrong secret")
    
    gamesDict[request.match_info['session_id']][p] = None

    if gamesDict[request.match_info['session_id']][1] == None and gamesDict[request.match_info['session_id']][2] == None:
        del gamesDict[request.match_info['session_id']]
    
    return web.Response(status=200)

@routes.get('/{session_id}')
async def get_game(request):
    session_id = request.match_info['session_id']
    try:
        game = gamesDict[session_id][0]
        if game.checkGameEnd(gamesDict[session_id][3]):
            return web.Response(text=str(gamesDict[session_id][3] % 2 + 1))
        return web.Response(text=game.getString() + '\n---' + '\n' + str(gamesDict[session_id][3]))
    except KeyError:
        return web.Response(status=404, reason="session not found")

app = web.Application()
app.add_routes(routes)
web.run_app(app)
