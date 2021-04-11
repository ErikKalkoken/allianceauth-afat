/**
 * convert a string to a slug
 * @param {string} text
 * @returns {string}
 */
let convertStringToSlug = function (text) {
    'use strict';

    return text.toLowerCase().replace(/[^\w ]+/g, '').replace(/ +/g, '-');
};

/**
 * sorting a table by its first columns alphabetically
 * @param {element} table
 * @param {string} order
 */
let sortTable = function (table, order) {
    'use strict';

    let asc = order === 'asc';
    let tbody = table.find('tbody');

    tbody.find('tr').sort(function (a, b) {
        if (asc) {
            return $('td:first', a).text().localeCompare($('td:first', b).text());
        } else {
            return $('td:first', b).text().localeCompare($('td:first', a).text());
        }
    }).appendTo(tbody);
};

/**
 * manage a modal window
 * @param {element} modalElement
 * @param {string} modalBodyText
 */
let manageModal = function (modalElement, modalBodyText) {
    'use strict';

    modalElement.on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget); // Button that triggered the modal
        let url = button.data('url'); // Extract info from data-* attributes
        let name = button.data('name');
        let modal = $(this);

        modal.find('#confirm-action').attr('href', url);
        modal.find('.modal-body').text(
            modalBodyText.replace('##NAME##', name)
        );
    }).on('hide.bs.modal', function () {
        let modal = $(this);

        modal.find('.modal-body').html('');
        modal.find('#confirm-action').attr('href', '');
    });
};
