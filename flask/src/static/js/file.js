window.addEventListener('load', function() {
    console.log(short_link);
    fetch(`/api/v1/file/${short_link}`)
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw response.json();
        }
    })
    .then(data => {
        console.log(data);
        document.getElementById('file').innerHTML = JSON.stringify(data);
    })
    .catch(err => {
        console.error(err);
    })
})