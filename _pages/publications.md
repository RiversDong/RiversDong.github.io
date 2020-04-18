---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}

* Dong C, Hao G F, Hua H L, et al. Anti-CRISPRdb: a comprehensive online resource for anti-CRISPR proteins[J]. Nucleic acids research, 2017, 46(D1): D393-D398.
* Dong C, Jin Y T, Hua H L, et al. Comprehensive review of the identification of essential genes using computational methods: focusing on feature implementation and assessment[J]. Briefings in bioinformatics, 2018, bby116.
* Dong C, Dong-Kai Pu et al. AcrDetector: sensitively detect Acrs in prokaryotes using only six features.
* Dong C, Zeng Z, Wen Q F, et al. CasLocusAnno: a web-based server for annotating Cas loci and their corresponding (sub) types[J]. FEBS Letters, 2019, 593(18):2646-2654.
* Dong C, Yuan Y Z, Zhang F Z, et al. Combining pseudo dinucleotide composition with the Z curve method to improve the accuracy of predicting DNA elements: a case study in recombination spots[J]. Molecular BioSystems, 2016, 12(9): 2893-2900. 
* Guo F B, Dong C, Hua H L, et al. Accurate prediction of human essential genes using only nucleotide composition and association information[J]. Bioinformatics, 2017, 33(12): 1758-1764.
* Wen Q F, Shuo L, Dong C, et al. Geptop 2.0: an updated, more precise, and faster Geptop server for identification of prokaryotic essential genes[J]. Frontiers in Microbiology, 2019, 10: 1236.
