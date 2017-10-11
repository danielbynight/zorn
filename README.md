# Zorn - a static website generator

Install this version by running
```bash
pip install git+https://github.com/xassbit/zorn.git@zorn1
```

## Quick Start

Zorn is a simple website generator. To generate a site simply drop a Python script in your project root which imports `zorn` and start writing configuration. It should look something like this:

```python
class Settings(zorn.Settings):
    PAGES = (
        zorn.Page(template_name='index.html', name='home'),
    )
    PROCESSORS = (
        zorn.processors.JinjaProcessor,
        zorn.processors.FileSystemProcessor,
    )
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')
    OUTPUT_DIR = os.path.join(CommonSettings.ROOT_DIR, 'docs')
```

At the end of the script simply instantiate a `zorn.Project` and call its `generate` method. Like so:

```python
if __name__ == '__main__':
    project = Project(Settings)
    project.generate()
```

## Settings

Learning about the available settings should be enough to understand `zorn`.

### `PAGES`

List or tuple of `zorn.Page` objects, each of which should describe a page of your website. `Page` objects takes the following arguments:

 - `template_name` (only required argument) - (a path from `Settings.TEMPLATES_DIR` pointing to the template file which should be used to generate the page);
 - `file_name` - the name of the file which should be exported;
 - `context` - a dictionary to be passed to a template as its context;
 - `route` - the path to the file, which will correspond to the url of a page;
 - `name` - a name to refer to the page internally (useful for routes).

### `PROCESSORS`

List of `zorn.Processor` child classes. These are read in order and will be used to manipulate the content of a page. Zorn offers the following processors (but you can write your own):

- `zorn.processors.JinjaProcessor` - reads a Jinja2 template and outputs html;
- `zorn.processors.FileSystemProcessor` - writes the page content in a file;
- `zorn.processors.JSONContextProcessor` - takes the context of a page from a JSON file. Requires the setting `JSON_DIR`, pointing to a directory which should mimic the structure of `TEMPLATES_DIR`.


### `PLUGINS`

List or tuple of `zorn.Plugin` objects. Zorn comes with `zorn.plugins.StaticFilesMoverPlugin`, which moves files in `Settings.STATIC_DIRS` to `Settings.OUTPUT_DIR`.


### `TEMPLATES_DIR`

The directory which contains the files for your site's pages.

### `OUTPUT_DIR`

The directory where the site's pages will be generated to. Only required when using `zorn.processors.FileSystemProcessor`.

### `DEVELOPMENT`

A boolean which is passed to processors in order to distinguish if the current project is in "development" mode or in "production" mode. `zorn.processors.JinjaProcessor` uses it.