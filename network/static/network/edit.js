function show_edit_post(element_this) {
  const id = element_this.id;    
  document.querySelector('#post' + id).style.display = 'none';
  document.querySelector('#edit' + id).style.display = 'block';      
  document.querySelector('#textedit' + id).value = document.querySelector('#post_body' + id).innerHTML;
  document.querySelector('#edit' + id + ' > .btn-success').addEventListener('click', () => edit_post(id));           
  document.querySelector('#edit' + id + ' > .btn-secondary').addEventListener('click', () => cancel_edit_post(id));           
}

function cancel_edit_post(id) {
  document.querySelector('#post' + id).style.display = 'block';
  document.querySelector('#edit' + id).style.display = 'none';
}

function edit_post(id) {
  const new_content = document.querySelector('#textedit' + id).value;
  fetch('edit', {
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
  });  
}

function add_like(id) {
  const likes = document.querySelector('#like' + id);
  const heart = document.querySelector('#heart' + id);
  fetch('addlike', {
    method: 'POST',
    body: JSON.stringify({
        post_id: id
    })
  })
  .then(response => { 
    if (response.ok) {
      heart.setAttribute('onclick', "rem_like("+ id +")");
      likes.innerHTML = parseInt(likes.innerHTML) + 1;
    }
  })
}

function rem_like(id) {
  const likes = document.querySelector('#like' + id);
  const heart = document.querySelector('#heart' + id);
  fetch('remlike', {
    method: 'DELETE',
    body: JSON.stringify({
        post_id: id
    })
  })
  .then(response => {
    if (response.ok) {
      heart.setAttribute('onclick', "add_like("+ id +")");
      likes.innerHTML = parseInt(likes.innerHTML) - 1;
    }
  });  
}

