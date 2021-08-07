let recipesDiv = document.getElementById('rlist');
let addButton = document.getElementById('addbutton');

addButton.onclick = () => {
    let name = prompt("enter name:");
    if (typeof name === "string") {
        if (name.length <= 64 && name.length !== 0) {
            addRecipe(name);
        } else {
            alert("Name too long");
        }
    } else {
        alert("Invalid name");
    }
};

function setRecipeDate() {
    data = new FormData()
    data.append("name", this.parentElement.dataset.rname);
    data.append("op", "setdate");
    fetch('http://tbuli12.pythonanywhere.com/recipes', {
        method: 'POST',
        body: data
    });/*.then(response => {
        return response.text()
    }).then(response => {
        alert(response);
    });*/
}

function addRecipe(name) {
    data = new FormData()
    data.append("name", name);
    data.append("op", "new");
    fetch('http://tbuli12.pythonanywhere.com/recipes', {
        method: 'POST',
        body: data
    });/*.then(response => {
        return response.text()
    }).then(response => {
        alert(response);
    });*/
    drawRecipe({"name": name});
}

function drawRecipe(recipe) {
    let newRecipeElem = document.createElement('div');
    newRecipeElem.innerHTML = recipe.name;
    newRecipeElem.dataset.rname = recipe.name;
    
    let newButton = document.createElement('button');
    newButton.innerHTML = 'Done';
    newButton.onclick = setRecipeDate;
    newRecipeElem.append(newButton);

    recipesDiv.append(newRecipeElem);
}

function drawRecipes(recipesArray) {
    recipesArray.forEach(drawRecipe);
}


fetch('http://tbuli12.pythonanywhere.com/recipes').then(response => {
    return response.json();
}).then(response => {
    drawRecipes(response);
});


/*
fetch('tbuli12.pythonanywhere.com/recipes', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
    },
    body: 
})
*/