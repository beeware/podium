# Podium reference

The following is a list of all the features that a Podium slide deck can contain, as well as the controls for managing the presentation of a deck.

## Slides and speaker notes

Your slide content is contained within a `slides.md` file, which requires some specific formatting to render as separate slides.

Each slide and associated speaker notes are separated from the next with three dashes (`---`). The speaker notes are separated from the slide content by three question marks (`???`).

A simple slide with speaker notes would be formatted as follows:

```markdown
# Slide title

???

Welcome to my talk.

---
```

![A simple slide in the speaker view in Podium.](../images/simple_slide.png)

Speaker notes will render Markdown syntax, and can span multiple lines and include separate paragraphs.

This basic format applies regardless of what syntax you include in the slide content.

You can also attach annotations in the form of classes. For example, centering the title and author on a title slide would include the following:

```markdown
class: title

# Talk title

## Author name
```

![A title slide in Podium.](../images/title_slide_class.png)

Other possible class annotations will be mentioned alongside the relevant content below.

### Incremental content builds

You can introduce one element at a time on your slides with incremental content builds. For example, introducing a series of basic bullets one at a time is formatted as follows:

```markdown
# Incremental presentation

* Introduce
--

* one
--

* bullet
--

* point
--

* at
--

* a
--

* time
```

![An incremental bullet list build in Podium.](../images/incremental_basic.gif)

Your speaker notes must be included throughout the slide to show up at the same time as each bullet. They will not show up until the end if you put them at the end. For example, displaying your speaker notes alongside each bullet is formatted as follows:

```markdown
# Incremental presentation

* First bullet

???

First bullet notes.

--

* Second bullet

???

Second bullet notes.

--

* Third bullet

???

Third bullet notes.
```

![An incremental bullet list build with speaker notes in Podium.](../images/incremental_speaker_notes.gif)

### Style customization

You'll find the default `style.css` stylesheet within the Podium slide deck bundle. You can modify it to apply style overrides to your slides.

There are three primary classes available for overriding CSS: `.remark-slides-area`, `.remark-preview-area`, and `.remark-notes-area`. `.remark-slides-area` applies to the full slide-view window, and to the current slide section in the presenter window, which is located at the top-left. `.remark-preview-area` applies to the next slide preview in the presenter window, which is located at the lower-left. `.remark-notes-area` applies to the speaker notes section in the presenter window, which is located on the right.

![The slide-view window with the CSS divs identified.](../images/slides_area.png)

![The presenter-view window with the CSS divs identified.](../images/preview_area.png)

Within `.remark-slides-area` and `.remark-preview-area`, `.remark-slide-content` applies to all slide content. Any styling applied to `.remark-slide-content` alone will apply to *both* the slides area and the preview area. If you wish to target only one, you need to specify which parent you are targeting.

You can attach an arbitrary CSS class to a specific slide, and then anything you want to put into the `style.css` override, using that class, will get picked up and used on the associated slides.

For example, you might want to color the text on a slide red. You could add `red-text` to the top of a slide as follows:

```markdown
class: red-text

Info on this slide
```

Then, in the `style.css`, you would add the following:

```css
.remark-slide-content .red-text {
    color: red;
}
```

You can apply multiple classes to a single slide. If you wanted to change the color of the text on your title slide, you could add `red-text` to the top of the title slide as follows:

```markdown
class: title red-text

# Title Slide
```

The `title` class is built into Podium. The same `red-text` element in `style.css` would apply to this slide as well.

The default `style.css` file within the `example.podium` bundle contains the necessary CSS to modify the watermark. The [Customizing the "Made with Podium" watermark guide](../how-to/watermark.md) explains how.

## Markdown syntax

Basic Markdown is supported.

### Basic formatting

