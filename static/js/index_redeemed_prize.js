async function getPrize() {
    return fetch("/prize/redeemjson/").then((res) => res.json()) // Get JSON data of Prize
  }

async function refresher() { // Update asynchronously
    document.getElementById("prizes").innerHTML = ""
    const prize = await getPrize()

    let htmlString = ``

    prize.forEach((item) => {
      htmlString += `\n
      <div class="card w-full md:w-80 lg:w-96 bg-[#A7CBD9] hover:bg-[#A7CBD9] text-black glass">
        <div class="card-body">
          <h2 class="card-title">${item.fields.nama}</h2>
          <p class="poin">Stok: ${item.fields.stok}</p>
          <p class="desc">${item.fields.desc}</p>
          <div class="card-actions justify-end">
            <button id="redeem" class="btn btn-error" onclick={usePrize(${item.pk})}>Use</button>
          </div>
        </div>
      </div>`
    });

    document.getElementById("prizes").innerHTML = htmlString
  }

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
var csrftoken = getCookie("csrftoken");

function usePrize(id) { // Use prize (decrement stock or delete item from db) using AJAX
    $.ajax({
        type: "POST",
        url: `useprize/${id}/`,
        dataType: "json",
        data: { csrfmiddlewaretoken: csrftoken },
        success: function (data) {
            refresher()
            $.toast({
                heading: "Success",
                text: data.instance,
                bgColor: "#13970B",
                position: {
                    right:30,
                    top:80,
                },
                icon: 'success'
            });
        },
        error: function(jqXHR, exception) {
            if (jqXHR.status === 0) {
                alert('Not connect.\n Verify Network.');
            } else if (jqXHR.status == 404) {
                alert('Requested page not found. [404]');
            } else if (jqXHR.status == 500) {
                alert('Internal Server Error [500].');
            } else if (exception === 'parsererror') {
                alert('Requested JSON parse failed.');
            } else if (exception === 'timeout') {
                alert('Time out error.');
            } else if (exception === 'abort') {
                alert('Ajax request aborted.');
            } else {
                alert('Uncaught Error.\n' + jqXHR.responseText);
            }
        },
    });
}

$(document).ready(function () {
    refresher();
});
    
