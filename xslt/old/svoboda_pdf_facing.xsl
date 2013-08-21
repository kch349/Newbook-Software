<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 
<xsl:output method="text" />
<xsl:strip-space elements="*"/>
<xsl:key name="text-by-pb" match="/TEI/text/body/div//lb"
         use="generate-id(preceding::pb[1])"/>
<xsl:key name="text-by-lb" match="/TEI/text/body/div//text()[not(ancestor::head[@type='margin'])]|//name|//ref|//time"
         use="generate-id(preceding::lb[1])"/>
<xsl:key name="pb-pairs" match="/TEI/text/body//pb"
         use="@n" />
<xsl:template match="/">\documentclass[9pt]{book}
\usepackage[left=2cm,right=2cm,top=2cm,bottom=2cm]{geometry}
\usepackage{fontspec}
\usepackage{xltxtra}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguage{arabic}
\newfontfamily\arabicfont[Script=Arabic,Scale=1.5]{Scheherazade}
\setromanfont{Nimbus Roman No9 L}
\usepackage[T1]{fontenc}
\title{Alexander Svoboda's Journal of Journey}
\begin{document}
  \maketitle
  \section{<xsl:value-of  
  \begin{center}\Large April\end{center}
  <xsl:apply-templates select="/TEI/text/body//pb">
    <xsl:sort data-type="number" select="@n"/>
  </xsl:apply-templates>
\end{document}
</xsl:template>

<xsl:template match="//pb">
<xsl:for-each select=".">
<xsl:choose>
  <xsl:when test="ancestor::div[substring(@xml:id,5,4)='arab']">\fbox{\begin{minipage}[t]{.5\textwidth}\begin{flushright} 
  \noindent
  \begin{center}\Large<xsl:value-of select="./@n"/>\end{center}
  \begin{Arabic}
  <xsl:for-each select="key('text-by-pb', generate-id())">
    <xsl:apply-templates select="."/>
  </xsl:for-each>
  \end{Arabic}\end{flushright}
  \end{minipage}}</xsl:when> <xsl:otherwise>\noindent \fbox{\begin{minipage}[t]{.5\textwidth}\begin{flushleft}\noindent
  \begin{center}\Large<xsl:value-of select="./@n"/>\end{center}<xsl:for-each select="key('text-by-pb', generate-id())"> <xsl:apply-templates select="."/>
  </xsl:for-each>\end{flushleft}\end{minipage}}\newpage
  </xsl:otherwise>
</xsl:choose>
</xsl:for-each>
</xsl:template>

<xsl:template match="lb">
  <xsl:variable name="pnum" select="preceding::pb[1]/@n"/>
  <xsl:variable name="lang" select="substring(ancestor::div[@type='month']/@xml:id,5,4)"/>
  <xsl:variable name="addy">
    <xsl:choose>
      <xsl:when test="$lang='engl'">
        <xsl:value-of select="concat('HE',$pnum,'-',@n)"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="concat('HA',$pnum,'-',@n)"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  \mbox{}\newline\fbox{\begin{minipage}[t]{2cm}
  \tiny{}[<xsl:value-of select="@n" />]
  <xsl:choose>
    <xsl:when test="//head/@xml:id=$addy">\scriptsize <xsl:value-of select="//head[@xml:id=$addy]"/></xsl:when>
    <xsl:otherwise>\hspace*{2cm}</xsl:otherwise>
  </xsl:choose>\end{minipage}}\fbox{\begin{minipage}[t]{(\textwidth)-3cm}\scriptsize <xsl:for-each select="key('text-by-lb', generate-id())"><xsl:apply-templates select="."/></xsl:for-each>\end{minipage}}
</xsl:template>


<!--<xsl:template match="name">NN<xsl:value-of select="concat(' ',.,' ')"/></xsl:template>

<xsl:template match="time">TT<xsl:value-of select="concat(' ',.,' ')"/></xsl:template>

<xsl:template match="ref">RR<xsl:value-of select="concat(' ',.)"/>\footnotemark <xsl:value-of select="/TEI/text/back//text()[ancestor::note[@xml:id=substring(current()/@target,1,6)]]"/> </xsl:template>-->

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
