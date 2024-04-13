# py-ssgenerator

A markdown to HTML static site generator written in Python.
Comes with a basic server to visualize the rendered site.

## Motivation

Being a Markdown user  myself I found great interest in building my own parser and HTML generator.
A project I could regularly use and expand based on my needs.

### Goal

The idea is to keep a simple static site generator with added features that will eventually come, said features are:

- Improved parsing engine: that supports nested in-line blocks and better handles consecutive character delimiters without any spaces in between.
- Live preview: the addition of a live refresh feature to the server, re-rendering the site with every change to improve the writing workflow.
- Coming up with a better name

## Installation and Usage

In short, clone the repo, place your content on the corresponding *content* and *static* directories and run the main.sh script.
The project includes default content for demostration purposes, aswell as a HTML template and CSS stylesheet.
