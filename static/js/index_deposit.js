function show2(data) {
  let tab = ``;
  for (let r of data) {
    let par = ``;
    if (r.fields.isApprove == "DITERIMA") {
      par = `<p class="font-bold text-green-400">DITERIMA</p>`;
    } else if (r.fields.isApprove == "PENDING") {
      par = `<p class="font-bold text-blue-400">PENDING</p>`;
    } else if (r.fields.isApprove == "DITOLAK") {
      par = `<p class="font-bold text-red-400">DITOLAK</p>`;
    }
    tab += `
        <div
          class="card w-full md:w-80 lg:w-96 bg-[#B6C790] hover:bg-[#B6C790] text-black glass"
        >
          <div class="card-body">
            <h2 class="card-title">${r.fields.date}</h2>
            <div class="flex w-fit gap-3">
              <p class="font-bold w-fit">${r.fields.jenisSampah}</p>
              <p class="font-bold w-fit">${r.fields.beratSampah} Kg</p>
            </div>
            <p class="font-bold">Poin: ${r.fields.poin}</p>
            <p class="font-bold">Saldo: ${r.fields.totalHarga}</p>
            ${par}
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

function loadData2() {
  $.get("/deposit/get/", function (data) {
    show2(data);
  });
}

$(document).ready(function () {
  loadData2();
});

$(document).on("submit", "#buatproject", function (e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: "/deposit/add/",
    data: {
      jenisSampah: $("#id_jenisSampah").val(),
      beratSampah: $("#id_beratSampah").val(),
      csrfmiddlewaretoken: csrftoken,
    },
    dataType: "json",
    success: function (data) {
      loadData2();
      document.getElementById("id_jenisSampah").value = "";
      document.getElementById("id_beratSampah").value = "";
      if (data.instance == "Deposit diajukan") {
        $.toast({
          text: "Deposit berhasil diajukan",
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
          text: "Input tidak valid",
          showHideTransition: "fade", // It can be plain, fade or slide
          bgColor: "#E01A31", // Background color for toast
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
