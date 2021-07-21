// create_rep.js

let createButton = document.getElementById('create-button')

const sendForm = (e) => {
    console.log(e.target.id)
}

createButton.onclick = sendForm