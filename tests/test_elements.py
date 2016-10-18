from zorn import elements

def test_page():
    page = elements.Page('Test', 'test')
    assert page.title == 'Test'
    assert page.file_name == 'test'
    assert page.sub_pages == []