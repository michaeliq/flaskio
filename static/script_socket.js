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

socket.on('connect',(id_cli)=>{
    idUser = id_cli;
});

socket.on('message', (data) => {
        if(data['sid'] == idUser ){
            $('#mensajes').append('<li class="ml-auto p-2">' + data['name'] + ": " + data['msg'] + '</li>');
        }else{
            $('#mensajes').append('<li>' + data['name'] + ": " + data['msg'] + '</li>');
        };
        $('#content_info').removeClass('d-none');
        $('#info').text(data['name']);
    });


