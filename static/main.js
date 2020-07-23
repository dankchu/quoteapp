$( document ).ready(function(){
  setInterval(getQuote, 10000)

  function getQuote(){
    $.getJSON( "newquote", function( data ) {
      var quote = data.quote;
      var source  = data.source;
      $("#quote-container").text(quote);
      $("#source-container").text(source);
    });
  }//function getQuote

  $("#edit-button").click(function(){
    if ( $( "#edit-window" ).length == 0) {
      var jqxhr = $.get( "/edit")
      .done(function(data) {
        $( "body" ).append(data);
      })
      .fail(function() {
        alert( "error" );
      })
      //load from /Edit
    }//don't create new window if already created

  });//#edit-button click

  //Event delegation???? https://stackoverflow.com/questions/16598213/how-to-bind-events-on-ajax-loaded-content
  $(document).on("click", '#edit-window-button-close', function(event) {
    $("#edit-window").remove();
  });

  $(document).on("click", "#edit-submit-button", function(event){
    var quote = $("#submit-quote").val();
    var attr = $("#submit-attr").val();
    var data = {q: quote, a: attr};

    $.post( "/submitquote", JSON.stringify(data))
      .done(function(data) {
        $("#submit-attr").val("Attributed");
        $("#submit-quote").val("New quotation...");
        if ( $( "#edit-window-edit-container" ).length > 0) {
          var jqxhr = $.get( "/editrefresh")
          .done(function(data) {
            $( "#edit-window-edit-container" ).html(data);
          })
          .fail(function() {
            alert( "error" );
          })
          //load from /Edit
        }//don't create new window if already created
      })
      .fail(function(){
        console.log("Quote submission failed");
      });
  });

  $(document).on("click", '#edit-quote-delete', function(event) {
    var container = $(this).parent().parent();
    var qid = container.attr("qid")
    //1. remove from database.
    var data = {qid:qid};

    //as written, this will remove the quote from the edit window regardless of whether or not the delete actually succeeded?
    $.post( "/deletequote", JSON.stringify(data)).done(function(data) {
      $( ".result" ).html( data );
      $(container).remove();
    });
  });





  getQuote();

});
