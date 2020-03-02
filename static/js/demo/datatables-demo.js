// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({
    dom: 'B<"clear">lfrtip',
    buttons: {
      name:'primary',
      buttons: ['copy', 'csv', 'excel', 'pdf']
    },
    stateSave: true
  });
});
