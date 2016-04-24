var express = require('express');
var app = express();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
var bodyParser = require('body-parser');
var exec = require('child_process').exec;

// base de datos
var db = [{
	nombre: '',
  	tarjeta: '8754702864680439',
  	enrolado: true,
  	factor: { factor: '1.12280701754' }}];
var cliente = 0;
var action;
// usar peticiones post
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// urls para app
app.use('/public', express.static(__dirname+'/public'));

app.get('/', function(req, res){
	res.sendFile(__dirname+'/ola.html');
});

app.get('/admin', function(req, res){
	res.sendFile(__dirname+'/admin.html');
});

app.post('/guardar-cliente', function(req, res){
	var tarjeta = Math.random().toString();
	tarjeta = tarjeta.split('.');
	req.body.tarjeta = tarjeta[1];
	req.body.enrolado = false;
	db.push(req.body);
	res.send('ok');
});

app.post('/listar-clientes', function(req, res){
	res.send(db);
});

app.post('/validate', function(req, res){
	//console.log(req.body);
	cliente = req.body;
	action = "enrolar";
	res.send("OK");
});

app.post('/fact', function(req, res){
	fact = req.body;
	//console.log(cliente);
	if(action == "enrolar"){
		db[cliente.id].enrolado = true;
		db[cliente.id].factor = fact;
		io.emit("changeRoll");
	}
	else if(action == "validar"){
		//console.log(db[0]);
		//console.log(fact);
		//console.log(cliente.factor.factor)
		console.log(db[0].factor)
		console.log(parseFloat(fact.factor)+0.03)
		console.log(parseFloat(fact.factor)-0.03)
		db.forEach(function(cliente){
			if(cliente.factor.factor < (parseFloat(fact.factor)+0.03) && cliente.factor.factor > (parseFloat(fact.factor)-0.03)){
				io.emit("hay");
			}
		})
	}
	res.send("OK");
});

// conecciones con web sockets o canales
io.on('connection', function(socket){

  socket.on('exec', function(msg){
  	exec('python ~/Desktop/banquito/olakase.py', output);
  });
  socket.on('validarPaps', function(msg){
  	action = "validar";
  });

});

// funcion para recibir metricas de python
function output(error, stdout, stderr){
	var result = stdout.replace('\n', '');
	result = result.replace(' ', '');

	if(result == '100-20'){
		io.emit('changeDisplay', 'now');
	}
}

// poner a escuchar la app en un puerto
http.listen(8000, function(){
	console.log('server on 8000');
});