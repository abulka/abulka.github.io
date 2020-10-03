
---
title: "on-images"
linkTitle: "Plantuml Images Baby"
date: 2019-01-04
description: >
  A short lead description about this content page. Text here can also be **bold** or _italic_ and can even be split over multiple paragraphs.
---

## baseURL broken

https://github.com/gohugoio/hugo/issues/5226

You need to set to true to make image links generated with full path incl. the 'hugo-docsy-example' sub-path 
```toml
canonifyurls = true
```

For example these images will not render unless canonifyurls is true cos the subpath of the baseURL is not generated for assets - thus is relevant for deploying to github project pages
![png your image](/blog/images/fred.png)
![png your image](/images/uml/fred-uml.png)
but its a bit ugly having to turn canonifyurls on because all the links in the website become long, absolute.

Gee this is needed also for previewing locally! WTF
but https://discourse.gohugo.io/t/solved-generate-wrong-image-relative-url/11726 says:
> The baseURL config doesn’t affect links set in markdown.

### Andy's shortcode hack
You can refer to images in html files using `RelPermalink` but for markdown files which don't allow such templating, we have to encapsulate the trick into a shortcode fragment
```html
{{ .Get 0 | absURL }}
```

E.g. trying to add a shortccodes to image urls can be the solution (no leading /, either viz `images/...` not `/images/...`)
This workaround trick seems to survive turning canonifyurls off.

![png your image]({{< andy/img "blog/images/fred.png" >}})
![png your image]({{< andy/img "images/uml/fred-uml.png" >}})

Note: trying to fiddle with my shortcode and get a relpermalink into it has been abandoned
```html
{{ $url := .Get 0 | absURL }}
{{/* $url = $url.RelPermalink */}}
{{/* {{ $url = .RelPermalink }} */}}
{{ $url }}
```

