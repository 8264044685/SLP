function addTechnicalPdfFile(input) {

  if (input.files && input.files[0]) {
        var tech_file_count = $('#technical_uploaded_file_count').val();

        if( input.files[0].size > 2000000)
        {
            swal("Error!", "Please select file less then 2Mb!", "error", {
                button: "Ok!",  
            });
        }else if( input.files[0].type != 'application/pdf'){
            swal("Error!", "Please select pdf file!", "error", {
                button: "Ok!",
            });
        }else{
            var pdfHtml = "";
            pdfHtml += '<li id="display_tech_file_'+tech_file_count+'">';
                pdfHtml += '<div class="box">';
                    pdfHtml += '<a href="javascript:void(0);" class="remove1" onclick="removeTechnicalFile('+tech_file_count+')">';
                        pdfHtml += '<i class="icofont icofont-close"></i>';
                    pdfHtml += '</a>';
                    pdfHtml += '<div class="icon">';
                        pdfHtml += '<i class="icofont icofont-file-pdf"></i>';
                    pdfHtml += '</div>';
                    pdfHtml += '<span style="display: inline-block;width: 75px;">'+input.files[0].name+'</span>';
                pdfHtml += '</div>';
            pdfHtml += '</li>';
            $('#js_uploaded_pdf').append(pdfHtml);

            var prev_file_count = tech_file_count;
            $('.technical_file_'+tech_file_count).css('display','none');
            tech_file_count++;
            var tech_input_file = '<input name="technical_datasheet_'+tech_file_count+'" id="technical_file_'+tech_file_count+'" type="file" class="custom-file-input js_technical_file  technical_file_'+tech_file_count+'" onchange="addTechnicalPdfFile(this)" accept=".pdf"/>';
            $('.technical_file_'+prev_file_count).after(tech_input_file);
            $('#technical_uploaded_file_count').val(tech_file_count);
        }
    }
}
function removeTechnicalFile(file_count){
    var tech_file_input = document.getElementById('technical_file_'+file_count);    
    tech_file_input.remove();

    var li_display_file = document.getElementById('display_tech_file_'+file_count);
    li_display_file.remove();
}


function addGuidelinesPdfFile(input){

    if (input.files && input.files[0]) {
        var guidelines_file_count = $('#guidelines_uploaded_file_count').val();

        if(input.files[0].size > 2000000){
            swal("Error!", "Please select file less then 2Mb!", "error", {
                button: "Ok!",
            });
        }else if( input.files[0].type != 'application/pdf'){
            swal("Error!", "Please select pdf file!", "error", {
                button: "Ok!",
            });
        }else{
            var pdfHtml = "";
            pdfHtml += '<li id="display_guidelines_file_'+guidelines_file_count+'">';
                pdfHtml += '<div class="box">';
                    pdfHtml += '<a href="javascript:void(0);" class="remove1" onclick="removeguidelinesFile('+guidelines_file_count+')">';
                        pdfHtml += '<i class="icofont icofont-close"></i>';
                    pdfHtml += '</a>';
                    pdfHtml += '<div class="icon">';
                        pdfHtml += '<i class="icofont icofont-file-pdf"></i>';
                    pdfHtml += '</div>';
                    pdfHtml += '<span style="display: inline-block;width: 75px;">'+input.files[0].name+'</span>';
                pdfHtml += '</div>';
            pdfHtml += '</li>';
            $('#guide_file_pdf_show').append(pdfHtml);

            var prev_file_count = guidelines_file_count;
            $('.guidelines_file_'+guidelines_file_count).css('display','none');
            guidelines_file_count++;
            var tech_input_file = '<input name="application_guidelines_'+guidelines_file_count+'" id="guidelines_file_'+guidelines_file_count+'" type="file" class="custom-file-input js_guideline_file  guidelines_file_'+guidelines_file_count+'" onchange="addGuidelinesPdfFile(this)" accept=".pdf"/>';
            $('.guidelines_file_'+prev_file_count).after(tech_input_file);
            $('#guidelines_uploaded_file_count').val(guidelines_file_count);
        }
    }
}

function removeguidelinesFile(file_count){
    var guideline_file_input = document.getElementById('guidelines_file_'+file_count);
    guideline_file_input.remove();

    var li_display_file = document.getElementById('display_guidelines_file_'+file_count);
    li_display_file.remove();
}

