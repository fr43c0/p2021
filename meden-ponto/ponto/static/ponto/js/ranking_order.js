//FUNCAO QUE ORDENA O RANKING PELA COLUNA 5
//POSE SER ACRESCENTADO UM BOTAO  NAS COLUNAS PARA ISSO



function convertToTimestamp(d) {
    let data = d.split("/")
    let ddtt = new Date(data[2], data[1], data[0])
    return ddtt.getTime()
}

function sortTable(N) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("rank");
    switching = true;
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
        // console.log('indo')
        //start by saying: no switching is done:
        switching = false;
        rows = table.rows;

        /*Loop through all table rows (except the
        first, which contains table headers):*/
        for (i = 1; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare,
            one from current row and one from the next:*/
            x = rows[i].getElementsByTagName("td")[N];
            y = rows[i + 1].getElementsByTagName("td")[N];
            //check if the two rows should switch place:
            if (N == 1) {

                xd = convertToTimestamp(x.innerHTML)
                yd = convertToTimestamp(y.innerHTML)
                if (xd < yd) {
                    shouldSwitch = true;
                    break;
                }
            } else {
                if (Number(x.innerHTML.replace(',', '.')) < Number(y.innerHTML.replace(',', '.'))) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            }

        }
        if (shouldSwitch) {
            // console.log('fazer troca')
            /*If a switch has been marked, make the switch
            and mark that a switch has been done:*/
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }

}

function vai() {
    setTimeout(sortTable(Number(this.id)), 1000)
}
// Função para adicionar uma espera de evento em t
function load() {
    // var el = document.getElementById("i2");
    // el.addEventListener("click", vai, false);
    document.querySelectorAll('.fa-sort').forEach(item => {
        item.addEventListener('click', vai, false)
    })
}
document.addEventListener("DOMContentLoaded", load, false);


// setTimeout(sortTable, 1000)