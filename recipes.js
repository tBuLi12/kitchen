let recipesDiv = document.getElementById('rlist');
let addButton = document.getElementById('addbutton');
let logLink = document.getElementById('loglink');

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

logLink.onclick = () => {
    recipesDiv.innerHTML = 'You need to be logged in to view this content';
}

function setRecipeDate() {
    data = new FormData()
    data.append("name", this.parentElement.dataset.rname);
    data.append("op", "setdate");
    fetch('https://tbuli12.pythonanywhere.com/recipes', {
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
    fetch('https://tbuli12.pythonanywhere.com/recipes', {
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
    newRecipeElem.className = "recipediv";
    newRecipeElem.innerHTML = recipe.name;
    newRecipeElem.dataset.rname = recipe.name;
    
    let newButton = document.createElement('button');
    newButton.innerHTML = 'Done';
    newButton.onclick = setRecipeDate;
    
    let span = document.createElement('span');
    span.innerHTML = recipe.date;

    newRecipeElem.append(newButton);
    newRecipeElem.append(span);

    recipesDiv.append(newRecipeElem);
}

function drawRecipes(recipesArray) {
    recipesArray.forEach(drawRecipe);
}


recipesDiv.innerHTML = 'Loading recipes...';

fetch('https://tbuli12.pythonanywhere.com/recipes').then(response => {
    return response.json();
}).then(response => {
    recipesDiv.innerHTML = '';
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