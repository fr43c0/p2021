function moveRelogio() {
    nome = document.getElementsByClassName('navbar-brand')[0].innerText.toLowerCase().split(' ')[2].slice(0, -1)
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
    if (hora == 23 && minuto == 59 && segundo == 59) {
        fim = document.getElementById('sai-' + nome).click()

    }

    setTimeout("moveRelogio()", 1000)
}



// //==================================================================
// // referencia : https://docs.djangoproject.com/pt-br/3.2/ref/csrf/   <----------------------
// //funcao para pegar o cookie e o csrftoken...
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// const csrftoken = getCookie('csrftoken');


// function csrfSafeMethod(method) {
//     // these HTTP methods do not require CSRF protection
//     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }

// $.ajaxSetup({
//     beforeSend: function(xhr, settings) {
//         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//         }
//     }
// });
// //-------------------------------------***************--------------------------------

// // //=================== funcao que envia post =================================
// // referencia: https://stackoverflow.com/questions/18761069/django-ajax-post-extend-beforesend-method-used-for-csrf-protection    <----------------------
// // $.ajax({
// //    url: 'http://127.0.0.1:8000/',
// //    type: "POST",
// //    data:{'termino':123},

// // });
// // //=================== funcao que envia o post =================================



// function sendPostData(url, data) { // referencia: https://stackoverflow.com/questions/18761069/django-ajax-post-extend-beforesend-method-used-for-csrf-protection
//     $.ajax({
//         url: 'http://localhost:1234',
//         type: "POST",
//         data: data,
//     });
// }
// var origem = window.location.origin;
// console.log('origem ', origem)
// var url = 'http://meden.pythonanywhere.com/';
// var data = { "DERRUBAR": '' }
// sendPostData(url, data)
// console.log(data)

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



//  loadOnline()?

//Seleciona 1 e apeans 1 das 7 colunas disponiveis para filtro
function selectOnlyThis(id) {
    for (var i = 1; i <= 7; i++) {
        document.getElementById("check" + i).checked = false;
    }
    document.getElementById(id).checked = true;
}