function showPrizeRedeem(data) {
  tab = ``;

  for (let r of data) {
    tab += `
      <div
  class="card w-full md:w-80 lg:w-96 bg-[#A7CBD9] hover:bg-[#A7CBD9] text-black glass"
>
  <div class="card-body">
    <h2 class="card-title">${r.fields.nama}</h2>
    <p class="">${r.fields.desc}</p>
    <div class="card-actions justify-end">
      <button class="btn btn-accent" onclick={use(${r.pk})}>Use</button>
    </div>
  </div>
</div>
    `;
  }

  console.log("show");
  document.getElementById("tableRedeem").innerHTML = tab;
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

function loadDataRedeem() {
  $.get("/prize/get_prize_redeem/", function (data) {
    showPrizeRedeem(data);
  });
}

function showPrize(data) {
  tab = ``;

  for (let r of data) {
    tab += `
      <div
  class="card w-full md:w-80 lg:w-96 bg-[#A7CBD9] hover:bg-[#A7CBD9] text-black glass"
>
  <div class="card-body">
    <h2 class="card-title">${r.fields.nama}</h2>
    <p class="">${r.fields.stok}</p>
    <p class="">${r.fields.poin}</p>
    <p class="">${r.fields.desc}</p>
    <div class="card-actions justify-end">
      <button class="btn btn-accent" onclick={redeem(${r.pk})}>Redeem</button>
    </div>
  </div>
</div>
    `;
  }

  console.log("show");
  document.getElementById("table").innerHTML = tab;
}

function loadDataPrize() {
  $.get("/prize/get_prize/", function (data) {
    showPrize(data);
  }).then(function () {
    $.get("/prize/get_prize_redeem/", function (data) {
      showPrizeRedeem(data);
    });
  });
}

$(document).ready(function () {
  loadDataPrize();
});

function redeem(id) {
  $.ajax({
    type: "POST",
    url: `redeem/${id}`,
    data: { csrfmiddlewaretoken: csrftoken },
    dataType: "json",
    success: function (data) {
      loadDataPrize();
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
}

function use(id) {
  $.ajax({
    type: "POST",
    url: `use/${id}`,
    data: { csrfmiddlewaretoken: csrftoken },
    dataType: "json",
    success: function (data) {
      loadDataRedeem();
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
}
