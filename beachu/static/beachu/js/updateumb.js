// Increase the number of available umbrellas
function increaseUmb(id) {
    fetch('/incumb', {
        method: 'PUT',
        body: JSON.stringify({
            estab_id: parseInt(id)
        })
    })
    .then(response => {
        if (response.ok) {
            const availumb = document.querySelector('#availumb');
            availumb.innerHTML = parseInt(availumb.innerHTML) + 1;
            const nrumb = document.querySelector('#nrumb');
            if (nrumb) { nrumb.max = parseInt(nrumb.max) + 1; }
        }
        else if (response.status === 401) {            
                const incumb = document.querySelector('#incumb');
                incumb.onclick = null;
                const decumb = document.querySelector('#decumb');
                decumb.onclick = () => { decreaseUmb(id); }
        }        
    });
    return false;
}


// Increase the number of available umbrellas
function decreaseUmb(id) {
    fetch('/decumb', {
        method: 'PUT',
        body: JSON.stringify({
            estab_id: parseInt(id)
        })
    })
    .then(response => {
        if (response.ok) {
            const availumb = document.querySelector('#availumb');
            availumb.innerHTML = parseInt(availumb.innerHTML) - 1;
            const nrumb = document.querySelector('#nrumb');
            if (nrumb) { nrumb.max = parseInt(nrumb.max) - 1; }
        }
        else if (response.status === 401) {            
            const incumb = document.querySelector('#incumb');
            incumb.onclick = () => { increaseUmb(id); }
            const decumb = document.querySelector('#decumb');
            decumb.onclick = null;
        }  
    });
    return false;
}