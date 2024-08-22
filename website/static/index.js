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