var http = require("http");

var port = process.env.PORT || 5000;

http.createServer(function(request, response) {
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("Hello World, this is a Jeu de Taquin");
  response.end();
}).listen(port);