# AndyPatterns

Andy Bulka's Software Blog, Projects and Articles

This site is ready to be viewed at https://abulka.github.io/.

## Installing

    brew install hugo
    git submodule add https://github.com/google/docsy.git themes/docsy
    git submodule update --init --recursive
    npm install

## Building Tips

    /content  --build-step-->  /docs

static content can go into e.g.

    /static/files

and be referred as `/files/pdfs/blah.pdf`.

## Updating Docsy submodule

    git submodule update --init --recursive

## Adding a directory

Add it under `/content` and either create a correspondingly names dir in `/layouts` which is a custom overriding version of `/themes/layouts` or simply explicitly specify the type e.g. `type: projects` in each of the pages.

> If you want to add a top-level section, just add a new subdirectory, though you’ll need to specify the layout or content type explicitly in the frontmatter of each page if you want to use any existing Docsy template other than the default one. (from https://www.docsy.dev/docs/adding-content/content/#custom-sections)

To that section add to the menu add a `menu` entry at the top of the `_index.html` file.  The `weight` is just an arbitrary number which controls the ordering of the menu items. 

    menu:
      main:
        weight: 40
