# Error note

## Observation
Q01 下 T07 位于 rank 3，score 0.690192；T07 的文本谈小企业贷款（The bank approved a loan for the small business.）。

## Speculation
“bank” 的词面歧义可能让金融句保留较高相似度；query 中的 bank 同时激活了河岸与金融机构两种语义。

## Missing evidence
这是 teacher_demo_fixture（手工示范向量），不是任何真实模型的输出，因此不能判定 MiniLM、E5 或 BGE-M3 是否会出现相同排序行为。

## Next test
在 cached MiniLM 下固定 corpus、L2 normalization 与 top-k=3，只把 query 从 Q01（river bank）改为 Q02（river shore beside flowing water），再比较 T07 的 rank 与 score 变化。
