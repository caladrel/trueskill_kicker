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

io.on('connection', function (socket) {
    socket.emit('news', { hello: 'world' });
    socket.on('available', function (data) {
        socket.join('available');
        console.log(socket.id, 'player', data, 'is available');
    });
    socket.on('unavailable', function (data) {
        socket.leave('available');
        console.log(socket.id, 'player', data, 'is not available anymore');
    });
    socket.on('checkready', function (data) {
        //console.log(io.sockets.adapter.rooms['available']);
        socket.leave('available');
        socket.join('ready');
        if (!state.checking) {
            state.checking = true;
            state.players = [];
            socket.broadcast.to('available').emit('check', data);
        }
        if (state.players.length < 4) {
            state.players.push(data);
            socket.emit('ready', state.players);
            socket.broadcast.to('ready').emit('ready', state.players);
        }
        if (state.players.length == 4) {
            state.checking = false;
            socket.emit('finished');
            socket.broadcast.to('ready').emit('finished');
        }
        console.log(socket.id, 'player', data, 'is ready');
        console.log(state.players);
    });
    socket.on('ready', function (data) {
        if (state.checking) {
            socket.leave('available');
            socket.join('ready');
            if (state.players.length < 4) {
                state.players.push(data);
                socket.emit('ready', state.players);
                socket.broadcast.to('ready').emit('ready', state.players);
            }
            if (state.players.length == 4) {
                state.checking = false;
                socket.emit('finished', state.players);
                socket.broadcast.to('ready').emit('finished');
            }
            console.log(socket.id, 'player', data, 'is ready');
            console.log(state.players);
        }
    });
});

server.listen(process.env.PORT);
