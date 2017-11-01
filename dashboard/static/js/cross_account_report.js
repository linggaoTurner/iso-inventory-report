$(document).ready(function() {
  //setup bootstrap datatable style with search bar, pagination, order
  $('#datatable').DataTable({
      "dom":"<'row'<'col-md-6'l><'col-md-3'<'toolbar'>><'col-md-3'Bf>>" +
      "<'row'<'col-md-6'><'col-md-6'>>" +
      "<'row'<'col-md-12't>><'row'<'col-md-4'><'col-md-8'ip>>",

  });
  //bootstrap validation plugin language setup
  $.validate({
    lang: 'en'
  });

});


var submitClickable = false;

var changedArray = []
function changeEvent()
{
  $("#submit").attr('class', 'btn btn-primary pull-right');
  submitClickable = true;
  var sidExist = false;

  for (var i=0; i<changedArray.length;i++)
  {

    if(changedArray[i]['account_id'] == $(this).closest('tr').find('td').eq(1).find("label").text())
    {
      changedArray[i]['ExecutiveSponsor'] = $(this).closest('tr').find('td').eq(3).find("input").val();
      changedArray[i]['ExecutiveSponsorEmail'] = $(this).closest('tr').find('td').eq(4).find("input").val();
      changedArray[i]['TechnicalContact'] =$(this).closest('tr').find('td').eq(5).find("input").val();
      changedArray[i]['TechnicalContactEmail'] = $(this).closest('tr').find('td').eq(6).find("input").val();
      sidExist = true;
    }
  }
  if (!sidExist)
  {
    var obj = new Object();
    obj['account_id'] = $(this).closest('tr').find('td').eq(1).find("label").text();
    obj['ExecutiveSponsor'] = $(this).closest('tr').find('td').eq(3).find("input").val();
    obj['ExecutiveSponsorEmail'] = $(this).closest('tr').find('td').eq(4).find("input").val();
    obj['TechnicalContact'] =$(this).closest('tr').find('td').eq(5).find("input").val();
    obj['TechnicalContactEmail'] = $(this).closest('tr').find('td').eq(6).find("input").val();

    changedArray.push(obj);
  }
  console.log(changedArray)


}
$('#cross_account_table').on('change', 'input', changeEvent);

//submit modified info from table
$('#submit').click(function(){
  if(submitClickable){
    var unchangeExecutiveSponsor = true;
    var unchangeExecutiveSponsorEmail = true;
    var unchangeTechnicalContact = true;
    var unchangeTechnicalContactEmail = true;
    for (var i = 0; i<jsonList.length;i++)
    {
      for (var j = 0; j<changedArray.length;j++)
      {

        if(jsonList[i]['account_id'] == changedArray[j]['account_id'])
        {
          if(jsonList[i]['ExecutiveSponsor'] == null && changedArray[j]['ExecutiveSponsor'] == 'None')
          {
            unchangeExecutiveSponsor = true
          }
          else if(jsonList[i]['ExecutiveSponsor'] == changedArray[j]['ExecutiveSponsor']){
            unchangeExecutiveSponsor = true
          }
          else {
            unchangeExecutiveSponsor = false
          }

          if(jsonList[i]['ExecutiveSponsorEmail'] == null && changedArray[j]['ExecutiveSponsorEmail'] == 'None')
          {
            unchangeExecutiveSponsorEmail = true
          }
          else if(jsonList[i]['ExecutiveSponsorEmail'] == changedArray[j]['ExecutiveSponsorEmail']){
            unchangeExecutiveSponsorEmail = true
          }
          else {
            unchangeExecutiveSponsorEmail = false
          }

          if(jsonList[i]['TechnicalContact'] == null && changedArray[j]['TechnicalContact'] == 'None')
          {
            unchangeTechnicalContact = true
          }
          else if(jsonList[i]['TechnicalContact'] == changedArray[j]['TechnicalContact']){
            unchangeTechnicalContact = true
          }
          else {
            unchangeTechnicalContact = false
          }

          if(jsonList[i]['TechnicalContactEmail'] == null && changedArray[j]['TechnicalContactEmail'] == 'None')
          {
            unchangeTechnicalContactEmail = true
          }
          else if(jsonList[i]['TechnicalContactEmail'] == changedArray[j]['TechnicalContactEmail']){
            unchangeTechnicalContactEmail = true
          }
          else {
            unchangeTechnicalContactEmail = false
          }

          if(unchangeExecutiveSponsor
            && unchangeExecutiveSponsorEmail
            && unchangeTechnicalContact
            && unchangeTechnicalContactEmail)
          {
            changedArray.splice(j,1);


          }
        }
      }
    }
    if(changedArray.length>0)
    {
    //make a json file then send it to server through ajax
      var formData = new FormData();
      formData.append("list", JSON.stringify(changedArray));

      $.ajax({
        url:$('#cross_account_table').attr('action'),
        type: 'POST',
        csrfmiddlewaretoken: '{{ csrf_token }}',
        data: formData,
        async: true,
        cache: false,
        contentType: false,
        processData: false,

        "success": function(result) {
          if(result.success == false)
          {
            console.log('submit failed')
          }
          else {
            window.location.reload();
          }
        }
      });
    }
    else {
      alert("You did not make any changes");
    }
  }
});