function addVideoFile(input){
    if (input.files && input.files[0]) {
        var video_file_count = $('#video_uploaded_file_count').val();
        var file_type = input.files[0].type;
        console.log("file type is",file_type)
        if( input.files[0].size > 2000000)
        {
            swal("Error!", "Please select file less then 2Mb!", "error", {
                button: "Ok!",
            });
        }else if( input.files[0].type != 'video/mp4'){
            swal("Error!", "Please select video mp4 file!", "error", {
                button: "Ok!",
            });
        }else{
            var pdfHtml = "";
            pdfHtml += '<li id="display_video_file_'+video_file_count+'">';
                pdfHtml += '<div class="box">';
                    pdfHtml += '<a href="javascript:void(0);" class="remove1" onclick="removeVideoFile('+video_file_count+')">';
                        pdfHtml += '<i class="icofont icofont-close"></i>';
                    pdfHtml += '</a>';
                    pdfHtml += '<div class="icon">';
                        pdfHtml += '<i class="icofont icofont-video"></i>';
                    pdfHtml += '</div>';
                    pdfHtml += '<span style="display: inline-block;width: 75px;">'+input.files[0].name+'</span>';
                pdfHtml += '</div>';
            pdfHtml += '</li>';
            $('#video_file_show').append(pdfHtml);

            var prev_file_count = video_file_count;
            $('.video_file_'+video_file_count).css('display','none');
            video_file_count++;
            var video_input_file = '<input name="videofile_'+video_file_count+'" id="video_file_'+video_file_count+'" type="file" class="custom-file-input js_video_file  video_file_'+video_file_count+'" onchange="addVideoFile(this)" accept="video/*"/>';
            $('.video_file_'+prev_file_count).after(video_input_file);
            $('#video_uploaded_file_count').val(video_file_count);
        }
    }
}

function removeVideoFile(file_count){
    var video_file_input = document.getElementById('video_file_'+file_count);
    video_file_input.remove();

    var li_display_file = document.getElementById('display_video_file_'+file_count);
    li_display_file.remove();
}



function addSafetyDatasheetFile(input){
    if (input.files && input.files[0]) {
        var safety_datasheet_file_count = $('#safety_datasheet_uploaded_file_count').val();
        if(input.files[0].size > 2000000){
            swal("Error!", "Please select file less then 2Mb!", "error", {
                button: "Ok!",
            });
        }else if( input.files[0].type != 'application/pdf'){
            swal("Error!", "Please select pdf file!", "error", {
                button: "Ok!",
            });
        }else{
            var pdfHtml = "";
            pdfHtml += '<li id="display_safety_datasheet_file_'+safety_datasheet_file_count+'">';
                pdfHtml += '<div class="box">';
                    pdfHtml += '<a href="javascript:void(0);" class="remove1" onclick="removeSafetyDatasheetFile('+safety_datasheet_file_count+')">';
                        pdfHtml += '<i class="icofont icofont-close"></i>';
                    pdfHtml += '</a>';
                    pdfHtml += '<div class="icon">';
                        pdfHtml += '<i class="icofont icofont-file-pdf"></i>';
                    pdfHtml += '</div>';
                    pdfHtml += '<span style="display: inline-block;width: 75px;">'+input.files[0].name+'</span>';
                pdfHtml += '</div>';
            pdfHtml += '</li>';
            $('#safetydatasheet_file_pdf_show').append(pdfHtml);

            var prev_file_count = safety_datasheet_file_count;
            $('.safety_datasheet_file_'+safety_datasheet_file_count).css('display','none');
            safety_datasheet_file_count++;
            var safety_datasheet_input_file = '<input name="safety_datasheet_file_'+safety_datasheet_file_count+'" id="safety_datasheet_file_'+safety_datasheet_file_count+'" type="file" class="custom-file-input js_safety_datasheet_file  safety_datasheet_file_'+safety_datasheet_file_count+'" onchange="addSafetyDatasheetFile(this)" accept=".pdf"/>';
            $('.safety_datasheet_file_'+prev_file_count).after(safety_datasheet_input_file);
            $('#safety_datasheet_uploaded_file_count').val(safety_datasheet_file_count);
        }
    }
}

function removeSafetyDatasheetFile(file_count){
    var safety_datasheet_file_input = document.getElementById('safety_datasheet_file_'+file_count);
    safety_datasheet_file_input.remove();

    var li_display_file = document.getElementById('display_safety_datasheet_file_'+file_count);
    li_display_file.remove();
}



// var extensionIcon = '';
//     if(extension == 'pdf'){
//         extensionIcon = `<i class="icofont icofont-file-pdf"></i>`
//     } else {
//         extensionIcon = `<i class="icofont icofont-ui-image"></i>`
//     }