Text formatting includes *italics* (`*italics*`), **bold** (`**bold**`), ***bold italics*** (`***bold italics***`), and ~~strikethrough~~ (`~~strikethrough~~`). You can include links, such as `[BeeWare](https://beeware.org)`, which renders as [BeeWare](https://beeware.org).

### Title slide

A basic title slide consists of a centered title and an author name. It requires `title` class annotation. It is formatted as follows:

```markdown
class: title

# Talk title
## Author name
```

![A title slide in Podium.](../images/title_slide_class.png)

You can extend titles to multiple lines, and include multiple authors, formatted as follows:

```markdown
class: title

# A very long title
# made up of multiple
# lines of text
## First Author name
## Second Author name
## Third Author name
```

![A title slide with a longer title and multiple authors in Podium.](../images/multi_title_slide.png)

### Reverse color slide

You can make a point stand out by using a title slide with a `reverse` annotation, formatted as follows:

```markdown
class: title reverse

# Point of emphasis
```

![A reverse, point of emphasis title slide in Podium.](../images/reverse.png)

### Bullet and number slides

There are multiple ways to display content listed on a slide.

Bullets are denoted by a dash (`-`), asterisk (`*`), or plus sign (`+`) at the beginning of a line. You can indent one or more items to create a nested list.

#### Basic bullets

A slide with a simple bullet list would be formatted as follows:

```markdown
# Simple bullets

* Introduction
* Deep-dive
* Deep-dive
```

![A slide with a bullet list in Podium.](../images/basic_bullets.png)

A slide with a nested bullet list could be formatted as follows:

```markdown
# Nested bullets

* Introduction
    * Subpoint
    * Subpoint
* Deep-dive
    * Subpoint
    * Subpoint
        * Subpoint
* Deep-dive
```

![A slide with a nested bullet list in Podium.](../images/nested_bullets.png)

Markdown allows for mixing bullet notation in nested bullet lists, but each nested level *must* be consistent, as shown above.

#### Numbered lists

A slide with a numbered list would be formatted as follows:

```markdown
# Numbered list

1. Introduction
   1. Subpoint
   2. Subpoint
      1. Subpoint
      2. Subpoint
2. Deep-dive
3. Deep-dive
```

![A slide with a numbered list in Podium.](../images/numbered_list.png)

### Images

You can display images on slides using standard Markdown.

Images are formatted as follows:

```markdown
![Image alt text](path/to/image.png)
```

#### Basic images with a caption

You can include a footnote as a caption. The following would show an image of a kitten with the link to the original as a caption:

```markdown
![A red kitten](kitten.png)

.footnotes[ commons.wikimedia.org/wiki/File:Red_Kitten_01.jpg ]
```

![A slide showing an image of a kitten with a footnote caption.](../images/image_kitten.png)

#### Screenshots

You can display a screenshot with a caption, formatted as follows:

```markdown
class: screenshot

![A Fahrenheit to Celsius converter app](screenshot.png)

# A screenshot
```

![A slide showing a screenshot of an app in Podium.](../images/screenshot_slide.png)

This centers the image, and makes space for the caption.

#### Logos

You can display a logo, formatted as follows:

```markdown
class: logo

![The BeeWare logo](beeware.png)
```

![A slide showing the BeeWare logo in Podium.](../images/logo.png)

This emphasizes, and vertically centers the image.

### Columns

You can display a slide with content in two columns.

For example, two bullet lists displayed side by side would be formatted as follows:

```markdown
# Two lists

.left-column[

* Introduction with some very long text indeed
* Deep-dive
* Deep-dive

]

.right-column[

* Introduction with some very long text indeed
* Deep-dive
* Deep-dive

]
```

![A slide with two bullet lists displayed side by side in Podium.](../images/two_lists.png)

Two images displayed side by side would be formatted as follows:

```markdown
# Two images

.left-column[

![A red kitten](../images/kitten.png)

]

.right-column[

![A Fahrenheit to Celsius converter app](../images/screenshot.png)

]
```

![A slide with two images displayed side by side in Podium.](../images/two_images.png)

Any valid Markdown can be displayed in either column.

### Quotations

You can display quotations and attribution, formatted as follows:

<!-- rumdl-disable MD013 -->

```markdown
# Quotation

> One thing was certain, that the white kitten had had nothing
> to do with it -- it was the black kitten's fault entirely. For
> the white kitten had been having its face washed by the old cat,
> for the last quarter of an hour (and bearing it pretty well,
> considering) so you see that it couldn't have had any hand in
> the mischief.

<cite>Lewis Carroll, Through the Looking Glass</cite>
```

<!-- rumdl-enable MD013 -->

![A slide with a quotation and attribution in Podium.](../images/quotation.png)

Quotations can also be included as bulleted content, formatted as follows:

```markdown
# Other inline content

* A quote in a bullet

    > To be, or not to be

    <cite>William Shakespeare</cite>
```

![A slide with a quotation and attribution in a bullet list in Podium.](../images/quotation_bullet.png)

### Code

Inline code and codeblocks are supported.

Inline code is surrounded by single backticks. The following would render as a bullet with the word "inline" in code formatting.

```markdown
* A bullet with `inline` code formatting.
```

You can include codeblocks both at the top level and in bullet lists. Codeblocks are denoted by three backticks on the lines before and after the code, with the first line including the language being rendered.

To include a Python codeblock at the top level, you could include the following in your `slides.md`:

````markdown
```python
def greeting(arg):
    if arg == 'hello':
        print('Hello World')
    else:
        print(arg)


class Something():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
```
````

![A code snippet on a slide in Podium.](../images/code.png)

To include a Python codeblock in a bullet list, you could include the following:

````markdown
* Code in a bullet:

    ```python
    def greeting(arg):
      if arg == 'hello':
          print('Hello World')
    ```
````

![A code snippet in a bullet on a slide in Podium.](../images/code_bullet.png)

### Footnotes

You can include footnotes in your slides, formatted as follows:

```markdown
# Footnotes

* First thing.dag1[]

* Second thing.dag2[]

* Third thing.dag3[]

* Last thing.dag4[]

.footnotes[

.dag1[] This isn't exactly what it sounds like. You need to consider this very carefully. And I mean _really_ carefully

.dag2[] Second dagger

.dag3[] Third dagger

.dag4[] Fourth dagger

]
```

![A slide with footnotes in Podium.](../images/footnotes.png)

### Animated transitions

Podium supports a number of animated transitions.

Animated slides require the following class annotation, followed by the content:

```markdown
class: animated animationName

Content here.
```

Incoming transitions include:

- `shake` - Shakes content back and forth, left to right.
- `tada` - Zooms out slightly, and twists content back and forth.
- `swing` - Swings content left to right, like a pendulum connected from the top.
- `wobble` - Wobbles content left to right, like a pendulum connected from the bottom.
- `pulse` - Zooms in and out once.
- `flash` - Flashes between the current slide content and the previous slide content.
- `bounce` - Bounces content up and down.
- `bounceIn` - Bounces content back to front.
- `bounceInUp` - Bounces content up from the bottom of the slide.
- `bounceInDown` - Bounces content down from the top of the slide.
- `bounceInLeft` - Bounces content in from the left of the slide.
- `bounceInRight` - Bounces content in from the right of the slide.
- `flip` - Flips the content twice around a vertical axis.
- `flipInX` - Flips the content once around the x-axis, from top to bottom.
- `flipInY` - Flips the content once around the y-axis, from left to right.
- `fadeIn` - Fades previous slide content out and current slide content in.
- `fadeInUp` - Fades the current content up from the bottom of the slide.
- `fadeInDown` - Fades the current content down from the top of the slide.
- `fadeInLeft` - Fades the current content in from the left of the slide.
- `fadeInRight` - Fades the current content in from the right of the slide.
- `rotateIn` - Content begins upside down, and rotates around the z-axis from left to right, to become upright.
- `rotateInUpLeft` - Rotates content onto the slide from the bottom, as though attached to the bottom left corner.
- `rotateInDownLeft` - Rotates content onto the slide from the top, as though attached to the top left corner.
- `rotateInUpRight` - Rotates content onto the slide from the bottom, as though attached to the bottom right corner.
- `rotateInDownRight` - Rotates content onto the slide from the bottom, as though attached to the top right corner.
- `rollIn` - Rolls content in from the left of the slide.
- `lightSpeedIn` - Moves content quickly onto the slide, with momentum, from the right of the slide.

## Keyboard shortcuts

- CMD+Shift+P - Enter presentation mode; or, if in presentation mode, pause timer
- CMD+P - Open presentation in Print view
- CMD+Q - Quit Podium (exit presentation mode)
- CMD+Tab - Switch displays
- Right/Left arrows - Next/previous slide
- Home/End - first/last slide
- CMD+A - Switch aspect ratio between 16:9 and 4:3
- CMD+R - Reload slide deck
- CMD+T - Reset timer
