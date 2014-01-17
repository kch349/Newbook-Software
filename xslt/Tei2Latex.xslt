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
<!-- This was revised on 1-11-14.-->

<xsl:template match="/">
 \documentclass{book}

 \begin{document}
  <xsl:apply-templates />
 
 \end{document}
</xsl:template>

<xsl:template match="p" >
    <p>
 <xsl:value-of select="."/>
    <xsl:call-template name="StringReplace">
      <xsl:with-param name="text" select="." />
      <xsl:with-param name="chars" select="'&#038;aeiou'" />
    </xsl:call-template>
    </p>
</xsl:template>
<xsl:template match="body/div1/head">
	\chapter{<xsl:value-of select="."/>}
</xsl:template>

<xsl:template match="body/div1/div2/head">
	\section{<xsl:value-of select="."/>}
</xsl:template>

<xsl:template match="text/front/titlePage/titlePart" type="main">
	\title{<xsl:value-of select="."/>}
	\maketitle
</xsl:template>

<xsl:template match="date">
	\date{<xsl:value-of select="."/>}
</xsl:template>

<xsl:template match="text/front/titlePage/byLine">
	\author{<xsl:value-of select="."/>}
</xsl:template>

<tex:replace-map>
  <entry key="&lt;">\langle</entry>
  <entry key="&gt;">\rangle</entry>
  <entry key="&#038;">\&amp;</entry>
</tex:replace-map>

<xsl:template name="StringReplace">  
    <xsl:param name="text" />   
    <xsl:param name="chars" />

    <xsl:choose>
    <xsl:when test="string-length($chars) &gt; 0">
      <xsl:variable name="char" select="substring($chars,1,1)" />
      <xsl:choose>                         
          <xsl:when test="contains($text, $char)">  
             <xsl:variable name="nextString">                                      
                  <xsl:call-template name="StringReplace">                                       
                      <xsl:with-param name="text" select="substring-after($text, $char)" />
                      <xsl:with-param name="chars" select="$chars" />
                  </xsl:call-template>                                
              </xsl:variable>                                
              <xsl:variable name="onedown">
                <xsl:value-of select="concat(substring-before($text, $char), document('')/*/tex:replace-map/entry[@key=$char], $nextString)" />
              </xsl:variable>
              <xsl:call-template name="StringReplace">
                <xsl:with-param name="text" select="$onedown" />
                <xsl:with-param name="chars" select="substring($chars,2)" />
              </xsl:call-template>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$text" />
          </xsl:otherwise> 
      </xsl:choose>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$text" />
    </xsl:otherwise> 
    </xsl:choose>
</xsl:template> 


</xsl:stylesheet> 
