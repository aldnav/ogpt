
/***
 * Table select all
 ***/
$('table').on('click', 'thead input[type="checkbox"]', e => {
    // Check all boxes when header checkbox is ticked
    let table = $(e.target).closest('table');
    table.find('tbody td input[type="checkbox"]').prop('checked', $(e.target).prop('checked'));
    saveSelectedColumnIds(table);
});
$('table').on('click', 'tbody td input[type="checkbox"]', e => {
    // Un-tick header checkbox when not all table checkboxes are ticked
    let table = $(e.target).closest('table');
    let checkboxes = table.find('tbody input[type="checkbox"]');
    let checked = checkboxes.filter(':checked');
    if (checked.length !== checkboxes.length) {
        table.find('thead input[type="checkbox"]').prop('checked', false);
    }
    saveSelectedColumnIds(table);
});
function saveSelectedColumnIds(table) {
    let checked = table.find('tbody input[type="checkbox"]').filter(':checked');
    $('#export_selected_form input[name="_selected_column_ids"]').val(
        checked.map(function() {
            return this.value;
        }).get().join());
    // FIXME: Make flexible getting table of actions
    $('.table-actions--download-selected').toggleClass('d-none', checked.length === 0);
}

$('.export-selected').on('click', (e) => {
    e.preventDefault();
    let exportLink = $(e.target).prop('href');
    window.location = exportLink + '&' + $('#export_selected_form').serialize();
});
