console.log("logout js")

// $(document).ready(function(){
//     console.log("ready logot js")
    $('#logout').click(function(){
        console.log("in id logout function")
        url = $(this).attr('data-url')
        console.log("url--",url)

        $.ajax({        
            method: "POST",
            url: url,
            data:{
                'device':'website'
            },
            success: function(data){
                console.log("success")
                window.location.href = "/login/";
            },
            error: function(error_data){
                console.log("error")
                console.log(error_data)
            }
        })
    })
// })


// function adminLogout(){
//     console.log('cn----')
//     url = $('.logot1').attr('data-url')
//     console.log("url--",url)

//     $.ajax({        
//         method: "POST",
//         url: url,
//         data:{
//             'device':'website'
//         },
//         success: function(data){
//             console.log("success")
//             window.location.href = "/login/";
//         },
//         error: function(error_data){
//             console.log("error")
//             console.log(error_data)
//         }
//     })
// }

function adminLogout(){
    console.log('cn----')
    url = $('.logot1').attr('data-url')
    console.log("url--",url)
    
    $.ajax({
    method: "POST",
    url: url,
    data:{
    'device':'website'
    },
    success: function(data){
    console.log("success", data)
    if (data == 'logout'){
    window.location.href = "/login/";
    }
    else{
    alert(data);
    }
    
    },
    error: function(error_data){
    console.log("error")
    console.log(error_data)
    }
    })
    }