### leaving off the slash
leaving off the leading / on image references as recommended [here](https://github.com/gohugoio/hugo/issues/5736) is not the solution either because the images don't show up in development server mode, nor does the right url get generated when you generate the static site

![png your image](blog/images/fred.png)
![png your image](images/uml/fred-uml.png)

e.g.

```
relative to blog/... unless you put the /blog in there you get
http://localhost:1313/   blog/2019/01/04/plantuml-images/blog/images/fred.png 404 (Not Found)

with the /blog you get the correct
http://localhost:1313/   blog/images/fred.png

viz.

bad urls generated:
<img src="/blog/images/fred.png" alt="png your image">
<img src="/images/uml/fred-uml.png" alt="png your image">

leaving off the leading / on image references is not the solution either
<img src="blog/images/fred.png" alt="png your image">
<img src="images/uml/fred-uml.png" alt="png your image">

```


## Experiments with page variables

<!-- {{ .RelPermalink }} -->
your site's url is {{< andy/siteurl >}} hi `there` andy.

your site's url is
```
{{< andy/siteurl >}}
```

The `.Page.RelPermalink` and `.Page.Permalink` are
```
{{< andy/rel_permalink >}}
{{< andy/permalink >}}
```

# links and xrefs

all these are correctly output - either absolute or relative links get the correct path from the baseUrl inserted

[pynsource dir]({{< ref "/projects/aaaa-pynsource/" >}} "About Us")

[pynsource info]({{< ref "some-info" >}} "some-info")

[pynsource info]({{< ref "some-info.md" >}} "some-info")

[pynsource info]({{< relref "/projects/aaaa-pynsource/some-info.md" >}} "some-info")

[pynsource info]({{< relref "projects/aaaa-pynsource/some-info.md" >}} "some-info")

viz.
```
<p><a href="https://abulka.github.io/hugo-docsy-example/projects/aaaa-pynsource/" title="About Us">pynsource dir</a></p>
<p><a href="https://abulka.github.io/hugo-docsy-example/projects/aaaa-pynsource/some-info/" title="some-info">pynsource info</a></p>
<p><a href="https://abulka.github.io/hugo-docsy-example/projects/aaaa-pynsource/some-info/" title="some-info">pynsource info</a></p>
<p><a href="/hugo-docsy-example/projects/aaaa-pynsource/some-info/" title="some-info">pynsource info</a></p>
<p><a href="/hugo-docsy-example/projects/aaaa-pynsource/some-info/" title="some-info">pynsource info</a></p>
```


http://localhost:1313/projects/aaaa-pynsource/

http://localhost:1313/projects/aaaa-pynsource/some-info/

# ANDY IMAGES

## svg is ok

but has no background unless you specify

```plantuml
skinparam backgroundcolor AntiqueWhite/Gold
```

See colour info https://plantuml.com/color 

## serve from the blog subdir

![svg your image](/blog/images/fred.svg)

__shortcode hack version:__
![png your image]({{< andy/img "blog/images/fred.svg" >}})

### what about a png?

from the blog subdir

![png your image](/blog/images/fred.png)

__shortcode hack version:__
![png your image]({{< andy/img "blog/images/fred.png" >}})

## serve from static dir

from a common dir in `/static` - note that you don't
need to specify the `/static` part of the path, just the subdir path.

![png your image](/images/uml/fred-uml.png)

__shortcode hack version:__
![png your image]({{< andy/img "images/uml/fred-uml.png" >}})

remember to set the out path of plantuml vscode plugin to `static/images/uml/`

## local uml dir

you can keep uml `.wsd` files anywhere so how about in a subdir within the blog area you are writing for - they still get exported to a common place though.

{{% alert title="Note" %}}
Note that images will **always** end up in a subdirectory structure - even if you specify `exportSubFolder` false - cos that only controls an extra dir level with the same name as the uml file, not the whole dir levels thing.
```json
{
    "plantuml.exportOutDir": "static/images/uml",
    "plantuml.exportSubFolder": false
}
```
{{% /alert %}}

So you need to specify a long path into the static dir - related to where your *original* source code lives e.g.
`/images/uml/content/en/blog/newcat/uml/test-uml.png`

![png your image](/images/uml/content/en/blog/newcat/uml/test-uml.png)


__shortcode hack version:__
![png your image]({{< andy/img "images/uml/content/en/blog/newcat/uml/test-uml.png" >}})

## docsy theme visualised using my tool

[![svg your image](/images/uml/content/en/blog/newcat/uml/docsy.svg)](/images/uml/content/en/blog/newcat/uml/docsy.svg)

__shortcode hack version:__
[![svg your image]({{< andy/img "images/uml/content/en/blog/newcat/uml/docsy.svg" >}})]({{< andy/img "images/uml/content/en/blog/newcat/uml/docsy.svg" >}})

## my new 'imgsvg' shortcode attempt 
it works!

{{< andy/img2 "images/uml/content/en/blog/newcat/uml/docsy.svg" >}}
just the image

{{< andy/imgsvg "images/uml/content/en/blog/newcat/uml/docsy.svg" >}}
image with clickable link








## Usual content

Text can be **bold**, _italic_, or ~~strikethrough~~. [Links](https://github.com) should be blue with no underlines (unless hovered over).

There should be whitespace between paragraphs. There should be whitespace between paragraphs. There should be whitespace between paragraphs. There should be whitespace between paragraphs.

There should be whitespace between paragraphs. There should be whitespace between paragraphs. There should be whitespace between paragraphs. There should be whitespace between paragraphs.

> There should be no margin above this first sentence.
>
> Blockquotes should be a lighter gray with a border along the left side in the secondary color.
>
> There should be no margin below this final sentence.

## First Header

This is a normal paragraph following a header. Bacon ipsum dolor sit amet t-bone doner shank drumstick, pork belly porchetta chuck sausage brisket ham hock rump pig. Chuck kielbasa leberkas, pork bresaola ham hock filet mignon cow shoulder short ribs biltong.  Bacon ipsum dolor sit amet t-bone doner shank drumstick, pork belly porchetta chuck sausage brisket ham hock rump pig. Chuck kielbasa leberkas, pork bresaola ham hock filet mignon cow shoulder short ribs biltong.  Bacon ipsum dolor sit amet t-bone doner shank drumstick, pork belly porchetta chuck sausage brisket ham hock rump pig. Chuck kielbasa leberkas, pork bresaola ham hock filet mignon cow shoulder short ribs biltong.



Bacon ipsum dolor sit amet t-bone doner shank drumstick, pork belly porchetta chuck sausage brisket ham hock rump pig. Chuck kielbasa leberkas, pork bresaola ham hock filet mignon cow shoulder short ribs biltong.

On big screens, paragraphs and headings should not take up the full container width, but we want tables, code blocks and similar to take the full width.

Lorem markdownum tuta hospes stabat; idem saxum facit quaterque repetito
occumbere, oves novem gestit haerebat frena; qui. Respicit recurvam erat:
pignora hinc reppulit nos **aut**, aptos, ipsa.

Meae optatos *passa est* Epiros utiliter *Talibus niveis*, hoc lata, edidit.
Dixi ad aestum.

## Header 2

> This is a blockquote following a header. Bacon ipsum dolor sit amet t-bone doner shank drumstick, pork belly porchetta chuck sausage brisket ham hock rump pig. Chuck kielbasa leberkas, pork bresaola ham hock filet mignon cow shoulder short ribs biltong.

### Header 3

```
This is a code block following a header.
```

#### Header 4

* This is an unordered list following a header.
* This is an unordered list following a header.
* This is an unordered list following a header.

##### Header 5

1. This is an ordered list following a header.
2. This is an ordered list following a header.
3. This is an ordered list following a header.

###### Header 6

| What      | Follows         |
|-----------|-----------------|
| A table   | A header        |
| A table   | A header        |
| A table   | A header        |

----------------

There's a horizontal rule above and below this.

----------------

Here is an unordered list:

* Salt-n-Pepa
* Bel Biv DeVoe
* Kid 'N Play

And an ordered list:

1. Michael Jackson
2. Michael Bolton
3. Michael Bublé

And an unordered task list:

- [x] Create a sample markdown document
- [x] Add task lists to it
- [ ] Take a vacation

And a "mixed" task list:

- [ ] Steal underpants
- ?
- [ ] Profit!

And a nested list:

* Jackson 5
  * Michael
  * Tito
  * Jackie
  * Marlon
  * Jermaine
* TMNT
  * Leonardo
  * Michelangelo
  * Donatello
  * Raphael

Definition lists can be used with Markdown syntax. Definition terms are bold.

Name
: Godzilla

Born
: 1952

Birthplace
: Japan

Color
: Green


----------------

Tables should have bold headings and alternating shaded rows.

| Artist            | Album           | Year |
|-------------------|-----------------|------|
| Michael Jackson   | Thriller        | 1982 |
| Prince            | Purple Rain     | 1984 |
| Beastie Boys      | License to Ill  | 1986 |

If a table is too wide, it should scroll horizontally.

| Artist            | Album           | Year | Label       | Awards   | Songs     |
|-------------------|-----------------|------|-------------|----------|-----------|
| Michael Jackson   | Thriller        | 1982 | Epic Records | Grammy Award for Album of the Year, American Music Award for Favorite Pop/Rock Album, American Music Award for Favorite Soul/R&B Album, Brit Award for Best Selling Album, Grammy Award for Best Engineered Album, Non-Classical | Wanna Be Startin' Somethin', Baby Be Mine, The Girl Is Mine, Thriller, Beat It, Billie Jean, Human Nature, P.Y.T. (Pretty Young Thing), The Lady in My Life |
| Prince            | Purple Rain     | 1984 | Warner Brothers Records | Grammy Award for Best Score Soundtrack for Visual Media, American Music Award for Favorite Pop/Rock Album, American Music Award for Favorite Soul/R&B Album, Brit Award for Best Soundtrack/Cast Recording, Grammy Award for Best Rock Performance by a Duo or Group with Vocal | Let's Go Crazy, Take Me With U, The Beautiful Ones, Computer Blue, Darling Nikki, When Doves Cry, I Would Die 4 U, Baby I'm a Star, Purple Rain |
| Beastie Boys      | License to Ill  | 1986 | Mercury Records | noawardsbutthistablecelliswide | Rhymin & Stealin, The New Style, She's Crafty, Posse in Effect, Slow Ride, Girls, (You Gotta) Fight for Your Right, No Sleep Till Brooklyn, Paul Revere, Hold It Now, Hit It, Brass Monkey, Slow and Low, Time to Get Ill |

----------------

Code snippets like `var foo = "bar";` can be shown inline.

Also, `this should vertically align` ~~`with this`~~ ~~and this~~.

Code can also be shown in a block element.

```
foo := "bar";
bar := "foo";
```

Code can also use syntax highlighting.

```go
func main() {
  input := `var foo = "bar";`

  lexer := lexers.Get("javascript")
  iterator, _ := lexer.Tokenise(nil, input)
  style := styles.Get("github")
  formatter := html.New(html.WithLineNumbers())

  var buff bytes.Buffer
  formatter.Format(&buff, style, iterator)

  fmt.Println(buff.String())
}
```

```
Long, single-line code blocks should not wrap. They should horizontally scroll if they are too long. This line should be long enough to demonstrate this.
```

Inline code inside table cells should still be distinguishable.

| Language    | Code               |
|-------------|--------------------|
| Javascript  | `var foo = "bar";` |
| Ruby        | `foo = "bar"{`      |

----------------

Small images should be shown at their actual size.

![](https://placekitten.com/g/300/200/)

Large images should always scale down and fit in the content container.

![](https://placekitten.com/g/1200/800/)

## Components

### Alerts

{{< alert >}}This is an alert.{{< /alert >}}
{{< alert title="Note:" >}}This is an alert with a title.{{< /alert >}}
{{< alert type="success" >}}This is a successful alert.{{< /alert >}}
{{< alert type="warning" >}}This is a warning!{{< /alert >}}
{{< alert type="warning" title="Warning!" >}}This is a warning with a title!{{< /alert >}}


## Sizing

Add some sections here to see how the ToC looks like. Bacon ipsum dolor sit amet t-bone doner shank drumstick, pork belly porchetta chuck sausage brisket ham hock rump pig. Chuck kielbasa leberkas, pork bresaola ham hock filet mignon cow shoulder short ribs biltong.

### Parameters available

Bacon ipsum dolor sit amet t-bone doner shank drumstick, pork belly porchetta chuck sausage brisket ham hock rump pig. Chuck kielbasa leberkas, pork bresaola ham hock filet mignon cow shoulder short ribs biltong.

### Using pixels

Bacon ipsum dolor sit amet t-bone doner shank drumstick, pork belly porchetta chuck sausage brisket ham hock rump pig. Chuck kielbasa leberkas, pork bresaola ham hock filet mignon cow shoulder short ribs biltong.

### Using rem

Bacon ipsum dolor sit amet t-bone doner shank drumstick, pork belly porchetta chuck sausage brisket ham hock rump pig. Chuck kielbasa leberkas, pork bresaola ham hock filet mignon cow shoulder short ribs biltong.

## Memory

Bacon ipsum dolor sit amet t-bone doner shank drumstick, pork belly porchetta chuck sausage brisket ham hock rump pig. Chuck kielbasa leberkas, pork bresaola ham hock filet mignon cow shoulder short ribs biltong.

### RAM to use

Bacon ipsum dolor sit amet t-bone doner shank drumstick, pork belly porchetta chuck sausage brisket ham hock rump pig. Chuck kielbasa leberkas, pork bresaola ham hock filet mignon cow shoulder short ribs biltong.

### More is better

Bacon ipsum dolor sit amet t-bone doner shank drumstick, pork belly porchetta chuck sausage brisket ham hock rump pig. Chuck kielbasa leberkas, pork bresaola ham hock filet mignon cow shoulder short ribs biltong.

### Used RAM

Bacon ipsum dolor sit amet t-bone doner shank drumstick, pork belly porchetta chuck sausage brisket ham hock rump pig. Chuck kielbasa leberkas, pork bresaola ham hock filet mignon cow shoulder short ribs biltong.



```
This is the final element on the page and there should be no margin below this.
```
