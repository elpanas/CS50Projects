document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views  
    const bookimg = document.querySelector('#bookimg');
    if (bookimg) { bookimg.addEventListener('click', () => change_book()); }
  });


// Update image and text of the DOM element
function change_book() {
  if (document.querySelector('#booktext').innerHTML === "Book your place now!") {
    addbook();
  } else {  
    rembook();
  }     
}


// Add favourite to the db
function addbook() {
  const nrumb = document.querySelector('#nrumb');
  const bookumb = document.querySelector('#bookumb');
  if (parseInt(nrumb.value) > 0) {
    fetch('/addbook', {
      method: 'POST',
      body: JSON.stringify({
          estab_id: parseInt(document.querySelector('#estabid').value),
          nrumb: parseInt(document.querySelector('#nrumb').value)
      })
    })
    .then(response => {
      if (response.ok) {
        document.querySelector('#bookimg').src = '/static/beachu/images/calendar-check-fill.svg';
        document.querySelector('#booktext').innerHTML = 'Remove booking';       
        nrumb.style.display = 'none';
        bookumb.innerHTML = nrumb.value;
        bookumb.style.display = 'block';        
      }
    });
  }  
  return false;
}


// Remove favourite from the db
function rembook() {
  fetch('/rembook', {
    method: 'DELETE',
    body: JSON.stringify({
        estab_id: parseInt(document.querySelector('#estabid').value)
    })
  })
  .then(response => {
    if (response.ok) {
      document.querySelector('#bookimg').src = '/static/beachu/images/calendar-check.svg';
      document.querySelector('#booktext').innerHTML = 'Book your place now!';
      document.querySelector('#bookumb').style.display = 'none';
      const nrumb = document.querySelector('#nrumb');
      nrumb.style.display = 'block';
      nrumb.value = "";
    }
  });
  return false;
}