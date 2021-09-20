


function moveRelogio(){
    momentoAtual = new Date()
    hora = momentoAtual.getHours()
    minuto = momentoAtual.getMinutes()
    segundo = momentoAtual.getSeconds()
    str_segundo = new String (segundo)
    if (str_segundo.length == 1)
       segundo = "0" + segundo
    str_minuto = new String (minuto)
    if (str_minuto.length == 1)
       minuto = "0" + minuto
    str_hora = new String (hora)
    if (str_hora.length == 1)
       hora = "0" + hora
    horaImprimivel = hora + " : " + minuto + " : " + segundo
    document.form_relogio.relogio.value = horaImprimivel;
    if(hora == 23 && minuto ==59&& segundo ==59)
       fim=document.getElementById('sai').click()
 
       
   
    setTimeout("moveRelogio()",1000)
 }


  function loadOnline(e){
    const xhr=new XMLHttpRequest();
    xhr.open('GET', './../../static/ponto/js/online.json',true)
    xhr.onload=function(){
       if(this.status===200){
         let dono=document.getElementById('dono').textContent.toLowerCase()
         resposta=(this.responseText);
         const online=JSON.parse(this.responseText)
         if (dono != null){
            online.forEach(function(on){
               // if (on != dono && on['a'] != 0){
               //    var oldDate = "2010-03-05T07:03:51-0800";
               //    var dateObj = moment(oldDate, "YYY-MM-DDTHH:mm:ssZ").toDate();
               // }
               
            })
         }
        }
    }
     xhr.send();
     resposta.forEach(

     )
     setTimeout("loadOnline()",10000)
  }
//  loadOnline()
