[].forEach.call(document.getElementsByClassName('tags-input'), function (el) {
    let hiddenInput = document.createElement('input'),
        mainInput = document.createElement('input'),
        tags = [];

    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', el.getAttribute('data-name'));
    hiddenInput.setAttribute('id', el.getAttribute('data-name'));
    mainInput.setAttribute('type', 'text');
    mainInput.setAttribute('placeholder', 'tags...')
    mainInput.setAttribute('onfocus', "this.placeholder=''");
    if (tags.length == 0) {
        mainInput.setAttribute('onblur', "this.placeholder='tags...'");
    }
    mainInput.classList.add('main-input');

    mainInput.addEventListener('input', function () {
        let enteredTags = mainInput.value.split(',');
        if (enteredTags.length > 1) {
            enteredTags.forEach(function (t) {
                let filteredTag = filterTag(t);
                if (filteredTag.length > 0)
                    addTag(filteredTag);
            });
            mainInput.value = '';
        }
    });

    mainInput.addEventListener('keydown', function (e) {
        let keyCode = e.which || e.keyCode;
        // add a tag with Enter key in addition to comma
        if (keyCode === 13 && mainInput.value.length > 0) {
            addTag(mainInput.value);
            mainInput.value = "";
        }
        // delete tag with backspace key
        if (keyCode === 8 && mainInput.value.length === 0 && tags.length > 0) {
            removeTag(tags.length - 1);
        }
    });

    el.appendChild(mainInput);
    el.appendChild(hiddenInput);


    function addTag(text) {
        let tag = {
            text: text,
            element: document.createElement('span'),
        };

        tag.element.classList.add('tag');
        tag.element.textContent = tag.text;

        let closeBtn = document.createElement('span');
        closeBtn.classList.add('close');
        closeBtn.addEventListener('click', function () {
            removeTag(tags.indexOf(tag));
        });
        tag.element.appendChild(closeBtn);

        tags.push(tag);

        el.insertBefore(tag.element, mainInput);

        refreshTags();
    }


    function removeTag(index) {
        let tag = tags[index];
        tags.splice(index, 1);
        el.removeChild(tag.element);
        refreshTags();
    }

    function refreshTags() {
        let tagsList = [];
        tags.forEach(function (t) {
            tagsList.push(t.text);
        });
        hiddenInput.value = tagsList.join(',');
    }

    function filterTag(tag) {
        // trim anything that isn't a word character, space or dash, then replace all white spaces with a dash
        return tag.replace(/[^\w -]/g, '').trim().replace(/\W+/g, '-');
    }
});


function filterByTag(t) {
    fetch('/filter-tag', {
        method: "POST",
        body: JSON.stringify({ tag: t }),
        redirect: 'manual'
    }).then((_res) => {
        window.location.href = `/filter-tag/${t}`
    });
}
