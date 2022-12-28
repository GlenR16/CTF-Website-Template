const timer = document.getElementById("timer")
if (timer)
{
  var countDownDate = new Date("Jan 5, 2023 15:37:25").getTime();
  var timerSetter = setInterval(function() {
    var distance = countDownDate - new Date().getTime();
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    document.getElementById("timer").innerHTML = "Event Begins in "+ days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
    if (distance < 0) 
    {
      clearInterval(x);
      document.getElementById("timer").innerHTML = "CTF has begun. <br> Please Reload the website.";
    }
  }, 1000);
}
function verifyPassword(password) {  
  if (password.length < 8)
  {  
    document.getElementById("password").style.borderColor = "#ff0000"; 
  }
  else
  {
    document.getElementById("password").style.borderColor = "#1aff00"; 
  }
}

function tableSearch() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("table_search");
  filter = input.value.toUpperCase();
  table = document.getElementById("team_table");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}