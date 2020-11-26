const socket = io();	
const nombreUsuario = window.prompt('Cual es tu nombre?', 'invitado');
		
document.getElementById('nombreUsuario').innerHTML = nombreUsuario;

$('#send').on('click', function(){
    socket.send({
        'name':nombreUsuario,
        'msg':$('#myMessage').val()});
    $('#myMessage').val('')
});

socket.on('message', (data) => {
        $('#messages').append('<li>' + data['name'] + ": " + data['msg'] + '</li>');
        $('#content_info').removeClass('d-none');
        $('#info').text(data['name']);
    });


