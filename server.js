var http = require('http'),
    httpProxy = require('http-proxy')
    Server = require('socket.io');

var targetUrl = 'http://127.0.0.1:' + process.env.DJANGO_PORT

var proxy = httpProxy.createProxyServer({});
var server = http.createServer(function(req, res) {
  proxy.web(req, res, {target: targetUrl});
});

var io = new Server(server);

server.listen(process.env.PORT);
