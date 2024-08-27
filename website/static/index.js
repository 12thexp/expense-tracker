function handleClick(val){
    document.getElementById('flag').value = val;
    return true;
}


function deleteRow(rowId) {
    fetch('/delete-row', {
        method: 'POST',
        body: JSON.stringify({ rowId: rowId}),
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