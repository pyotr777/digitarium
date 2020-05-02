---
id: 191
title: 'Bash: Expanding variables and commands in text'
date: 2015-10-15T11:54:19+09:00
author: Peter Bryzgalov
layout: post
guid: http://comp.photo777.org/?p=191
permalink: /bash-expanding-variables-in-text/
categories:
  - public
tags:
  - bash
  - expand variables
---
Say you have a text file with variables or commands in it:

<pre class="top-set:false top-margin:0 highlight:0 decode:true bottom-margin:15 show-title:false ranges:false nums:false nums-toggle:false">Today is $(date).
I have $n things to do.</pre>

Store text file contents in a variable and expand variables and commands in the text with:

<pre class="top-set:false top-margin:0 bottom-set:false bottom-margin:15 show-title:false ranges:false nums:false nums-toggle:false wrap-toggle:false lang:sh decode:true "># Init variables
n=25
# Store file in a variable
text="$(echo EOF;cat $filename;echo EOF)"
# Expand text (and print it to stdout)
eval "cat &lt;&lt;$text"</pre>

That&#8217;s it! You will see something like:

<pre class="top-set:false top-margin:0 highlight:0 decode:true bottom-margin:15 show-title:false ranges:false nums:false nums-toggle:false">Today is Thu Oct 15 12:04:56 JST 2015.
You have 25 things to do.</pre>

Note, that without <span class="lang:default decode:true crayon-inline">echo EOF</span> bash will use first line of text as a limit string for <a href="http://tldp.org/LDP/abs/html/here-docs.html" target="_blank">heredoc</a>.