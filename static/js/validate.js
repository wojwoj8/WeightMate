function validateForm() {
  const usern = document.forms.registerform.username.value;
  const passw = document.forms.registerform.password.value;
  const log = !!document.getElementById('confirmation');
  if (log == true) {
    var confirm = document.forms.registerform.confirmation.value;
  }
  if (usern == null || usern == '') {
    document.getElementsByClassName('error')[0].style.visibility = 'visible';
    document.getElementsByClassName('authstyle')[0].style.border = '2px solid red';
    document.getElementsByClassName('error')[0].innerHTML = 'Please Fill out all fields';
    return false;
  }
  if (passw == null || passw == '') {
    document.getElementsByClassName('error')[0].style.visibility = 'visible';
    document.getElementsByClassName('authstyle')[1].style.border = '2px solid red';
    document.getElementsByClassName('error')[0].innerHTML = 'Please Fill out password';
    return false;
  }
  if (log == true) {
    if (confirm != passw) {
      document.getElementsByClassName('error')[0].style.visibility = 'visible';
      document.getElementsByClassName('authstyle')[2].style.border = '2px solid red';
      document.getElementsByClassName('error')[0].innerHTML = 'passwords must be the same';
      return false;
    }
  } else {
    return true;
  }
}
