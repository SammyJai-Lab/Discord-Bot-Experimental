getRevisionId = """
function getRevisionId() {
    let revisionIdFromUrl = window.location.pathname.match(/r[0-9]+$/);
    if (revisionIdFromUrl)
        revisionIdFromUrl = revisionIdFromUrl[0];
    let revisionIdFromState = window.__STATE__ && window.__STATE__.data && window.__STATE__.data.meta && window.__STATE__.data.meta.revisionId;
    let revisionIdForOldSongsterr = document.head.innerHTML.toString().match(/revision=([0-9]+)/);
    if (revisionIdForOldSongsterr)
        revisionIdForOldSongsterr = revisionIdForOldSongsterr[1];
    let revisionIdForNewSongsterr = document.body.innerHTML.toString().match(/"revisionId":([0-9]+)/);
    if (revisionIdForNewSongsterr)
        revisionIdForNewSongsterr = revisionIdForNewSongsterr[1];
    let revisionId = revisionIdFromUrl || revisionIdFromState || revisionIdForOldSongsterr || revisionIdForNewSongsterr;
    return revisionId;
}
"""