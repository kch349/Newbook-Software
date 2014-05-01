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
<!--xsltproc -v -nonet try2safety.xsl proc_03.xml >proc_03.html-->



<xsl:template match="/">
	<html>
	<head>
		<title>New Book Digital Texts xsl 2.1.14</title>
	</head>	
	
	<body><xsl:apply-templates select="//body" /></body>
     </html>
</xsl:template>


<xsl:template match="body">
	<html>	
<xsl:apply-templates/>
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
   	<figure>
	<img src="temple.jpg" alt="An Old Temple" width="304" height="288" />
<!--Note:size configured, but not necessary -->
		<xsl:apply-templates/>
	
	</figure>
</xsl:template>

<xsl:template match="table">
	<table border="1">
		<tr>
		  <th>Arrive</th>
		  <th>Depart</th>	
		</tr>
		<tr>
		  <td>some time</td>
		  <td>some other time</td>
		</tr>
<xsl:apply-templates/>
	</table>
</xsl:template>


<xsl:template match="pb">
	<hr />
	<span class="pb">
[pg: <xsl:value-of select="@n"/>]
	</span>
</xsl:template>
	

<xsl:template match="lb"> 

	<span class="lb">
<!--line--> <xsl:value-of select="@n"/><!--:-->
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
