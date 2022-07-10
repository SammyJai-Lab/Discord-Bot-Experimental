from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup

import asyncio


asession = AsyncHTMLSession()

async def downloadSongsterr():

    SONGSTERR_URL = 'https://www.songsterr.com/a/wsa/tim-henson-the-worst-riff-dimarzio-showcase-tab-s464648/'

    r = await asession.get(SONGSTERR_URL)

    await r.html.arender()

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

    revisionID = await r.html.arender(script=getRevisionId, reload=False)

    await r.close()

    XML_URL = f"https://www.songsterr.com/a/ra/player/songrevision/{revisionID}.xml"

    r = await asession.get(XML_URL)

    data = BeautifulSoup(r.text, "xml")

    await r.close()

    GP_URL = data.find("attachmentUrl").text

    filename = GP_URL.split('/')[-1]

    r = await asession.get(GP_URL)

    open(filename, "wb").write(r.content)

    await r.close()