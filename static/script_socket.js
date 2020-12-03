const socket = io();	
const nombreUsuario = window.prompt('Cual es tu nombre?', 'invitado');
var idUser = null;
		
document.getElementById('nombreUsuario').innerHTML = nombreUsuario;

$('#send').on('click', function(){
    socket.send({
        'name':nombreUsuario,
        'msg':$('#myMessage').val()});
    $('#myMessage').val('')
});

$('#link-room').addEventListener('click',()=>{
    socket.emit('join','user added');
});

socket.on('message', (data) => {
        if(data['sid'] == idUser ){
            $('#mensajes').append('<li class="mr-auto p-2"><a class="link-room" href="#">' + data['name'] + "</a>: " + data['msg'] + '</li>');
        }else{
            $('#mensajes').append('<li class="ml-auto p-2"><a class="link-room" href="#">' + data['name'] + "</a>: " + data['msg'] + '</li>');
        };
        $('#content_info').removeClass('d-none');
        $('#info').text(data['name']);
    });

socket.on('writing',(usuario)=>{
    console.log(usuario, ' is typing')
});

document.getElementById('myMessage').addEventListener('keypress', ()=>{
    socket.emit('writing',nombreUsuario);
});


