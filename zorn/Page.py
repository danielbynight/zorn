class Page:
    def __init__(self, page_name, file_name, sub_pages=None):
        self.page_name = page_name
        self.file_name = file_name
        if sub_pages is None:
            sub_pages = []
        self.sub_pages = sub_pages
