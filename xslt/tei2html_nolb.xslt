<?xml version="1.0" encoding="utf-8"?>

<xsl:stylesheet version="1.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">


<xsl:output method="html" />
<!--1/23/14: added paragraph tag-->
<!--1/23/14: added h1 tag-->
<!--1/26/14: added italics template-->
<!--2/4/14: added "stanza" div-class with line breaks -->
<!--2/4/14: added "figure" element -->
<!--2/14/12: added span-class hb instruction (numbered page breaks)-->
<!--2/17/12: added span-class lb instruction (numbered line breaks)-->
<!--5/15/14: edited "pb" removed "hb" (hard break) instruction -->
<!--5/15/14: added html doctype declarion; validated at w3schools -->
<!--5/15/14: edited "table" instruction to confrom to html5-->
<!--xsltproc -v -nonet try2safety.xsl proc_03.xml >proc_03.html-->

<xsl:template match="/">
<xsl:text disable-output-escaping="yes">&lt;</xsl:text>!DOCTYPE html<xsl:text disable-output-escaping="yes">&gt;</xsl:text>

	<html>
	<head>
		<title>New Book Digital Texts xsl 2.1.14</title>
	</head>	
	
	<body><xsl:apply-templates select="//body" /></body>
     </html>
</xsl:template>

<xsl:template match="list">
	<ul>
		<xsl:apply-templates/>
	</ul>
</xsl:template>


<xsl:template match="item">
	<li>
		<xsl:apply-templates/>
	</li>
</xsl:template>


		
<xsl:template match="p">
	<p>
	   <xsl:apply-templates/>
	</p>
</xsl:template>


<xsl:template match="div1/head">
	<h1>
	   <xsl:apply-templates/>
	</h1>
</xsl:template>

<xsl:template match="div2/head">
	<h2>
	<xsl:apply-templates/>
	</h2>
</xsl:template>


<xsl:template match="emph">
	<i>
	   <xsl:apply-templates/>
	</i>
</xsl:template>


<xsl:template match="lg">
	<p class="stanza">
		<xsl:apply-templates/>
	</p>
</xsl:template>



<xsl:template match="figure">
   	
	<img src="temple.jpg" alt="An Old Temple" width="304" height="288" />
<!--Note:size configured, but not necessary -->
		<xsl:apply-templates/>
</xsl:template>

<xsl:template match="table">
	<table style="border:1px solid black;">
	<xsl:for-each select="./row">
		<tr>
		  	<xsl:for-each select="./cell">
		<td style="border:1px solid black;"><xsl:value-of select="."/></td>
			</xsl:for-each>	
		</tr>
	</xsl:for-each>
	</table>
</xsl:template>


<xsl:template match="pb">
	<span class="pb">
[pg: <xsl:value-of select="@n"/>]
	</span>
</xsl:template>
	

<xsl:template match="lb"> 

	<span class="lb">
<!--This instruction is distinct from tei2html_lb. It creates a span-class for lines and their unique numbers, but this is not represented in the output-->
	</span>
</xsl:template>




<xsl:template match="foreign">
	<em>
	   <xsl:apply-templates/>
	</em>
</xsl:template>

<xsl:template match="name">
	<xsl:element name="span">
	   <xsl:attribute name="class">
	<xsl:value-of select="@type"/>
	   </xsl:attribute>
	<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
	
<xsl:template match="note">
		<xsl:element name="span">
		<xsl:attribute name="class">
	<xsl:value-of select="@xml:id"/>
		</xsl:attribute>
	<xsl:apply-templates/>
		</xsl:element>
</xsl:template>



</xsl:stylesheet>
