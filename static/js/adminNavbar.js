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
  }
}

$(document).ready(function () {
  loadDataNav();
});
