$(document).ready(function(){
  $('#id_onpage').change(function () {
    PARAMS.page = 1;
    PARAMS.onpage = $(this).val();
    document.location = document.location.pathname + "?" + $.param(PARAMS);
  });
});
