//open_close.js

let create_rep = document.getElementById('create-rep')
let create_rep_form = document.getElementById('create-rep-form')
let close = document.getElementById('close')


const open_form = (e) => {
    console.log(e.target.id)
    create_rep_form.style.display = 'flex'
}

const close_form = (e) => {
    console.log(e.target.id)
    create_rep_form.style.display = 'none'
}

create_rep.onclick = open_form
close.onclick = close_form