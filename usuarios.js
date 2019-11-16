function select_usuarios(_box) {
    $.ajax({
        url: '/usuarios_call',
        type: 'POST',
        success: function (ress) {
            users = ress;
            pintar_tabla_usuarios(ress, _box)
        },
        error: function (err) {
            console.log(err);
        }
    });
}
 
function pintar_tabla_usuarios(user_data, _box) {
    $("#" + _box).empty();
    var row_print = '<table id="tabla_usuarios" class="highlight striped responsive-table"><thead><tr><th>Id</th><th>Nombre</th><th>Puesto</th><th>Fecha Alta</th><th>Celular</th><th>Jefe Inmediato</th><th>Estatus</th></thead><tbody>';
    for (i in user_data) {
        row_print += '<tr id="'+i+'" class="row_user">';
        for (x in user_data[i]) {
            if(x < 7){
                if(x == 1){
                    row_print += '<td>' + user_data[i][x] + '<br>' + user_data[i][18] +'</td>';
                }else {
                    row_print += '<td>' + user_data[i][x] + '</td>';
                }
                
            }
        }
        row_print += '</tr>';
    }
    $("#" + _box).append(row_print);
    row_print += '</tbody></table>'
    console.log(users)
}