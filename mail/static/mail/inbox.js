document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views  
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#submitmail').addEventListener('click', send_mail);
  
  // By default, load the inbox
  load_mailbox('inbox'); 
});


// show and fill the template to create an email
function compose_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  activate_button('compose');

  var recip = document.querySelector('#compose-recipients');
  var subject = document.querySelector('#compose-subject');
  var body = document.querySelector('#compose-body');

  recip.value = '';
  subject.value = '';
  body.value = '';

  // Reply
  if (email.id > 0) {
    if (email.subject.substring(0, 2) === 'Re:') {
      subject.value = email.subject;
    }
    else {
      subject.value = 'Re: ' + email.subject;
    }
    // Clear out composition fields
    recip.value = email.sender;
    body.value = 'On ' + email.timestamp + ' ' + email.sender + ' wrote:\n\n' + email.body;
  }
}


function load_mailbox(mailbox) {

  var choise_array = ['inbox', 'sent', 'archive'];

  if (mailbox === 'archive') {
    activate_button('archived');
  } else {
    activate_button(mailbox);
  }
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  if (choise_array.includes(mailbox)) {
    show_mail_list(mailbox);
  } 
}


// show and fill the form to create and send email
function send_mail() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then((result) => {
    console.log(result);    
  });

  load_mailbox('sent');
}


// show a list of the emails
function show_mail_list(mailbox) {
  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      var i = 0;
      // create a row for each email
      emails.forEach((email) => {
        i++;      
        const element_row = document.createElement('div');
        if (email.read) {
          element_row.className = 'row customrow';
        } else {
          element_row.className = 'row customrow read';
        }
        
        element_row.id = 'r' + i;   
        document.querySelector('#emails-view').append(element_row);         
        // create a column for each field
        for (var j = 1; j < 4; j++) {
          const element_col = document.createElement('div');
          element_col.className = 'col-sm';
          element_col.id = 'c' + j;    
          
          switch (j) {
            case 1:
              element_col.innerHTML = '<strong>' + email.sender + '</strong>';
              break;

            case 2:   
              element_col.className = 'col-7';           
              element_col.innerHTML = email.subject;
              break;

            case 3:              
              element_col.innerHTML = email.timestamp;
              break;
          }          
          document.querySelector('#r' + i).append(element_col);
        } 
        element_row.addEventListener('click', () => show_mail(email.id));
        var reply = document.querySelector('#reply');
        var archive = document.querySelector('#archive');
        if (mailbox === 'sent') {
          reply.style.display = 'none';
          archive.style.display = 'none';
        } else {
          reply.style.display = 'block';
          archive.style.display = 'block';
        }       
      }); 
  });  
}

// show 1 email
function show_mail(email_id) {
  fetch('/emails/' + email_id)
  .then(response => response.json())
  .then(email => {  
      // Hide other views
      document.querySelector('#email-view').style.display = 'block';
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';   
       
      // Print email
      document.querySelector('#from').innerHTML = '<strong>From: </strong>' + email.sender;
      document.querySelector('#to').innerHTML = '<strong>To: </strong>' + email.recipients;
      document.querySelector('#subject').innerHTML = '<strong>Subject: </strong>' + email.subject;
      document.querySelector('#timestamp').innerHTML = '<strong>Timestamp: </strong>' + email.timestamp;

      // add the body content
      document.querySelector('#email-body').innerHTML = email.body; 
      
      document.querySelector('#reply').addEventListener('click', () => compose_email(email));
      document.querySelector('#archive').addEventListener('click', () => archive_email(email.id,email.archived));
      change_archive(email.id,email.archived);

      if (email.archived === false) {
        fetch('/emails/' + email_id, {
          method: 'PUT',
          body: JSON.stringify({
              read: true,
              archived: true
          })
        });
        change_archive(email.id,true);
      }   
  });  
}


// archive mail
function archive_email(email_id, arch) {
  fetch('/emails/' + email_id, {
    method: 'PUT',
    body: JSON.stringify({
        archived: arch
    })
  });

  change_archive(arch);  
}


function activate_button(clicked_button_id) {

  var button_array = ['inbox', 'compose', 'sent', 'archived'];

  button_array.forEach((id) => {

    var element_button = document.querySelector('#' + id);
    
    if (id === clicked_button_id) {
      element_button.className = 'btn btn-sm btn-primary';
    } else {
      element_button.className = 'btn btn-sm btn-outline-primary';
    }
  })
}

// support function: change the text of the button
function change_archive(email_id,arch) {  
  var archive = document.querySelector('#archive');
  archive.addEventListener('click', () => archive_email(email_id,!arch));

  if (arch === true) {
    archive.innerHTML = 'Unarchive';    
  }  
  else {
    archive.innerHTML = 'Archive';
  }
}