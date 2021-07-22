//open_close.js

let create_rep = document.getElementById('create-rep')
let create_rep_form = document.getElementById('create-rep-form')

let add_image = document.getElementById('add-image')
let add_image_form = document.getElementById('add-image-form')

let close = document.getElementsByClassName('close')


const open_rep = (e) => {
    console.log(e.target.id)
    create_rep_form.style.display = 'flex'
}

const open_image = (e) => {
    console.log(e.target.id)
    add_image_form.style.display = 'flex'
}

const close_form = (e) => {
    console.log(e.target.id)
    create_rep_form.style.display = 'none'
    add_image_form.style.display = 'none'
}

create_rep.onclick = open_rep
add_image.onclick = open_image

for(let i = 0; i < close.length; i++){
    close[i].onclick = close_form
}