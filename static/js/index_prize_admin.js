function show(data) {
  tab = ``;

  for (let r of data) {
    tab += `
      <div
  class="card w-full md:w-80 lg:w-96 bg-[#A7CBD9] hover:bg-[#A7CBD9] text-black glass"
>
  <div class="card-body">
    <h2 class="card-title">${r.fields.nama}</h2>
    <p class="">Stok: ${r.fields.stok}</p>
    <p class="">Poin: ${r.fields.poin}</p>
    <p class="">${r.fields.desc}</p>
    <div class="card-actions justify-end">
      <button class="btn btn-error" onclick={delData(${r.pk})}>Delete</button>
    </div>
  </div>
</div>
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
  $.get("/admin/prize/get", function (data) {
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
    url: "/admin/prize/add",
    data: {
      nama: $("#id_nama").val(),
      poin: $("#id_poin").val(),
      stok: $("#id_stok").val(),
      desc: $("#id_desc").val(),
      csrfmiddlewaretoken: csrftoken,
    },
    dataType: "json",
    success: function (data) {
      loadData();
      document.getElementById("id_nama").value = "";
      document.getElementById("id_poin").value = "";
      document.getElementById("id_stok").value = "";
      document.getElementById("id_desc").value = "";
      $.toast({
        text: data.instance,
        showHideTransition: "fade", // It can be plain, fade or slide
        bgColor: "#23B65D", // Background color for toast
        textColor: "#eee", // text color
        allowToastClose: false, // Show the close button or not
        hideAfter: 2000, // `false` to make it sticky or time in miliseconds to hide after
        stack: 5, // `fakse` to show one stack at a time count showing the number of toasts that can be shown at once
        textAlign: "left", // Alignment of text i.e. left, right, center
        position: "bottom-right", // bottom-left or bottom-right or bottom-center or top-left or top-right or top-center or mid-center or an object representing the left, right, top, bottom values to position the toast on page
      });
    },
  });
});

function delData(id) {
  $.ajax({
    type: "POST",
    url: `del/`,
    data: { id: id, csrfmiddlewaretoken: csrftoken },
    dataType: "json",
    success: function () {
      loadData();
      $.toast({
        text: "Prize dihapus",
        showHideTransition: "fade", // It can be plain, fade or slide
        bgColor: "#E01A31", // Background color for toast
        textColor: "#eee", // text color
        allowToastClose: false, // Show the close button or not
        hideAfter: 2000, // `false` to make it sticky or time in miliseconds to hide after
        stack: 5, // `fakse` to show one stack at a time count showing the number of toasts that can be shown at once
        textAlign: "left", // Alignment of text i.e. left, right, center
        position: "bottom-right", // bottom-left or bottom-right or bottom-center or top-left or top-right or top-center or mid-center or an object representing the left, right, top, bottom values to position the toast on page
      });
    },
  });
}
