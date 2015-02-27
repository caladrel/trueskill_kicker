var http = require('http'),
    httpProxy = require('http-proxy')
    Server = require('socket.io');

var targetUrl = 'http://127.0.0.1:' + process.env.DJANGO_PORT

var proxy = httpProxy.createProxyServer({});
var server = http.createServer(function(req, res) {
  proxy.web(req, res, {target: targetUrl});
});

var io = new Server(server);

var state = {
   checking: false,
   players: []
}

function broadcastcount () {
    if ('available' in io.sockets.adapter.rooms)
        count = Object.keys(io.sockets.adapter.rooms['available']).length;
    else
        count = 0;

    io.emit('availablecount', count);

    enable = state.checking || count > 3

    io.emit('enable', enable);
}

function broadcastready () {
    io.sockets.in('ready').emit('ready', state.players);
}

function finish () {
    state.checking = false;
    io.sockets.in('ready').emit('finished');
    if ('ready' in io.sockets.adapter.rooms)
        for (id in io.sockets.adapter.rooms['ready'])
            io.sockets.connected[id].leave('ready');
}

function ready (id, player) {
    if (Object.keys(state.players).length < 4) {
        state.players[id] = player;
        broadcastready();
    }
    if (Object.keys(state.players).length == 4)
        finish();

    console.log(id, 'player', player, 'is ready');
    console.log(state.players);
    broadcastcount();
}

io.on('connection', function (socket) {
    broadcastcount()

    socket.on('available', function (data) {
        socket.join('available');
        console.log(socket.id, 'player', data, 'is available');
        broadcastcount();
    });
    socket.on('unavailable', function (data) {
        socket.leave('available');
        console.log(socket.id, 'player', data, 'is not available anymore');
        broadcastcount();
    });
    socket.on('checkready', function (data) {
        socket.leave('available').join('ready');
        if (!state.checking) {
            state.checking = true;
            state.players = {};
            io.sockets.in('available').emit('check', data);
        }
        ready(socket.id, data);
    });
    socket.on('ready', function (data) {
        console.log('got ready');
        if (state.checking) {
            socket.leave('available').join('ready');
            ready(socket.id, data);
        }
    });
    socket.on('disconnect', function () {
        if (socket.id in state.players) {
            delete state.players[socket.id];
            broadcastready();
        }
        broadcastcount();
    });
});

server.listen(process.env.PORT);
