function moveRelogio() {
    
    momentoAtual = new Date()
    hora = momentoAtual.getHours()
    minuto = momentoAtual.getMinutes()
    segundo = momentoAtual.getSeconds()
    str_segundo = new String(segundo)
    if (str_segundo.length == 1)
        segundo = "0" + segundo
    str_minuto = new String(minuto)
    if (str_minuto.length == 1)
        minuto = "0" + minuto
    str_hora = new String(hora)
    if (str_hora.length == 1)
        hora = "0" + hora
    horaImprimivel = hora + " : " + minuto + " : " + segundo
    document.form_relogio.relogio.value = horaImprimivel;
    
    setTimeout("moveRelogio()", 1000)
}




//funçao para atualizar dados na pagina Ranking (atualiza independente do que esta salvo no banco de dados)
function refreshData() {
    var nodelist = document.querySelectorAll('.ranking')

    for (i = 0; i < (nodelist.length / 8); i++) {
        let j = i * 8 + 1
        let data = nodelist[j].innerText;
        d = data.split('/')
        data = d[1] + '/' + d[0] + '/' + d[2]
        let nd = new Date()
        let nd2 = nd //.toLocaleString()
        let fim = new Date(nd2)
        fim.setHours(fim.getHours() - 3)
        let ini = new Date(data) //data
        let dif = Math.abs(fim.getTime() - ini.getTime());
        let dif1 = dif / (1000 * 60 * 60 * 24)
        let dif2 = Math.floor(dif1)
        nodelist[j + 1].innerText = dif2
        let diasT = parseInt(nodelist[j + 2].innerText)
        nodelist[j + 3].innerText = (100 * diasT / dif2).toFixed(1)
        let htot = parseInt(nodelist[j + 4].innerText)
        nodelist[j + 6].innerText = (htot / diasT).toFixed(1)
        nodelist[j + 5].innerText = (htot / dif2).toFixed(1)
    };
};




//Seleciona 1 e apeans 1 das 7 colunas disponiveis para filtro
function selectOnlyThis(id) {
    for (var i = 1; i <= 7; i++) {
        document.getElementById("check" + i).checked = false;
    }
    document.getElementById(id).checked = true;
}
