const dateButton = document.getElementById("date");
const accountButton = document.getElementById("account");
const categoryButton = document.getElementById("category");
const categoryFilter = document.getElementById("filterPopover")


function open(){
    categoryFilter.hidden=false
}

function close(){
    categoryFilter.hidden=true
}

document.addEventListener("DOMContentLoaded",  () => {
    categoryButton.addEventListener("click", () => {
    categoryFilter.hidden ? open() : close();
    })
});

document.addEventListener('click', (e) => {
    if (!categoryFilter.hidden && !categoryFilter.contains(e.target) && e.target !== categoryButton) {
        close();
    }
});

  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });

