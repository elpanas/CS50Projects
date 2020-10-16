document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views  
    const fav = document.querySelector('#fav');
    if (fav) { fav.addEventListener('click', () => change_fav()); }
  });


// Update image and text of the DOM element
function change_fav() {
  if (document.querySelector('#favtext').innerHTML === "Add to favourites!") {
    addfav();
  } else {  
    remfav()
  }      
}


// Add favourite to the db
function addfav() {
  fetch('/addfav', {
    method: 'POST',
    body: JSON.stringify({
        estab_id: parseInt(document.querySelector('#estabid').value)
    })
  })
  .then((response) => {
    if (response.ok) {
      document.querySelector('#favimg').src = '/static/beachu/images/suit-heart-fill.svg';
      document.querySelector('#favtext').innerHTML = 'Remove from favourites';
    }
  })
  .catch(() => {
    return false;
  });
}


// Remove favourite from the db
function remfav() {
  fetch('/remfav', {
    method: 'DELETE',
    body: JSON.stringify({
        estab_id: parseInt(document.querySelector('#estabid').value)
    })
  })
  .then(response => {
    if (response.ok) {
      document.querySelector('#favimg').src = '/static/beachu/images/suit-heart.svg';
      document.querySelector('#favtext').innerHTML = 'Add to favourites!';
    }
  })
  .catch(() => {
    return false;
  });
}