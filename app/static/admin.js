const INVITATION_DIV = (i) => `
    <tr>
        <th>${i+1}</th>
        <td><input class="form-control" type="text" value="" name="contact${i}" id="contact${i}"></td>
        <td>
            <input class="form-control" type="text" value="1" maxlength="2" name="quantity${i}" id="count${i}">
        </td>
    </tr>
`;

function buildInvitationsBlocks(e) {
    const N = +$('#number-input').val();
    if (isNaN(N) || N < 0)
        return alert('Invalid number of invitations!');
    let filling = `
        <table class="invitations table table-hover">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Recipient</th>
                            <th>Count</th>
                        </tr>
                    </thead>
                    <tbody>
    `;
    for (let i = 0; i < N; i++)
        filling += INVITATION_DIV(i);
    filling += `
        </tbody>
                </table>
    `;
    $('.invitations').empty();
    $('.invitations').append($(filling));
}



function checkData() {
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