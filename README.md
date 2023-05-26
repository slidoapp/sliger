# `sliger`

<p align="center">
  <img src="https://raw.githubusercontent.com/slidoapp/sliger/main/static/images/sliger-black.png" /> <br />
  <strong>Slide of the tiger</strong> <br />
  <em>Slide the power of Python (and Jinja2) into Google Slides</em>
</p>


<p align="center">

  ![PyPI](https://img.shields.io/pypi/v/sliger)
  ![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-green.svg)
  <a href="https://pycqa.github.io/isort/"><img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" /></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>
  [![Scc Count Badge](https://sloc.xyz/github/slidoapp/sliger/)](https://github.com/slidoapp/sliger/)
  [![Scc Count Badge](https://sloc.xyz/github/slidoapp/sliger/?category=cocomo)](https://github.com/slidoapp/sliger/)

</p>


## Install

    pip install sliger

## Prerequisites

To use `sliger` with a specific Google Slides presentation, the following is necessary:

1. Keys to a GCP Service Account (a `.json` file)
2. The presentation needs to be shared with the email that can be found in 1.

## Usage

In general, `sliger` needs two pieces of information in order for it to
do any automation on a specific Google Slides presentation:

1. The credentials file (the first point in the previous section)
2. The Presentation ID (assuming the presentation can be found at https://docs.google.com/presentation/d/1ijjVtlf9Jq1Rr0xTOMZWcSAUbfl6oA1aaBickwpUdGQ/edit the presentation ID would be `1ijjVtlf9Jq1Rr0xTOMZWcSAUbfl6oA1aaBickwpUdGQ`)

There are quite a few commands that the `sliger` supports:

### `duplicate-presentation`

To duplicate a specific presentation (in this case the presentation with the ID `1ijjVtlf9Jq1Rr0xTOMZWcSAUbfl6oA1aaBickwpUdGQ`) to a new one with a specific name (in this case `'A new presentation test'`), one could run the following command:

    sliger --creds-file mrshu-gslidesexperiments-7cd84ace2933.json --presentation-id 1ijjVtlf9Jq1Rr0xTOMZWcSAUbfl6oA1aaBickwpUdGQ duplicate-presentation --copy-title 'A new presentation test' 

### `delete-slide`

To delete slide number 3, one can run the following:

    sliger --creds-file mrshu-gslidesexperiments-7cd84ace2933.json --presentation-id 1ijjVtlf9Jq1Rr0xTOMZWcSAUbfl6oA1aaBickwpUdGQ delete-slide --id 3

### `duplicate-slide`

To duplicate slide number 3, one can run the following:

    sliger --creds-file mrshu-gslidesexperiments-7cd84ace2933.json --presentation-id 1ijjVtlf9Jq1Rr0xTOMZWcSAUbfl6oA1aaBickwpUdGQ duplicate-slide --id 3

### `jinjify`

`sliger` also supports [Jinja Templates](https://jinja.palletsprojects.com/en/3.1.x/).

It also provides a few custom functions, such as
[`strftime`](https://strftime.org/) which can be used to format dates. For instance the string 

```
Hi! Today is {{ strftime("%A, %O %B", now) }}
```

Would get rendered to

```
Hi! Today is Friday, 2nd September

```

Jinjify is also able to render Python functions. Once added the function to `collector.py` and to the variable `func_dict`, `jinjify` will parse the Python output in plain text.
For instance the string:

```
{{ greet_pycon() }}
```
Would get render to

```
Hi PyCon Italy! This string is generated from a Python function.
```

To render the template directly inside a specific presentation, you can run

    sliger --creds-file mrshu-gslidesexperiments-7cd84ace2933.json --presentation-id 1ijjVtlf9Jq1Rr0xTOMZWcSAUbfl6oA1aaBickwpUdGQ jinjify

Note that for the apostrophes to be picked up correctly, you will need to turn off the **Use smart quotes** option in **Tools -> Preferences**, as described in the [community docs](https://support.google.com/docs/thread/82024200/the-formatting-on-apostrophes-changes-everytime-i-use-the-grammar-spell-check?hl=en).


### `imagify`

Looks for text elements whose content is in the following format:

```
![image](<IMAGE_PATH>)
```

It then replaces the found text elements with image elements containing the images found at 
`IMAGE_PATH`. The image needs to be present locally. The `IMAGE_PATH` can be templated with 
Jinja. The used Jinja function should return the path to a locally present image that should be 
uploaded.

For example the following text placeholder will call the `generate_image` Jinja function which 
should create an image on the disk and return the path to the image. 

```
![image]({{ generate_image }})
```

To replace the placeholders with actual images in the presentation, one can run:

    sliger --creds-file mrshu-gslidesexperiments-7cd84ace2933.json --presentation-id 1ijjVtlf9Jq1Rr0xTOMZWcSAUbfl6oA1aaBickwpUdGQ imagify
