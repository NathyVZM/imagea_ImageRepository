//input_file.js

let file = document.getElementById('file')

if(file){
    const showFile = (e) => {
        console.log(file.files[0].name)
        let label = document.querySelector('.inputbox label')
        label.innerHTML = file.files[0].name
    }
    
    file.onchange = showFile
}