<?xml version="1.0"?>

<xsl:stylesheet href="products.xml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:template match="/">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
  </head>
  <html>
  <body>
    <h2>Products</h2>
    <table border="1">
      <tr bgcolor="ffff24">
        <th>Product</th>
        <th>Price</th>
        <th>Image</th>
      </tr>
      <xsl:for-each select="root/product">
        <tr>
          <td><xsl:value-of select="name"/></td>
          <td><xsl:value-of select="price"/></td>
          <td>
              <img>
              <xsl:attribute name="src">
                  <xsl:value-of select="img"/>
              </xsl:attribute>
            </img>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>