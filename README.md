# AndyPatterns

Andy Bulka's Software Blog, Projects and Articles

This site is ready to be viewed at https://abulka.github.io/.

## Notes
The instructions below are for my own reference.  There is no need to follow them unless you are me. 

Just visit https://abulka.github.io/ to see the site.

I'm using the [Hugo](https://gohugo.io/) static site generator with the [Docsy](https://www.docsy.dev/) theme.

## 2024 Update

I've switched away from using git submodules for the Docsy theme to using Go modules based theme approach - see https://www.docsy.dev/docs/updating/convert-site-to-module/

## Installing

Installing (2024) - [Hugo modules](https://gohugo.io/hugo-modules/) are the simplest and latest way to use Hugo themes like Docsy when building a website. 

I cloned the example site and then replaced the content with my own. See 
https://github.com/google/docsy-example. In the latest version of this example project, the Docsy theme is pulled in as a Hugo module, together with its dependencies (no need for git submodules). This project has been updated similarly to use Hugo modules (no need for nasty git submodules). 

    brew install hugo
    git clone ...
    npm install

## Building Tips

Architecturally, the site is structured as follows:

    /content  --build-step-->  /docs

static content goes into

    /static/files

and be referred as e.g. `/files/pdfs/blah.pdf`.

Edit the files in `/content`, add files to `/static` and then run `bin/build` to generate the site in `/docs`. 

### Running

    bin/run

and visit
http://localhost:1313/ 

## Updating Docsy submodule
Latest Go module approach
https://www.docsy.dev/docs/updating/updating-hugo-module/

    hugo mod get -u github.com/google/docsy

## Deploying

Deploy
run

    bin/build

then commit and push

There is a action that runs on GitHub when you push, so it may take a few seconds to update.

## Adding a directory

Add it under `/content` and either create a correspondingly names dir in `/layouts` which is a custom overriding version of `/themes/layouts` or simply explicitly specify the type e.g. `type: projects` in each of the pages.

> If you want to add a top-level section, just add a new subdirectory, though you’ll need to specify the layout or content type explicitly in the frontmatter of each page if you want to use any existing Docsy template other than the default one. (from https://www.docsy.dev/docs/adding-content/content/#custom-sections)

To that section add to the menu add a `menu` entry at the top of the `_index.html` file.  The `weight` is just an arbitrary number which controls the ordering of the menu items. 

    menu:
      main:
        weight: 40
