# AndyPatterns

Andy Bulka's Software Blog, Projects and Articles

This site is ready to be viewed at https://abulka.github.io/.

## Notes
The instructions below are for my own reference.  There is no need to follow them unless you are me. 

Just visit https://abulka.github.io/ to see the site.

I'm using the [Hugo](https://gohugo.io/) static site generator with the [Docsy](https://www.docsy.dev/) theme.

## 2024 Update

I've switched away from using git submodules for the Docsy theme to using Go modules based theme approach - see https://www.docsy.dev/docs/updating/convert-site-to-module/

## 2026 Update - building with newer Hugo versions

Newer Hugo releases (>= 0.161) added security policies that break the Docsy build out of
the box. If you install a recent Hugo via `brew install hugo`, add/keep these settings in
`hugo.toml` (they were added 2026-08-12 to build with Hugo 0.164):

    [security]
      allowContent = [".*"]

    [security.node]
      [security.node.permissions]
        disable = true

- `security.allowContent` (new in Hugo 0.162) denies `text/html` content files by default;
  the site has `.html` content pages, so content types must be allowed.
- `security.node.permissions` (new in Hugo 0.161) runs Node tools (e.g. PostCSS used by
  Docsy's SCSS pipeline) under a restricted permission model; it must be disabled for the
  theme's asset build to work.

Older Hugos (before 0.161) did not have these defaults, which is why the site built
without them before.

## Installing

Installing (2024) - [Hugo modules](https://gohugo.io/hugo-modules/) are the simplest and latest way to use Hugo themes like Docsy when building a website. 

I cloned the example site and then replaced the content with my own. See 
https://github.com/google/docsy-example. In the latest version of this example project, the Docsy theme is pulled in as a Hugo module, together with its dependencies (no need for git submodules). This project has been updated similarly to use Hugo modules (no need for nasty git submodules). 

    brew install hugo
    git clone ...
    npm install

## Building Tips

Architecturally, the site is structured as follows:

    /content  --build-step-->  /public

static content goes into

    /static/files

and be referred as e.g. `/files/pdfs/blah.pdf`.

Edit the files in `/content`, add files to `/static` and then run `bin/build` to generate the site in `/public`. The generated `/public` (and the old `/docs`) output is gitignored - you never commit build output.

### Running

    bin/run

and visit
http://localhost:1313/ 

## Updating Docsy submodule
Latest Go module approach
https://www.docsy.dev/docs/updating/updating-hugo-module/

    hugo mod get -u github.com/google/docsy

## Deploying

Just commit and push your source changes (in `/content`, `/static`, etc.). A GitHub
Actions workflow (`.github/workflows/deploy.yml`) builds the site and deploys it to
GitHub Pages automatically. It takes a few seconds to update.

Note: the GitHub Pages publishing source must be set to **GitHub Actions**
(Settings → Pages → Build and deployment → Source), not "Deploy from a branch".

To preview locally first:

    bin/run

and visit http://localhost:1313/

## Adding a directory

Add it under `/content` and either create a correspondingly names dir in `/layouts` which is a custom overriding version of `/themes/layouts` or simply explicitly specify the type e.g. `type: projects` in each of the pages.

> If you want to add a top-level section, just add a new subdirectory, though you’ll need to specify the layout or content type explicitly in the frontmatter of each page if you want to use any existing Docsy template other than the default one. (from https://www.docsy.dev/docs/adding-content/content/#custom-sections)

To that section add to the menu add a `menu` entry at the top of the `_index.html` file.  The `weight` is just an arbitrary number which controls the ordering of the menu items. 

    menu:
      main:
        weight: 40
