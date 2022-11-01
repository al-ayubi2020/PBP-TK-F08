const table = (data) => `
  <tr>
    <td> ${data.fields.date} </td>
    <td> ${data.fields.jumlah} </td>
  </tr>`

function show(data) {
  for (let r of data) {
    tab += `
    $('#parent').append($('<tr><td>' + ${r.fields.date} + '</td>   <td>' + ${r.fields.jumlah} + '</td></tr>'))
    `;
  }

  document.getElementById("table").innerHTML = tab;
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

function loadData() {
  $.get("/withdraw/get/", function (data) {
    show(data);
  });
}

$(document).ready(function () {
  loadData();
});

$(document).on("submit", "#buatproject", function (e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: "/withdraw/add/",
    data: {
      jumlah: $("#id_jumlah").val(),
      csrfmiddlewaretoken: csrftoken,
    },
    dataType: "json",
    success: function (data) {
      loadData();
      document.getElementById("id_jumlah").value = "";
      if (data.instance == "Saldo Kurang") {
        $.toast({
          text: "Saldo Kurang",
          showHideTransition: "fade", // It can be plain, fade or slide
          bgColor: "#E01A31", // Background color for toast
          textColor: "#eee", // text color
          allowToastClose: false, // Show the close button or not
          hideAfter: 2000, // `false` to make it sticky or time in miliseconds to hide after
          stack: 5, // `fakse` to show one stack at a time count showing the number of toasts that can be shown at once
          textAlign: "left", // Alignment of text i.e. left, right, center
          position: "bottom-right", // bottom-left or bottom-right or bottom-center or top-left or top-right or top-center or mid-center or an object representing the left, right, top, bottom values to position the toast on page
        });
      } else if (data.instance == "Input tidak valid") {
        $.toast({
          text: "Input tidak valid",
          showHideTransition: "fade", // It can be plain, fade or slide
          bgColor: "#23B65D", // Background color for toast
          textColor: "#eee", // text color
          allowToastClose: false, // Show the close button or not
          hideAfter: 2000, // `false` to make it sticky or time in miliseconds to hide after
          stack: 5, // `fakse` to show one stack at a time count showing the number of toasts that can be shown at once
          textAlign: "left", // Alignment of text i.e. left, right, center
          position: "bottom-right", // bottom-left or bottom-right or bottom-center or top-left or top-right or top-center or mid-center or an object representing the left, right, top, bottom values to position the toast on page
        });
      } else {
        $.toast({
          text: "Berhasil Ditarik",
          showHideTransition: "fade", // It can be plain, fade or slide
          bgColor: "#23B65D", // Background color for toast
          textColor: "#eee", // text color
          allowToastClose: false, // Show the close button or not
          hideAfter: 2000, // `false` to make it sticky or time in miliseconds to hide after
          stack: 5, // `fakse` to show one stack at a time count showing the number of toasts that can be shown at once
          textAlign: "left", // Alignment of text i.e. left, right, center
          position: "bottom-right", // bottom-left or bottom-right or bottom-center or top-left or top-right or top-center or mid-center or an object representing the left, right, top, bottom values to position the toast on page
        });
      }
    },
  });
});
