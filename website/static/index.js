// prevent Enter key from submitting the form
window.addEventListener('keydown', function (e) {
    if (e.keyIdentifier == 'U+000A' || e.keyIdentifier == 'Enter' || e.keyCode == 13) {
        if (e.target.nodeName == 'INPUT' && e.target.type == 'text') {
            e.preventDefault();
            var nextInput = inputs.get(inputs.index(this) + 1);
            if (nextInput) {
                nextInput.focus();
            }
            return false;
        }
    }
}, true);


// prevent automatic form submit when refreshing page
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}


// set color for amount based on whether it's income or expense
let tableAmount = document.getElementsByClassName("amount-flag");
for (let i = 0; i < tableAmount.length; i++) {
    if (tableAmount[i].innerHTML < 0)
        tableAmount[i].parentNode.style.color = 'red';
    else if (tableAmount[i].innerHTML > 0)
        tableAmount[i].parentNode.style.color = 'green';
    tableAmount[i].innerHTML += '€';
}


// handles 'Income' and 'Expenses' flags
function handleClick(val) {
    document.getElementById('flag').value = val;
    return true;
}

// deletes rows in /edit page
function deleteRow(rowId) {
    fetch('/delete-row', {
        method: 'POST',
        body: JSON.stringify({ rowId: rowId }),
    }).then((_res) => {
        window.location.href = "./edit"
    });
}


// functions for dynamic insertion of new options in dropdown

function DropDownChanged(oDDL) {
    var newCategoryTxt = document.getElementById("category_in");
    if (newCategoryTxt) {
        newCategoryTxt.style.display = (oDDL.value == "") ? "" : "none";
        if (oDDL.value == "")
            newCategoryTxt.focus();
    }
}


function FormSubmit() {
    // for select dropdown
    var newCategoryTxt = document.getElementById("category_in")
    var oHidden = document.getElementById("category");
    var oDDL = document.getElementById("category_ddl");
    if (oHidden && oDDL && newCategoryTxt)
        oHidden.value = (oDDL.value == "") ? newCategoryTxt.value : oDDL.value;

}


let years = document.getElementById("yearSelect");

for (let i=0; i < years.length; i++) {
    years[i].selectedIndex = 0;
}
