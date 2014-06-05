<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
     xmlns:tex="placeholder.uri" exclude-result-prefixes="tex">
<xsl:output method="text" />

<!-- The name of this file is tei2LaTeX -->
<!-- This xslt script converts NDTH tei-xml to LaTeX -->
<!-- xsltproc -v -nonet input.xslt input.xml > output.tex -->
<!-- xsltproc -v -nonet input.xslt input.xml > output.tex 2>err -->
<!-- This command uses -v = verbose -nonet = no not use internet to fetch DTD, etc -->
<!-- This file was created and maintained by Aaron Gupta-->
<!-- Copyright 2013-2014 NDTH-UW. All Rights Reserved.-->
<!-- This was revised on 4-23-14.-->
<!-- added support for %,#,\,^,{,},~ -->
<!-- added support for pb, lb, verse , and l tags -->
<!-- 4/23/14 - added support for emph, ref, note,  fixed lg, l and lb-->
<!-- 5/1/14 - fixed string replace (hopefully) -->
<!-- 5/8/14 Fixed Cell template and escaping of \ -->
<!-- 5/14/14 Added support for [ and ] -->
<!-- 5/18/14 added recursion for notes and fixed repeating <l> and <lb> issue-->
<!-- 5/21/14 Fixed char replacement in ref environment-->
<!-- 5/22/14 changed pb template, prints out [p: #] rather then adding a new tag-->
<!-- 6/5/14 Working on Foreign Tag/ Picture grabbing templates. -->
<xsl:template match="/">

\documentclass{report}
<!--
\usepackage{arabtext}
\usepackage{utf8}
-->
\begin{document}

<!--\newcommand{\mnote}[1] {\marginpar{\scriptsize \raggedright #1 }} -->

<xsl:apply-templates select = "/TEI/text/body" />
 
 \end{document}

</xsl:template>

<!-- Prints div1 heads as a Chapter -->
<xsl:template match="div1/head">
	\chapter{<xsl:apply-templates />}
</xsl:template>

<!-- Prints div2 heads as a Section -->
<xsl:template match="div2/head">
	\section{<xsl:apply-templates />}
</xsl:template>

<!-- Prints out paragraphs -->
<xsl:template match="p">
	\par{
 	<xsl:apply-templates/>
	}
</xsl:template>

<!-- [[Figure-CAPTION =- [URL]]]
<xsl:template match="figure">\lbrack \lbrack </xsl:template>

<xsl:template match="figure/head"><xsl:apply-templates/>Caption:</xsl:template>

<xsl:template match="graphic"><xsl:value-of select="@url"/>\rbrack \rbrack </xsl:template>-->


<!--Adds linebreaks into document-->
<xsl:template match="lb">\ \\</xsl:template>


<xsl:template match="pb">
  \[p: <xsl:value-of select="@n"/> \]
</xsl:template>

<!-- adds page breaks into document 
<xsl:template match="pb">
	\pagebreak
</xsl:template>
-->
<!--adds linegroups into document using minipage 
<xsl:template match="lg">
	\par{	
		\framebox{
		\begin{minipage}[c]{\textwidth}
		<xsl:value-of select="."/>
		\end{minipage}
		}
	}
</xsl:template>
<foreign xml:lang="*-Latn", -Arab, -
<!--adds arabic environment that surrounds arabic text 
<xsl:template match="foreign">
	\begin{quote} <xsl:value-of select="."/> \end{quote}
</xsl:template> -->

<!-- inserts linegroup into document-->
<xsl:template match="lg">
	\begin{verse}
	<xsl:apply-templates/>
	\end{verse}
</xsl:template>

<!-- inserts a line within the linegroup into document -->
<xsl:template match="l">
	<xsl:apply-templates/>
</xsl:template>

<!--
<!-Prints margin notes with a smaller font, so they can fit in margin ->
 <xsl:template match= "note">
\mnote{<xsl:value-of select="."/> }
</xsl:template>
-->

<!-- Prints all Note tags as foot notes -->
<xsl:template match="note">
\footnote{<xsl:apply-templates/>}
</xsl:template>

<!--Prints lists with bullets -->
<xsl:template match= "list">
	\begin{itemize}
	<xsl:apply-templates/>
	\end{itemize}
</xsl:template>

<xsl:template match= "item">
	\item <xsl:value-of select="."/>
</xsl:template>

<xsl:template match="emph">
	\textit{<xsl:value-of select="."/>}
</xsl:template>

<xsl:template match="ref">
	\textsuperscript{<xsl:apply-templates />}
</xsl:template>

<!-- finish later, figure out how to grab url value 
<xsl:template match="figure">
	\begin{figure}
	<xsl:apply-templates/>
	\end{figure}
</xsl:template>

<xsl:template match="head">
	\caption{<xsl:value-of select="."/>}
}

-->

<xsl:template match="table">
	\begin{tabular}{c|c|c|c}
	<xsl:apply-templates/>
	\end{tabular}
</xsl:template>

<xsl:template match="row">
	<xsl:apply-templates/>
	\\
</xsl:template>

<xsl:template match="cell">
	<xsl:apply-templates/>
	<!--<xsl:value-of select='normalize-space()'/>-->
	&amp;
</xsl:template>


<tex:replace-map>
  <entry key="&gt;">$\rangle$</entry>
  <entry key="&lt;">$\langle$</entry> 
  <entry key="&amp;">\&amp;</entry>
  <entry key="_">\_</entry>
  <entry key="%">\%</entry>
  <entry key="#">\#</entry>
  <entry key="$">\$</entry>
  <entry key="\">\textbackslash{}</entry>
  <entry key="^">\^{}</entry>
  <entry key="{">\{</entry>
  <entry key="}">\}</entry>
  <entry key="~">\~{}</entry>
  <entry key="[">\lbrack </entry>
  <entry key="]">\rbrack </entry>

</tex:replace-map>

<xsl:template match = "text()" >
    <xsl:variable name="toreturn">
      <xsl:call-template name="StringReplace">
        <xsl:with-param name="text" select="." />
        <xsl:with-param name="chars" select="'&lt; &amp; % # $ \ * ^ { ~ } _ &gt; ] [ '" />
		<!-- % has to be added anywhere but the end or some cases dont get escaped -->
      </xsl:call-template>
    </xsl:variable>
    <xsl:value-of select="normalize-space($toreturn)" />
</xsl:template>


 
<xsl:template name="StringReplace">  
  <xsl:param name="text" />   
  <xsl:param name="chars" />

  <xsl:choose>
    <!-- when $chars still has spaces, we're not done replacing stuff -->
    <xsl:when test="contains($chars, ' ')">
      <!-- compute the current char to work on, it's the first one in $chars
           * chars is delimited by spaces -->
      <xsl:variable name="char" select="substring-before($chars,' ')" />

      <xsl:choose>                         
          <xsl:when test="contains($text, $char)">  
             <!-- the text contains the character to replace
                  * first compute the next string to call on 
                  * this is all the text after the first intance of the char to replace 
                  **** 
                  * recursively call this template on that text, will do replacement
                  * as we come back up from recursion-->
             <xsl:variable name="rightString">                                      
                  <xsl:call-template name="StringReplace">                                       
                      <xsl:with-param name="text" select="substring-after($text, $char)" />
                      <xsl:with-param name="chars" select="$chars" />
                  </xsl:call-template>                                
              </xsl:variable>     
                           
             <xsl:variable name="leftString">                                      
                  <xsl:call-template name="StringReplace">                                       
                      <xsl:with-param name="text" select="substring-before($text, $char)" />
                      <xsl:with-param name="chars" select="$chars" />
                  </xsl:call-template>                                
              </xsl:variable>     

              <!--  $rejoined contains the text to the left, the replacement char, and the reply from recursion -->
              <xsl:variable name="rejoined">
                <xsl:value-of select="concat($leftString, document('')/*/tex:replace-map/entry[@key=$char], $rightString)" />
              </xsl:variable>

              <!-- no more instances of the char to be replaced in $text, return the text to start
                   coming back from recursion --> 
              <xsl:value-of select="$rejoined" />
          </xsl:when>
          <xsl:otherwise>
              <!-- done with the current $char, shorten $chars and run again--> 
              <xsl:call-template name="StringReplace">
                <xsl:with-param name="text" select="$text" />
                <xsl:with-param name="chars" select="substring-after($chars,' ')" />
              </xsl:call-template>
          </xsl:otherwise> 
        </xsl:choose>
    </xsl:when>

    <xsl:otherwise>
      <!-- $chars is completely empty, we are done -->
      <xsl:value-of select="$text" />
    </xsl:otherwise>
  </xsl:choose>
</xsl:template> 
</xsl:stylesheet>

