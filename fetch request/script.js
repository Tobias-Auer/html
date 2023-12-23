fetch("https://reqres.in/api/users/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        name: "User 1"
    })
}).then(res => {
    return res.json()})
.then(data => {
    console.log(data)
    console.log(data["name"])
})
.catch(error => console.log("ERROR"))
