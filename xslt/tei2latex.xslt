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
<!-- This was revised on 3-7-14.-->

<xsl:template match="/">

\documentclass{report}

\begin{document}

\newcommand{\mnote}[1] {\marginpar{\scriptsize \raggedright #1 }}

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
<xsl:template match="p" >
 	\par{
 	<xsl:apply-templates/>
	}
</xsl:template>

<!-- Prints margin notes with a smaller font, so they can fit in margin -->
 <xsl:template match= "note">
\mnote{<xsl:value-of select="."/> }

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


<tex:replace-map>
  <entry key="&lt;">$\langle$</entry>
  <entry key="&gt;">$\rangle$</entry>
  <entry key="&amp;">\&amp;</entry>
  <entry key="_">\_</entry>
  <entry key="%">\%</entry>

</tex:replace-map>
<!-- new lines ? -->
<!-- template for lb tag -->


<xsl:template match = "text()" >
    <xsl:variable name="toreturn">
      <xsl:call-template name="StringReplace">
        <xsl:with-param name="text" select="." />
        <xsl:with-param name="chars" select="'&lt; &gt; % &amp; _ '" />
		<!--  % has to be in middle or it doesnt work -->
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
             <xsl:variable name="nextString">                                      
                  <xsl:call-template name="StringReplace">                                       
                      <xsl:with-param name="text" select="substring-after($text, $char)" />
                      <xsl:with-param name="chars" select="$chars" />
                  </xsl:call-template>                                
              </xsl:variable>                                

              <!--  $rejoined contains the text to the left, the replacement char, and the reply from recursion -->
              <xsl:variable name="rejoined">
                <xsl:value-of select="concat(substring-before($text, $char), document('')/*/tex:replace-map/entry[@key=$char], $nextString)" />
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
