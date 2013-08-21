<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 
<xsl:output method="text" />
<xsl:strip-space elements="*"/>
<!--<xsl:key name="ptext-by-pb" match="/TEI/text/body/div//text()[ancestor::p]"
         use="generate-id(preceding::pb[1])"/>-->
<!--<xsl:key name="text-by-lb" match="/TEI/text/body/div//text()[not(ancestor::head[@type='margin'])]|//name|//ref|//time"
         use="generate-id(preceding::lb[1])"/>
<xsl:key name="pb-pairs" match="/TEI/text/body//pb"
         use="@n" />-->
<xsl:template match="/">\documentclass[12pt]{book}
\usepackage{fontspec}
%\setmainfont[
%BoldFont={Nimbus Roman No9 L Medium},
%ItalicFont={Nimbus Roman No9 L Regular Italic},
%Mapping=tex-text]{Doulos SIL}
\usepackage{xltxtra}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguage{arabic}
\newfontfamily\arabicfont[Script=Arabic,Scale=1.5]{Scheherazade}
%\setromanfont{Nimbus Roman No9 L}
\usepackage[T1]{fontenc}
\title{\textbf{\Large Journal of a Journey\\
1897}\\[.5cm] {\normalsize Auto-generated from the Ottoman Text Archive Project's\\[-.3cm] XML encoding of the Journal}}
\author{\textsc{Alexandre Svoboda} \\Nowf A. Allawi with Walter Andrews, Eds.}
\date{\today}
\begin{document}
  \frontmatter
  \maketitle
  \tableofcontents
  \pagebreak
  <xsl:apply-templates select="TEI/text/front" />
  \mainmatter
  <xsl:apply-templates select="/TEI/text/body//div[@type='chapter'][ancestor::div[substring(@xml:id,5,4)='engl']]" />
\end{document}
</xsl:template>

<xsl:template match="p">
    <xsl:apply-templates select="./*|text()"/>
     
%texcomment to create literal linebreaks in output
</xsl:template>

<xsl:template match="*[ancestor::div[@xml:id='frontnotes']]" />

<xsl:template match="head[ancestor::front][not(ancestor::div[@xml:id='frontnotes'])]">
\section*{<xsl:value-of select="."/>}
</xsl:template>
<xsl:template match="head[@type='chapter']">
\chapter{<xsl:value-of select="."/>}
</xsl:template>

<xsl:template match="head[@type='margin']">
\marginpar{<xsl:value-of select="."/>}
</xsl:template>

<xsl:template match="foreign[ancestor::front]">\begin{Arabic}<xsl:apply-templates />\end{Arabic}
</xsl:template>

<xsl:template match="quote[ancestor::front]">
\begin{quote}<xsl:apply-templates />\end{quote}
</xsl:template>

<xsl:template match="ref[ancestor::front]">
<xsl:variable name="t"><xsl:value-of select="substring(@target,2,5)"/></xsl:variable>
\footnote{<xsl:value-of select="/TEI/text/front//note[@xml:id=$t]"/>}</xsl:template>

<xsl:template match="list">
\begin{itemize}
  <xsl:apply-templates />
\end{itemize}</xsl:template>

<xsl:template match="item">
\item <xsl:apply-templates /></xsl:template>

<xsl:template match="text()">
  <xsl:variable name="amp" select="'&amp;'"/>
  <xsl:if test="normalize-space()">
    <xsl:choose>
    <xsl:when test="contains(.,$amp)">
      <xsl:variable name="text">
      <xsl:value-of select="substring-before(.,$amp)"/>\&amp;<xsl:value-of select="substring-after(.,$amp)"/></xsl:variable>
      <xsl:value-of select="concat(' ',normalize-space(translate($text,'_',' ')),' ')"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="concat(' ',normalize-space(translate(.,'~_','- ')),' ')"/>
    </xsl:otherwise>
    </xsl:choose></xsl:if>
</xsl:template>

</xsl:stylesheet>
