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

function broadcastcount (socket) {
    if ('available' in io.sockets.adapter.rooms)
        count = Object.keys(io.sockets.adapter.rooms['available']).length;
    else
        count = 0;
    socket.emit('availablecount', count);
    socket.broadcast.emit('availablecount', count);

    enable = state.checking || count > 3

    socket.emit('enable', enable);
    socket.broadcast.emit('enable', enable);
}

function broadcastready (socket) {
    socket.emit('ready', state.players);
    socket.broadcast.to('ready').emit('ready', state.players);
}


io.on('connection', function (socket) {
    socket.emit('news', { hello: 'world' });
    socket.on('available', function (data) {
        socket.join('available');
        console.log(socket.id, 'player', data, 'is available');
        broadcastcount(socket);
    });
    socket.on('unavailable', function (data) {
        socket.leave('available');
        console.log(socket.id, 'player', data, 'is not available anymore');
        broadcastcount(socket);
    });
    socket.on('checkready', function (data) {
        socket.leave('available');
        socket.join('ready');
        if (!state.checking) {
            state.checking = true;
            state.players = {};
            socket.broadcast.to('available').emit('check', data);
        }
        if (Object.keys(state.players).length < 4) {
            state.players[socket.id] = data;
            broadcastready(socket);
        }
        if (Object.keys(state.players).length == 4) {
            state.checking = false;
            socket.emit('finished');
            socket.broadcast.to('ready').emit('finished');
        }
        console.log(socket.id, 'player', data, 'is ready');
        console.log(state.players);
        broadcastcount(socket);
    });
    socket.on('ready', function (data) {
        if (state.checking) {
            socket.leave('available');
            socket.join('ready');
            if (Object.keys(state.players).length < 4) {
                state.players[socket.id] = data;
                broadcastready(socket);
            }
            if (Object.keys(state.players).length == 4) {
                state.checking = false;
                socket.emit('finished', state.players);
                socket.broadcast.to('ready').emit('finished');
            }
            console.log(socket.id, 'player', data, 'is ready');
            console.log(state.players);
            broadcastcount(socket);
        }
    });
    socket.on('disconnect', function () {
        if (socket.id in state.players) {
            delete state.players[socket.id];
            broadcastready(socket);
        }
        broadcastcount(socket);
    });
});

server.listen(process.env.PORT);
