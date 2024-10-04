document.addEventListener('DOMContentLoaded', function() {

    // select the reply button
    document.querySelectorAll('#edit').forEach(button => {
        button.addEventListener('click', function(event) {
            edit_function(event, button)
        })
    })

    // submit the edited post
    document.querySelector('#edit-form').addEventListener('submit', submit_function)

    // select the toggle like buttons
    let buttons = document.querySelectorAll('.like-btn, .unlike-btn')

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            togglelike(button);
        })
    })

});

function load_posts() {
    document.querySelector('#edit-form').style.display = 'none';
    document.querySelector('#edit').style.display = 'block';
}

function edit_function(event, button) {
    event.preventDefault()
 

    const editForm = button.previousElementSibling;

    editForm.style.display = 'block';
    button.style.display = 'none';

    
}

function submit_function() {
    
    console.log("submit2")

    id = document.querySelector('#post-id').value;
    text = document.querySelector('#compose-text').value;

    fetch('/edit', {
        method: 'POST',
        body: JSON.stringify({
            id: id,
            text: text
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        if (result.message) {
            // Reload the page to reflect changes
            location.reload();
        } else if (result.error) {
            alert(result.error);
        }
    })
    .catch(error => console.log('Error:', error));
}



// togglelike function

function togglelike(button) {
    let isLiked = button.getAttribute('data-liked') === 'true';
    const id = button.id;
    
    if (isLiked) {
        fetch(`/unlike/${id}`)
        .then(response => response.json())
        .then(result => {
            if (result.message) {
                button.className = "btn fa fa-thumbs-down unlike-btn";
                button.style.color = "red";
                button.setAttribute('data-liked', 'false');

                const likeCount = document.getElementById(`like-count-${id}`);
                likeCount.innerHTML = `❤️ ${result.likes}`; 
            }
        })
        .catch(error => console.log('Error:', error));
        
    } else {
        fetch(`/like/${id}`)
        .then(response => response.json())
        .then(result => {
            if (result.message) {
                button.className = "btn fa fa-thumbs-up like-btn";
                button.style.color = "green";
                button.setAttribute('data-liked', 'true');
                
                const likeCount = document.getElementById(`like-count-${id}`);
                likeCount.innerHTML = `❤️ ${result.likes}`;
            }
        })
        .catch(error => console.log('Error:', error));
    }
}
