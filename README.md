# Mammoth .docx to HTML converter

Mammoth is designed to convert .docx documents,
such as those created by Microsoft Word,
and convert them to HTML.
Mammoth aims to produce simple and clean HTML by using semantic information in the document,
and ignoring other details.
For instance,
Mammoth converts any paragraph with the style `Heading1` to `h1` elements,
rather than attempting to exactly copy the styling (font, text size, colour, etc.) of the heading.

There's a large mismatch between the structure used by .docx and the structure of HTML,
meaning that the conversion is unlikely to be perfect for more complicated documents.
Mammoth works best if you only use styles to semantically mark up your document.

## Installation

    pip install mammoth
    
## Usage

### CLI

You can convert docx files by passing the path to the docx file and the output file.
For instance:

    mammoth document.docx output.html

If no output file is specified, output is written to stdout instead.

#### Images

By default, images are included inline in the output HTML.
If an output directory is specified by `--output-dir`,
the images are written to separate files instead.
For instance:

    mammoth document.docx --output-dir=output-dir

Existing files will be overwritten if present.

#### Styles

A custom style map can be read from a file using `--style-map`.
For instance:

    mammoth document.docx output.html --style-map=custom-style-map
    
Where `custom-style-map` looks something like:

    p.AsideHeading => div.aside > h2:fresh
    p.AsideText => div.aside > p:fresh

### Library

#### Basic conversion

To convert an existing .docx file to HTML,
pass a file-like object to `mammoth.convert_to_html`.
The file should be opened in binary mode.
For instance:

```python
import mammoth

with open("document.docx", "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html = result.value # The generated HTML
    messages = result.messages # Any messages, such as warnings during conversion
```

### Custom style map

By default,
Mammoth maps some common .docx styles to HTML elements.
For instance,
a paragraph with the style `Heading1` is converted to a `h1` element.
You can pass in a custom style map using the `style_map` argument.
A description of the syntax for style maps can be found in the section "Writing style maps".
For instance, if paragraphs with the style `SectionTitle` should be converted to `h1` elements,
and paragraphs with the style `SubSectionTitle` should be converted to `h2` elements:

```python
import mammoth

style_map = """
p.SectionTitle => h1:fresh
p.SubSectionTitle => h2:fresh
"""

with open("document.docx", "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file, style_map=style_map)
```

User-defined style mappings are used in preference to the default style mappings.
To stop using the default style mappings altogether,
set pass `include_default_style_map=False`:

```python
    result = mammoth.convert_to_html(docx_file, style_map=style_map, include_default_style_map=False)
```
## Writing style maps

A style map is made up of a number of style mappings separated by new lines.

A style mapping has two parts:

* On the left, before the arrow, is the document element matcher.
* On the right, after the arrow, is the HTML path.

When converting each paragraph,
Mammoth finds the first style mapping where the document element matcher matches the current paragraph.
Mammoth then ensures the HTML path is satisfied.

### Freshness

When writing style mappings, it's helpful to understand Mammoth's notion of freshness.
When generating, Mammoth will only close an HTML element when necessary.
Otherwise, elements are reused.

For instance, suppose one of the specified style mappings is `p.Heading1 => h1`.
If Mammoth encounters a .docx paragraph with the style `Heading1`,
the .docx paragraph is converted to a `h1` element with the same text.
If the next .docx paragraph also has the style `Heading1`,
then the text of that paragraph will be appended to the *existing* `h1` element,
rather than creating a new `h1` element.

In most cases, you'll probably want to generate a new `h1` element instead.
You can specify this by using the `:fresh` modifier:

`p.Heading1 => h1:fresh`

The two consective `Heading1` .docx paragraphs will then be converted to two separate `h1` elements.

Reusing elements is useful in generating more complicated HTML structures.
For instance, suppose your .docx contains asides.
Each aside might have a heading and some body text,
which should be contained within a single `div.aside` element.
In this case, style mappings similar to `p.AsideHeading => div.aside > h2:fresh` and
`p.AsideText => div.aside > p:fresh` might be helpful.

### Document element matchers

#### Paragraphs and runs

Match any paragraph:

```
p
```

Match any run:

```
r
```

To match a paragraph or run with a specific style name,
append a dot followed by the style name.
For instance, to match a paragraph with the style `Heading1`:

```
p.Heading1
```

### HTML paths

#### Single elements

The simplest HTML path is to specify a single element.
For instance, to specify an `h1` element:

```
h1
```

To give an element a CSS class,
append a dot followed by the name of the class:

```
h1.section-title
```

To require that an element is fresh, use `:fresh`:

```
h1:fresh
```

Modifiers must be used in the correct order:

```
h1.section-title:fresh
```

#### Nested elements

Use `>` to specify nested elements.
For instance, to specify `h2` within `div.aside`:

```
div.aside > h2
```

You can nest elements to any depth.
