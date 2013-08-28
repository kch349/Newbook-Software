<?xml version="1.0" encoding="utf-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" doctype-system="about:legacy-compat" />

  <xsl:template match="/">
  <html>
  <head>
  <meta charset="utf-8" />
  <style type="text/css">
    body { width:800px; margin:auto; }
  </style>
  </head>
  <body>
  <h2>Diary</h2>
  <xsl:apply-templates />
  </body>
  </html>
  </xsl:template>

  <xsl:template match="teiHeader"/>

  <xsl:template match="div1">
    <xsl:for-each select="head">
      <h3><xsl:value-of select="." /></h3>
    </xsl:for-each>
    <xsl:apply-templates select="div2" />
  </xsl:template>

  <xsl:template match="div2">
    <xsl:for-each select="head">
      <h4><xsl:value-of select="." /></h4>
    </xsl:for-each>
    <xsl:apply-templates select="p" />
  </xsl:template>



  <xsl:template match="p" >
    <p>
    <xsl:apply-templates />
    </p>
  </xsl:template>

  <xsl:template match="pb">
    <h5>[page <xsl:value-of select="@n" />]</h5>
  </xsl:template>

</xsl:stylesheet> 
