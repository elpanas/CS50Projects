function change_follow(id) {
    const foll_btn = document.querySelector('#foll' + id);
    const followers = document.querySelector('#followers');

    if (foll_btn.innerHTML == 'Unfollow') {        
        fetch('unfollow', {
            method: 'DELETE',
            body: JSON.stringify({
                user_id: id
            })
        })
        .then(response => {
            if (response.ok) { 
                foll_btn.innerHTML = 'Follow'; 
                followers.innerHTML = parseInt(followers.innerHTML) - 1;
            }
        });           
    }
    else {
        fetch('follow', {
            method: 'POST',
            body: JSON.stringify({
                user_id: id
            })
        })
        .then(response => {
            if (response.ok) { 
                foll_btn.innerHTML = 'Unfollow';
                followers.innerHTML = parseInt(followers.innerHTML) + 1;
            }
        });
    }
}