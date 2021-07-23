//view_rep.js

let update = document.getElementById('update')

if (update) {
    const update_user = (e) => {
        console.log(e.target.id)

        let userForm = document.getElementById('userForm')
        let form = new FormData(userForm)

        for (const value of form.values()) {
            console.log(value)
        }

        fetch('/user/edit', {
            method: 'PUT',
            body: form
        }).then(response => {
            return response.json()
        }).then(data => {
            console.log(data)

            // if(data.status == 200){
            //     window.location.href = '/repository'
            // }
        })
    }

    update.onclick = update_user
}