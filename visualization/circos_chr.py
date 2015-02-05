import os;

class circos_chr:
  chrs        = [];
  outdir      = "./";
  name        = "";
  karyotypes  = [];
  clust_links = [];
  text_prots  = [];
  gene_tiles  = [];
  exon_tiles  = [];

  chromosomes_units = 1;
  max_links_number  = 712173;

  def __init__(self, files, chrs, chr_scale, outdir, name):
    self.chrs        = chrs;
    self.chr_scale   = chr_scale;
    self.karyotypes  = files['karyotype'];
    self.clust_links = files['clusts'];
    self.text_prots  = files['genes']['text'];
    self.gene_tiles  = files['genes']['data'];
    self.exon_tiles  = files['exons'];
    self.outdir      = outdir;
    self.name        = name;

    for dir in [ '%s/%s' % (self.outdir, dir) for dir in [ 'data' ]]:
      try:
        os.makedirs(dir);
      except Exception:
        continue;
    #efor

    self.make_circos(outdir);
  #edef

  #############################################################################

  TXT_circos_conf = """
# circos conf
# Automatically generated by proteny tool
# https://github.com/thiesgehrmann/proteny

karyotype = %s

chromosomes_units           = %d
chromosomes_display_default = no
chromosomes                 = %s
%s

#<<include etc/chr_ideogram.conf>>
%s

#<<include etc/chr_links.conf>>
%s

#<<include etc/chr_plots.conf>>
%s

################################################################
# The remaining content is standard and required. It is imported 
# from default files in the Circos distribution.
#
# These should be present in every Circos configuration file and
# overridden as required. To see the content of these files, 
# look in etc/ in the Circos distribution.

<image>
# Included from Circos distribution.
<<include etc/image.conf>>
</image>

# RGB/HSV color definitions, color lists, location of fonts, fill patterns.
# Included from Circos distribution.
<<include etc/colors_fonts_patterns.conf>>
<<include etc/colors.conf>>

# Debugging, I/O an dother system parameters
# Included from Circos distribution.
<<include etc/housekeeping.conf>>
"""

  TXT_ideogram_conf = """
<ideogram>

  <spacing>
    default = 0.01r
  </spacing>

  radius    = 0.90r
  thickness = 20p
  fill      = yes

  show_label       = yes
  label_font       = default
  label_radius     = dims(image,radius) - 90p
  label_size       = 30
  label_rotate     = no

  label_parallel   = yes

</ideogram>
"""

  TXT_gene_plot = """
  <plot>
    file = %s
    type        = tile
    r1          = 1r
    r0          = 0.92r
    orientation = out
    
    layers      = 1
    margin      = 0.02u
    thickness   = 20
    padding     = 0
    
    layers_overflow=collapse
    stroke_thickness = 1
    <rules>
      <rule>
        condition    = var(strand) eq "n"
        stroke_color = red
        color        = red
      </rule>
      <rule>
        condition    = var(strand) eq "p"
        stroke_color = blue
        color        = blue
      </rule>
    </rules>
  </plot>
"""

  TXT_links_conf = """
    radius        = 0.92r
    bezier_radius = 0r
    thickness     = 2
    ribbon        = yes
    stroke_color     = vdgrey_a4
    stroke_thickness = 1
    
    <rules>
      flow = continue
      <rule>
        condition = 1
        #color     = eval(sprintf("hsv(%d,%f,%f)", var(h), 1.0, 1.0 ))
        color     = eval(sprintf("%d,%d,%d,0.5", var(r_int), var(g_int), var(b_int)))
        z         = eval( 99999999999999999 - min(var(SIZE1),var(SIZE2)) )
        #flat     = yes
      </rule>
    </rules>
"""

  #############################################################################

  def make_circos(self, outdir):
    i_d = self.make_ideogram(outdir);
    l_d  = self.make_links(outdir);
    p_d  = self.make_plots(outdir);

    self.make_conf(outdir, i_d, l_d, p_d);
  #edef

  #############################################################################

  def make_conf(self, outdir, i_d, l_d, p_d):
    filename = '%s/%s.conf' % (self.outdir, self.name);
    fd = open(filename, 'w');
    fd.write(self.TXT_circos_conf % (','.join(self.karyotypes), self.chromosomes_units, ';'.join(self.chrs), 'chromosomes_scale = ' + ','.join(self.chr_scale), i_d, l_d, p_d));
    fd.close();
  #edef

  #############################################################################

  def make_ideogram(self, outdir):
    return self.TXT_ideogram_conf;
  #edef

  #############################################################################

  def make_links(self, outdir):
    data = "";

    data +='<links>\n';
    for bl in self.clust_links:
      data += '  <link>\n';
      data += '    file          = %s\n' % bl;
      data += self.TXT_links_conf;
      data += '  </link>\n';
    #efor
    data += '</links>\n';

    return data;
  #edef

  #############################################################################

  def make_plots(self, outdir):
    data = "";

    data += '<plots>\n';
    for gene in self.gene_tiles:
      data += self.TXT_gene_plot % gene;
    #efor
    data += '</plots>\n';

    return data;
  #edef

  #############################################################################

#eclass

