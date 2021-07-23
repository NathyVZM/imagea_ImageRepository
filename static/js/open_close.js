//open_close.js

let create_rep = document.getElementById('create-rep')
let create_rep_form = document.getElementById('create-rep-form')

let add_image = document.getElementById('add-image')
let add_image_form = document.getElementById('add-image-form')

let arrow = document.getElementById('arrow')
let panel = document.getElementById('panel')

let close = document.getElementsByClassName('close')

if (create_rep && create_rep_form) {
    const open_rep = (e) => {
        console.log(e.target.id)
        create_rep_form.style.display = 'flex'
    }
    create_rep.onclick = open_rep
}

if (add_image && add_image_form){
    const open_image = (e) => {
        console.log(e.target.id)
        add_image_form.style.display = 'flex'
    }
    add_image.onclick = open_image
}


const open_panel = (e) => {
    console.log(e.target.id)
    panel.style.display = 'flex'
}

arrow.onclick = open_panel


if ((create_rep && create_rep_form) || (add_image && add_image_form) || (arrow && panel)){
    const close_form = (e) => {
        console.log(e.target.id)

        if((create_rep && create_rep_form) && !((add_image && add_image_form) || (arrow && panel))){
            create_rep_form.style.display = 'none'
        }
        else if((add_image && add_image_form) && !((create_rep && create_rep_form) || (arrow && panel))) {
            add_image_form.style.display = 'none'
        }
        else if ((arrow && panel) && !((create_rep && create_rep_form) || (add_image && add_image_form))) {
            panel.style.display = 'none'
        }
        else {
            create_rep_form.style.display = 'none'
            add_image_form.style.display = 'none'
            panel.style.display = 'none'
        }
    }

    for (let i = 0; i < close.length; i++) {
        close[i].onclick = close_form
    }
}