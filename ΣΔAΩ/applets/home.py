from flask import Markup as Mk

def home(elem, method, form, args):
    elem['content'] = Mk("""
                            <div class="row gtr-200">
                                <div class="col-6 col-12-medium">
                                    <script src="//rss.bloople.net/?url=https%3A%2F%2Fsearch.cnbc.com%2Frs%2Fsearch%2Fcombinedcms%2Fview.xml%3FpartnerId%3Dwrss01%26id%3D15839069&detail=&limit=5&showtitle=true&type=js"></script>
                                </div>

                                <div class="col-6 col-12-medium">
                                    <script src="//rss.bloople.net/?url=https%3A%2F%2Fsearch.cnbc.com%2Frs%2Fsearch%2Fcombinedcms%2Fview.xml%3FpartnerId%3Dwrss01%26id%3D100646281&limit=5&showtitle=false&type=js"></script>
                                </div>

                                <div class="col-12 col-12-medium">
                                    <br>
                                </div>    

							    <div class="col-4 col-12-medium">
                                    <script src="//rss.bloople.net/?url=https%3A%2F%2Fsearch.cnbc.com%2Frs%2Fsearch%2Fcombinedcms%2Fview.xml%3FpartnerId%3Dwrss01%26id%3D20910258&showtitle=true&type=js"></script>
                                </div>
                                <div class="col-4 col-12-medium">
                                    <script src="//rss.bloople.net/?url=https%3A%2F%2Fsearch.cnbc.com%2Frs%2Fsearch%2Fcombinedcms%2Fview.xml%3FpartnerId%3Dwrss01%26id%3D10001147&showtitle=true&type=js"></script>
                                </div>
                                <div class="col-4 col-12-medium">
                                    <script src="//rss.bloople.net/?url=https%3A%2F%2Fsearch.cnbc.com%2Frs%2Fsearch%2Fcombinedcms%2Fview.xml%3FpartnerId%3Dwrss01%26id%3D44877279&showtitle=false&type=js"></script>
                                </div>
                            </div>
                                             """)
    elem['side_content'] = Mk("""<br> <br> <script src="//rss.bloople.net/?url=https%3A%2F%2Fsearch.cnbc.com%2Frs%2Fsearch%2Fcombinedcms%2Fview.xml%3FpartnerId%3Dwrss01%26id%3D100727362&limit=25&showtitle=false&type=js"></script> """)
    return elem