# Zorn - a static website generator with personality
[![Build Status](https://travis-ci.org/xassbit/zorn.svg?branch=master)](https://travis-ci.org/xassbit/zorn)
[![Coverage Status](https://coveralls.io/repos/github/xassbit/zorn/badge.svg?branch=master)](https://coveralls.io/github/xassbit/zorn?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Zorn generates static websites. It's mostly a python package, but it's power can be combined [Gulp](https://www.npmjs.com/package/gulp)
in order to further automate your workflow. It supports:
- markdown content,
- one level of page nesting in navigation,
- [Jinja](http://jinja.pocoo.org) templates,
- Sass.
  
Zorn takes a lot of decisions for you. A zorn project comes out-of-the box with the capability of generating pages out of markdown
files and a few settings. It also comes with a pre-configured Gulpfile to help with the generation of html and css.

# Quick start

- Install zorn using pip by running `pip install git+git://github.com/xassbit/zorn.git@master`.
- Once installed, navigate to the directory where you want to locate your project and run `zorn`.
You will be led through the creation of a new project.

# Page blocks

A canonical zorn page has four blocks: *header*, *navigation*, *body* and *footer*.  
The *header* and *footer* blocks is the same for all pages and include the site title, subtitle and author.  
The *navigation* block includes links to all pages. Zorn adds the class `active` to the link to the page you are looking at to help styling.  
The *body* block takes the html rendered from the markdown file for that page.  
There is a fifth block called *head* wich contains meta-information about the page.


# File structure

A canonical zorn project has the following structure:

    my_project
        |_md
        |   |_index.md
        |   |_(other pages).md
        |_scss
        |   |_ _header.scss
        |   |_ _nav.scss
        |   |_ _settings.scss
        |   |_main.scss
        |_node_modules
        |   |_(node modules)
        |_admin.py
        |_settings.py
        |_package.json
        |_gulpfile.js
        |_main.css
        |_main.min.css
        |_index.html
        |_(other pages).html
        
where `my_project` is the name of your project.

# Nesting

Zorn allows for pages to be nested as subpages. Subpages show as dropdown under their parent on the navigation menu.
Also if the setting `URL_STYLE` is set to `'nested'`, they are generated into a folder with the name of their parent.

# Markdown content

The `md` folder is where you can drop markdown files with the content of the website's pages.
These files should be named with the name of the page they relate to.
For example, the content for `index.html` should be in the `index.md` file.
Not all pages need an associated `.md` file and `.md` files for which there is no associated page are ignored when generating the website.

# Style

When creating a zorn project by running `zorn` you can choose a default style. This will be imported to your project's directory. The default style is "basic". 
The stylesheets for the website are generated from [Sass](http://sass-lang.com) files with Gulp. The file `main.scss` just imports the other `.scss` files.
The file `settings.scss` has the main style settings, like colors and fonts.

# Command line

By default the project comes equiped with a `package.json` file, which is used to install Gulp once run `npm install`.
Gulp runs taks defined in `gulpfile.js`. Running `gulp` generates the css and html files.
Running `gulp watch` has Gulp watching for changes in the `.scss` and `.md` files as well as `settings.py` and re-generate the site when this files are modified and saved.  

You can interact with zorn in two ways. In order to create a project just invoke zorn from the command line by running `zorn`.
This command can take some arguments:

- `-v` or `--verbose` - make zorn talk more;
- `-s` or `--silent` - silence zorn (when this setting is on and a name was given, the project will be generated without prompting you once);
- `-n` or `--name` - pass the name you want to give your project (the project is created in a new directory with this name);
- `-t` or `--title` - pass the title of your site;
- `-a` or `--author` - pass the name of the author of your site;
- `--style` - choose one of the available styles for your site;
- `-g` or `--g` - add this flag if you want to generate the site after the creation process.

After a project was created, you can manage it by interacting with zorn through `admin.py`. Here is a list of commands (all should be appended to `python admin.py` when run from your project's root directory):

- `generate` - generates the website;
- `importtemplates` - imports the templates locally (to your project's directory). Pass the flag `-u` or `-update` to update the settings file;
- `importstyle:a_style` where `a_style` is one of the available styles - imports a style to the root directory of your project, i.e., creates a directory with the name of the style and the original Sass files of that style;
- `--help` - lists all available commands.

These flags can also be appended:

- `-v` or `--verbose` - make zorn talk more;
- `-s` or `--silent` - silence zorn.

# Settings

Here is a list of the available settings for a zorn project.

*Non-optional settings*
- `ROOT_DIR` - the root of your project, which should be `os.path.dirname(os.path.abspath(__file__))`.
- `PROJECT_NAME` - the name of your project.

*Optional settings*
- `DEBUG` - a boolean which states if you are on not in debug mode. By default it's `True`.

When in debug mode, the stylesheet used is `main.css` and the routes to pages point to files in your file system (they look like `../a-page/a-sub-page.html`).
If debug mode is disabled, the stylesheet used is the minified one (`main.min.css`) and routes are relative to your site's root url (they look like `/a-page/a-sub-page`).

When `False` the minified CSS is used.
- `URL_STYLE` - can be `'flat'` or `'nested'`. If the former is chosen then all html files are generated in your root directory.
If `nested` the subpages are generated into a folder with the name of their parent. This allows for urls like `domain/page/subpage`
- `SITE_DIR` - the directory where your site will be generated. `ROOT_DIR` by default.
Note: the stylesheets location may have to be updated in the gulpfile (for example, `.pipe(gulp.dest('site'));`).
- `TEMPLATES_DIR` - in case you have your templates directory locally on the project's root then pass here its path.
- `MARKDOWN_DIR` - the directory of you markdown content. By default it's `os.path.join(ROOT_DIR, 'md')`
- `MARKDOWN_EXTENSIONS` - the [extensions](http://pythonhosted.org/Markdown/extensions/index.html) to the markdown parser.
- `SITE_TITLE` - the title of your site. By default it's the project name capitalized and with hiphens and underscores replaced by spaces.
- `SITE_SUBTITLE` - the subtitle of your website, blank by default.
- `DESCRIPTION` - the description of your site, which is used in the *head* block.
- `AUTHOR` - the site's author, by default it's the terminal user.
- `KEYWORDS` - a list of keywords to your site, which are used in the *head* block.

# Pages
Registed the pages of your website as a list of `zorn.elements.Page` objects under the setting `PAGES`.
If you want some nesting then register the subpages as a list of `zorn.elements.SubPage` objects under the parent page.
If you want to generate a page which doesn't feature in the top navigation, register it as an `UnlinkedPage`.
The first argument of a `Page` or `SubPage` is the page's title and the second argument is a string which is going to be used to name the page's files (html and md).
An `UnlinkedPage` takes as a third argument the pieces of its path.
The order the pages appear in the navigation is taken from the order of pages in these lists.
Example:

    PAGES = [
        # main pages
        elements.Page('Home', 'index'),
        elements.Page('Page 1', 'page1'),
        elements.Page('Page 2', 'page2', [
            
            # pages nested under Page 2
            elements.SubPage('Sub Page 1', 'subpage1'),
            elements.SubPage('Sub Page 2', 'subpage2'),
        ]),
        elements.Page('Page 3', 'page3'),
        
        # creates an unlinked page under the url domain/path/to/unlinked
        elements.UnlinkedPage('Unlinked Page, 'unlinked', ['path', 'to']
    ]
    
# Routing
You can link from one page of your website to another from the markdown content by using a route tag.
This is a tag which starts and ends with `@@` and encloses the file name of the page you want to link to (without '.md' or '.html').
For example, considering that you have the following in your website settings:

    PAGES = [
        elements.Page('Home', 'index'),
        elements.Page('Such a great page', 'great-page', [
            elements.SubPage('Not a bad page either', 'not-bad')
        ]
    ]
    
    DEBUG = False
    URL_STYLE = 'nested'
 
Then the markdown content `...and you can click [here](@@not-bad@@) to check out a good page...` placed in `index.md` will be converted to

    ...and you can click <a href="/great-page/not-bad">here</a> to check out a good page...`.
 
   
 If you wish for the characters `@@` to not indicate a route you can escape them with backslashes: `\@\@`.
    