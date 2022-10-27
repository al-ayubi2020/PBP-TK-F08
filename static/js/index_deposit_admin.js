function show(data) {
  tab = ``;

  for (let r of data) {
    tab += `
        <div
    class="card w-full md:w-80 lg:w-96 bg-[#B6C790] hover:bg-[#B6C790] text-black glass"
  >
    <div class="card-body">
      <h2 class="card-title">${r.fields.date}</h2>
      <p class="font-bold">Username: ${r.fields.username}</p>
      <div class="flex w-fit gap-2">
        <p class="font-bold w-fit">${r.fields.jenisSampah}</p>
        <p class="font-bold w-fit">${r.fields.beratSampah} Kg</p>
      </div>
      <p class="font-bold">Poin: ${r.fields.poin}</p>
      <p class="font-bold">Saldo: ${r.fields.totalHarga}</p>
      <div class="card-actions justify-end">
        <button class="btn btn-success btn-circle" onclick={accData(${r.pk})}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-6 h-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M4.5 12.75l6 6 9-13.5"
            />
          </svg>
        </button>
        <button class="btn btn-error btn-circle" onclick={delData(${r.pk})}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-6 h-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>

      `;
  }

  console.log("show");
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

let count = 0;
function loadDataNav() {
  $.get("/admin/deposit/get/count/", function (data) {
    count = data;
    console.log(count);
    showCount();
  });
}

function showCount() {
  if (count > 0) {
    document.getElementById("notif").className =
      "indicator-item badge badge-secondary";
    document.getElementById("notif").innerHTML = count;

    document.getElementById("notif2").className =
      "indicator-item indicator-center badge badge-secondary";
    document.getElementById("notif2").innerHTML = count;
  } else {
    document.getElementById("notif").className =
      "indicator-item badge badge-secondary hidden";

    document.getElementById("notif2").className =
      "indicator-item indicator-center badge badge-secondary hidden";
  }
}

function loadData() {
  $.get("/admin/deposit/get", function (data) {
    show(data);
  }).then(function () {
    loadDataNav();
  });
}

$(document).ready(function () {
  loadData();
});

$(document).on("submit", "#buatproject", function (e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: "/admin/deposit/add/",
    data: {
      user: $("#user").val(),
      jenisSampah: $("#id_jenisSampah").val(),
      beratSampah: $("#id_beratSampah").val(),
      csrfmiddlewaretoken: csrftoken,
    },
    dataType: "json",
    success: function (data) {
      loadData();
      document.getElementById("user").value = "";
      document.getElementById("id_jenisSampah").value = "";
      document.getElementById("id_beratSampah").value = "";
      console.log(data);
      $.toast({
        text: "Deposit Dibuat",
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

function accData(id) {
  $.ajax({
    type: "POST",
    url: `acc/${id}`,
    data: { csrfmiddlewaretoken: csrftoken },
    dataType: "json",
    success: function () {
      loadData();
      $.toast({
        text: "Deposit diterima",
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

function delData(id) {
  $.ajax({
    type: "POST",
    url: `del/${id}`,
    data: { csrfmiddlewaretoken: csrftoken },
    dataType: "json",
    success: function () {
      loadData();
      $.toast({
        text: "Deposit ditolak",
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
