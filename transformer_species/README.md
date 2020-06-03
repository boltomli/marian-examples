# Example: Training a transformer model

Files and scripts in this folder show how to train a Google-style transformer model ([Vaswani et al, 2017](https://arxiv.org/abs/1706.03762)) on species canonical and Chinese names.

The problem set has created following the example from the original [tensor2tensor](https://github.com/tensorflow/tensor2tensor) repository by Google. It uses 32,000 common BPE units for both languages.

Assuming four GPUs are available (here 0 1 2 3), execute the command below to run the complete example:

```
./run-me.sh 0 1 2 3
```

The original training setting includes:

* Fitting mini-batch sizes to 4GB of GPU memory with synchronous SGD (ADAM), which results in large mini-batches. This has been chosen to fit on GPUs with about 6GB of RAM, we leave about 2GB for the remaining training parameters.
* Validation on external data set using cross-entropy, perplexity and BLEU
* 6-layer (or rather block) encoder and 6-layer decoder
* Tied embeddings for source, target and output layer
* Label smoothing
* Learning rate warm-up and cool-down
* Multi-GPU training

You can reduce the workspace size to about `-w 2000` if you want to fit on smaller GPUs with 4GB of RAM or increase it further more on GPUs with more RAM. On a Volta GPU with 16GB of RAM you can set `-w 14000` when using four GPUs.

The evaluation is performed on extinct species. `data/corpus.{en,zh}` and `data/valid.{en,zh}` are prepared manually.

For training data, a few databases might help.

* [中国生物物种名录](http://sp2000.org.cn/info/info_how_to_cite): The Biodiversity Committee of Chinese Academy of Sciences, 2020, Catalogue of Life China: 2020 Annual Checklist, Beijing, China.

```sql
SELECT canonical_name,
	CASE
		WHEN species_c <> '' THEN species_c 
		WHEN genus_c = '' THEN NULL
		WHEN substr(genus_c, -1) = '属' THEN substr(genus_c, 1, length(genus_c) - 1)
		ELSE genus_c
	END AS name_c
FROM scientific_names sn JOIN families f 
ON sn.family_id = f.record_id
WHERE f.class = 'Mammalia'
```

* [Species 2000 & ITIS Catalogue of Life](https://www.sp2000.org/index.php?option=com_content&task=view&id=17&Itemid=33): Roskov Y., Ower G., Orrell T., Nicolson D., Bailly N., Kirk P.M., Bourgoin T., DeWalt R.E., Decock W., Nieukerken E. van, Zarucchi J., Penev L., eds. (2019). Species 2000 & ITIS Catalogue of Life, 2019 Annual Checklist. Digital resource at www.catalogueoflife.org/annual-checklist/2019. Species 2000: Naturalis, Leiden, the Netherlands. ISSN 2405-884X.

```sql
SELECT Taxon.genus || ' ' || Taxon.specificEpithet AS canonical_name, vn.vernacularName AS name_c
FROM VernacularName vn JOIN Taxon
ON vn.taxonID = Taxon.taxonID
WHERE vn.language IN ('Mandarin Chinese')
```

See the transformer example (`marian/examples/transformer/`) for more details.
