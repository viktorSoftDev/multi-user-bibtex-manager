var allCol = document.querySelector("#colselect");
allCol.addEventListener("change", function() {
  var col = document.querySelectorAll(".toggleColumn");
  renderTable(col);
});
var allrow = document.querySelector("#numentries");
allrow.addEventListener("change", function() {
  var col = document.querySelectorAll(".toggleColumn");
  renderTable(col);
});

function renderTable(col) {
  columnList = [];
  for (var i = 0; i < col.length; i++) {
    columnList[i] = {
      targets: [parseInt(col[i].value)],
      visible: col[i].selected,
      className: "mdl-data-table__cell--non-numeric"
    };
  }
  var numrow;
  var rows = document.querySelectorAll(".rows");
  for (var i = 0; i < rows.length; i++) {
    if (rows[i].selected) {
      numrow = rows[i].value;
    }
  }
  
  // Initializing datatables. must be reinitialized every time there is a change
  // due to how the plugin is configured. therefore destroy = true.
  $("#example").DataTable({
    // Thx to datatables.net for this jquery plugin
    destroy: true,
    order: [[2, "asc"]],
    scrollX: true,
    sDom: "frtip",
    iDisplayLength: parseInt(numrow),
    searchPlaceholder: "something",
    language: {
      search: "_INPUT_",
      searchPlaceholder: "Filter by anything...",
      lengthMenu: "Display _MENU_ records"
    },
    columnDefs: columnList
  });
}

jQuery(document).ready(function($) {
  $(".modal").modal();
  $(".fixed-action-btn").floatingActionButton({});
  $(".fixed-action-btn").floatingActionButton("open");
  $("select").formSelect();
  $(".tooltipped").tooltip({ delay: 50 });
  renderTable(document.querySelectorAll(".toggleColumn"));

  $(".clickable-row").click(function() {
    window.location = $(this).data("href");
  });
});