function addcertificateFile(input){

    if (input.files && input.files[0]) {
        var certificate_file_count = $('#certificate_file_count').val();
        console.log(input.files[0].type)
        if(input.files[0].size > 2000000){
            swal("Error!", "Please select file less then 2Mb!", "error", {
                button: "Ok!",
            });
        }else if( input.files[0].type != 'image/jpeg' && input.files[0].type != 'image/png' && input.files[0].type != 'image/jpg' && input.files[0].type != 'application/pdf'){
            swal("Error!", "Please select pdf file !", "error", {
                    button: "Ok!",
                });
        }else{
            var pdfHtml = "";
            pdfHtml += '<li id="display_certificate_file_'+certificate_file_count+'">';
                pdfHtml += '<div class="box">';
                    pdfHtml += '<a href="javascript:void(0);" class="remove1" onclick="removeCertificateFile('+certificate_file_count+')">';
                        pdfHtml += '<i class="icofont icofont-close"></i>';
                    pdfHtml += '</a>';
                    pdfHtml += '<div class="icon">';
                    if(input.files[0].type != 'image/jpeg' && input.files[0].type != 'image/png' && input.files[0].type != 'image/jpg')
                        pdfHtml += '<i class="icofont icofont-file-pdf"></i>';
                     else{
                        pdfHtml += '<i class="icofont icofont-ui-image"></i>';
                     }
                    pdfHtml += '</div>';
                    pdfHtml += '<span style="display: inline-block;width: 75px;">'+input.files[0].name+'</span>';
                pdfHtml += '</div>';
            pdfHtml += '</li>';
            $('#certificate_file_show').append(pdfHtml);

            var prev_file_count = certificate_file_count;
            $('.certificate_file_'+certificate_file_count).css('display','none');
            certificate_file_count++;
            var certificate_input_file = '<input name="certificate_file_'+certificate_file_count+'" id="certificate_file_'+certificate_file_count+'" type="file" class="custom-file-input js_certificate_file  certificate_file_'+certificate_file_count+'" onchange="addcertificateFile(this)" accept=".pdf,image/*"/>';
            $('.certificate_file_'+prev_file_count).after(certificate_input_file);
            $('#certificate_file_count').val(certificate_file_count);
        }

    }
}

function removeCertificateFile(file_count){
    var certificate_input_file = document.getElementById('certificate_file_'+file_count);
    certificate_input_file.remove();

    var li_display_file = document.getElementById('display_certificate_file_'+file_count);
    li_display_file.remove();
}

// Remove tech file selected

function removeTEchFile(ele,id,product_id){
    url = $(ele).attr('data-tech-url')
    var csrf = $( "input[name$='csrfmiddlewaretoken']" ).val();
    $.ajax({
          url: url,
          type:"POST",
          data:{
            'tech_file_id':id,
            'csrfmiddlewaretoken':csrf,
            'product_id':product_id,
          },
          success: function(data){
            $(".techFileSelectd_"+id).fadeOut();

          }
      });
    }


function removeGuideFile(ele,id,product_id){
    url = $(ele).attr('data-guide-url')
    var csrf = $( "input[name$='csrfmiddlewaretoken']" ).val();
    $.ajax({
          url: url,
          type:"POST",
          data:{
            'guide_file_id':id,
            'csrfmiddlewaretoken':csrf,
            'product_id':product_id,
          },
          success: function(data){
            $(".Guide_file_selected_"+id).fadeOut();

          }
      });
    }


function removeSelectVideoFile(ele,id,product_id){
    url = $(ele).attr('data-video-url')
    var csrf = $( "input[name$='csrfmiddlewaretoken']" ).val();
    $.ajax({
          url: url,
          type:"POST",
          data:{
            'video_file_id':id,
            'csrfmiddlewaretoken':csrf,
            'product_id':product_id,
          },
          success: function(data){
            $(".Video_file_Selected_"+id).fadeOut();
          }
      });
    }

function removeSafetyFile(ele,id,product_id){
url = $(ele).attr('data-safety-url')
var csrf = $( "input[name$='csrfmiddlewaretoken']" ).val();
$.ajax({
      url: url,
      type:"POST",
      data:{
        'safety_file_id':id,
        'csrfmiddlewaretoken':csrf,
        'product_id':product_id,
      },
      success: function(data){
        $(".safety_file_selected_"+id).fadeOut();
      }
  });
}

function removeCertificateFileSelected(ele,id,product_id){
url = $(ele).attr('data-certificate-url')
var csrf = $( "input[name$='csrfmiddlewaretoken']" ).val();
$.ajax({
      url: url,
      type:"POST",
      data:{
        'certificate_file_id':id,
        'csrfmiddlewaretoken':csrf,
        'product_id':product_id,
      },
      success: function(data){
        $(".certificate_file_selected_"+id).fadeOut();
      }
  });
}


function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('.show_p_add_image').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$(".P_add_image").change(function(){
    readURL(this);
});
