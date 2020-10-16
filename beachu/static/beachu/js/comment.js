function show_edit_post(element_this) {
    const id = element_this.id;    
    document.querySelector('#post' + id).style.display = 'none';
    document.querySelector('#edit' + id).style.display = 'block';      
    document.querySelector('#textedit' + id).value = document.querySelector('#post_body' + id).innerHTML;
    document.querySelector('#edit' + id + ' > .btn-success').addEventListener('click', () => edit_post(id));           
    document.querySelector('#edit' + id + ' > .btn-secondary').addEventListener('click', () => cancel_edit_post(id));           
  }

function addcomment(id, user) {
    const post_id = parseInt(id);
    const post_body = document.querySelector('#textpost').value;
    fetch('/addcomment', {
        method: 'POST',
        body: JSON.stringify({
              estab_id: post_id,
              textpost: post_body
        })
    })
    .then(response => {  
        if (response.ok) {
            newpost(post_id, post_body, user);
            const postbtn = document.querySelector('#postbtn');
            postbtn.disabled = true;
            postbtn.innerHTML = 'Thanks for your comment';  
        }           
    });
}


function newpost(post_id, post_body, post_user) {
    const bigbox = document.querySelector('#lastpost');
    const newline = document.createElement("BR");

    const title = document.createElement('p');
    title.style.fontWeight = 'bold';
    title.innerHTML = post_user;
    bigbox.appendChild(title);

    const firstdiv = document.createElement('div');
    firstdiv.id = 'post' + post_id;
    bigbox.appendChild(firstdiv);

    const editbtn = document.createElement('div');
    editbtn.id = post_id;
    editbtn.className = 'base editlink';
    editbtn.onclick = function() { show_edit_post(this); }
    editbtn.innerHTML = 'Edit';
    firstdiv.appendChild(editbtn);    

    editbtn.insertAdjacentElement("afterend", newline);

    const smallbody = document.createElement('small');
    smallbody.id = 'post_body' + post_id;
    smallbody.innerHTML = post_body;
    firstdiv.appendChild(smallbody);    

    const seconddiv = document.createElement('div'); 
    seconddiv.id = 'edit' + post_id;
    seconddiv.style.display = 'none';
    bigbox.appendChild(seconddiv);

    seconddiv.insertAdjacentElement("afterend", newline);

    const textdiv = document.createElement('div');
    textdiv.className = 'form-group';
    seconddiv.appendChild(textdiv);

    const inputfield = document.createElement('input');
    inputfield.type = 'text';
    inputfield.className = 'form-control';
    inputfield.id = 'textedit' + post_id;
    textdiv.appendChild(inputfield);

    const savebtn = document.createElement('button');
    savebtn.className = "btn btn-success";
    savebtn.innerHTML = 'Save';
    seconddiv.appendChild(savebtn);

    const cancelbtn = document.createElement('button');
    cancelbtn.className = 'btn btn-secondary';
    cancelbtn.innerHTML = 'Cancel';
    seconddiv.appendChild(cancelbtn);

    const postdate = document.createElement('small');
    postdate.style.color = 'gray;';
    postdate.innerHTML = 'Just now';
    bigbox.appendChild(postdate);

    bigbox.style.display = 'block';
}

function cancel_edit_post(id) {
    document.querySelector('#post' + id).style.display = 'block';
    document.querySelector('#edit' + id).style.display = 'none';
  }
  
function edit_post(id) {
    const new_content = document.querySelector('#textedit' + id).value;
    fetch('/editcomment', {
      method: 'PUT',
      body: JSON.stringify({
          post_id: id,
          post_body: new_content
      })
    })
    .then(response => {
      if (response.ok) {
        document.querySelector('#post' + id).style.display = 'block';
        document.querySelector('#edit' + id).style.display = 'none';  
        document.querySelector('#post_body' + id).innerHTML = new_content;
      }
      else { cancel_edit_post(id); }
    });  
  }