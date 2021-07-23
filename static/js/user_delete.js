//user_delete.js

let user_delete = document.getElementById('delete')

if(user_delete) {
    const user_delete_action = (e) => {
        console.log(e.target.id)
        let username = document.getElementById('username')
        console.log(username.value)

        data = {'username': username.value}

        fetch('/user/delete', {
            method: 'DELETE'
        }).then(response => {
            return response.json()
        }).then(data => {
            console.log(data)

            if(data.status == 200) {
                window.location.href = '/logout'
            }
        })
    }

    user_delete.onclick = user_delete_action
}