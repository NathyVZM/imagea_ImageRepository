//input_file.js

let file = document.getElementById('file')
let add = document.getElementById('add')

if(file && add){
    const showFile = (e) => {
        console.log(file.files[0].name)
        let label = document.querySelector('.inputbox label')
        if(file.files[0].size > 3145728){
            label.innerHTML = 'File is too big'
            file.value = ''
        }
        else {
            label.innerHTML = file.files[0].name
        }
    }
    
    file.onchange = showFile

    const sendFile = (e) => {
        console.log(e.target.id)

        if(file.value == ''){
            let label = document.querySelector('.inputbox label')
            label.innerHTML = 'Choose a file'
        }
    }

    add.onclick = sendFile
}