$("#search").keypress(function (e) { 
        
    if (e.keyCode == 13){
        
        if($("#search").val())            
            $.ajax({                       
                url: ajax_search_url,                   
                
                data: {
                    'search_input': $("#search").val()     
                },
                
                success: function (data) {   
                    $("#searchResult").html(data); 
                }
            });
    }
});