const INVITATION_DIV = (i) => `
    <div class="invitation">
        <label for="contact${i}" class="col-2 col-form-label" >Contact: </label>
        <input class="form-control" type="text" value="" name="contact${i}" id="contact${i}">
        <label for="count${i}" class="col-2 col-form-label">Count: </label>
        <input class="form-control" type="text" value="1" maxlength="2" name="quantity${i}" id="count${i}">
    </div>
`;

function buildInvitationsBlocks(e) {
    const N = +$('#number-input').val();
    console.log('hui')
    if (isNaN(N) || N < 0)
        return alert('Invalid number of invitations!');
    let filling = '';
    for (let i = 0; i < N; i++)
        filling += INVITATION_DIV(i);
    $('.invitations').empty();
    $('.invitations').append($(filling));
}



function checkData(e) {
    e.preventDefault();
    const N = +$('#number-input').val();
    for (let i = 0; i < N; i++) {
        let forCheck = +$(`#count${i}`).val();
        if (isNaN(forCheck) || forCheck < 0)
            return false;
    }
    return true;
}

$(function() {
    $('#generate').click(buildInvitationsBlocks);
    $('#submit').click(function(e) {
        if (!checkData()) {
            alert('Wrong data input!');
            e.preventDefault();
        }
    });
});