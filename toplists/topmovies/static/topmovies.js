function addMovie(id) {
    jsonObj = {movie_id : id}
    
    $.post("/topmovies/add-movie/", jsonObj, function(data) {
        if (data.success)
        {
            alert("Movie added!")
        }
        else{
            alert("Movie is already in your list.")
        }
    });
}

function deleteMovie(id) {
    jsonObj = {movie_id : id}
    $.post("/topmovies/delete-movie/", jsonObj, function(data) {
        if (data.success)
        {
            var myobj = document.getElementById(id);
            myobj.remove()
        }
        else{
            alert("Error deleting movie.")
        }
    });
}

function increment() {
    var urlParams = new URLSearchParams(window.location.search);
    var newPage = parseInt(urlParams.get('page')) + 1
    urlParams.set("page", newPage)
    window.location.search = urlParams.toString();
}

function decrement() {
    var urlParams = new URLSearchParams(window.location.search);
    page = parseInt(urlParams.get('page'))
    if (page > 1){
      var newPage = page - 1
      urlParams.set("page", newPage)
    }
    window.location.search = urlParams.toString();
}

$(function(){
    $('#response').submit(function() {
      $.post($(this).attr('action'), $(this).serialize(), function(json) {
          if (json.success && json.purpose != 'Update') {
            window.location.href = json.redirect;
          }
          else {
              if (json.purpose == 'Log in') {
                alert("Wrong username or password, please try again.")
              }
              else if (json.purpose =='Sign up') {
                  if (json.reason == 'invalid') {
                    alert("Please choose a valid email")
                  }
                  else {
                    alert(json.reason + " is already taken.")
                  }
              }
              else {
                  if (json.reason == 'email')
                  {
                    alert(json.reason + " is already taken.")
                  }
                  else {
                    alert("Your information has been updated.")
                  }
              }
          }
      });
      return false;
    });
  });